from flask import Flask, jsonify, request
from flask_cors import CORS
import httpx
import asyncio
from functools import wraps
import chromadb
from chromadb.utils import embedding_functions
import os
import requests
import json
import base64
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root .env file
root_dir = Path(__file__).parent.parent
load_dotenv(dotenv_path=root_dir / '.env')

app = Flask(__name__)
CORS(app)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create collection
try:
    collection = chroma_client.get_collection(
        name="static_knowledge_base",
        embedding_function=embedding
    )
except Exception:
    collection = chroma_client.create_collection(
        name="static_knowledge_base",
        embedding_function=embedding,
        metadata={"description": "Static knowledge base for RAG"}
    )

# Initialize Lava Payments token
def get_lava_token():
    return base64.b64encode(json.dumps({
        "secret_key": os.getenv('LAVA_API_KEY'),
        "connection_secret": os.getenv('LAVA_SELF_CONNECTION_SECRET'),
        "product_secret": os.getenv('LAVA_SELF_PRODUCT_SECRET')
    }).encode()).decode()

def get_rag_context(query: str, n_results: int = 3):
    """
    Retrieve relevant documents from the vector database.

    Args:
        query: The search query
        n_results: Number of results to return

    Returns:
        List of dictionaries containing document text, distance, and metadata
    """
    # Check collection count
    count = collection.count()
    print(f"\n[RAG DEBUG] Collection has {count} documents")

    if count == 0:
        print("[RAG DEBUG] WARNING: Collection is empty! No documents to search.")
        return []

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )

    print(f"[RAG DEBUG] Query: {query}")
    print(f"[RAG DEBUG] Found {len(results['documents'][0])} results")

    context_items = []
    for doc, distance, metadata in zip(
        results['documents'][0],
        results['distances'][0],
        results['metadatas'][0]
    ):
        context_items.append({
            "text": doc,
            "distance": distance,
            "metadata": metadata
        })

    return context_items

@app.route('/')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'farmer_insights_api'}), 200

@app.route('/rag-query', methods=['POST'])
def rag_query():
    """
    Process a RAG query and return LLM response with context.

    Expected JSON body:
    {
        "prompt": "user's question",
        "n_results": 3  // optional, defaults to 3
    }

    Returns:
    {
        "response": "LLM response",
        "context": [...],  // retrieved documents
        "model": "gpt-4"
    }
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing "prompt" in request body'}), 400

        user_prompt = data['prompt']
        n_results = data.get('n_results', 3)

        # Get relevant context from RAG
        context_items = get_rag_context(user_prompt, n_results)

        # Format context for LLM
        context_text = "\n\n".join([
            f"[Source: {item['metadata']['source']}]\n{item['text']}"
            for item in context_items
        ])

        # Create LLM prompt with context
        system_message = """You are a helpful agricultural assistant with access to a knowledge base.
Use the provided context to answer the user's question accurately. If the context doesn't contain
relevant information, acknowledge this and provide your best general answer."""

        user_message = f"Context:\n{context_text}\n\nQuestion: {user_prompt}"

        # Print RAG prompt for debugging
        print("\n" + "="*80)
        print("RAG PROMPT TO LLM")
        print("="*80)
        print(f"\nSYSTEM MESSAGE:\n{system_message}\n")
        print(f"USER MESSAGE:\n{user_message}")
        print("="*80 + "\n")

        # Call OpenAI via Lava Payments
        token = get_lava_token()

        lava_response = requests.post(
            "https://api.lavapayments.com/v1/forward?u=https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        lava_data = lava_response.json()
        response_text = lava_data['choices'][0]['message']['content']

        return jsonify({
            'response': response_text,
            'context': context_items,
            'model': lava_data.get('model', 'gpt-4o-mini')
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)