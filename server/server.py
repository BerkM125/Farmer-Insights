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
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )

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

@app.route('/rag-query', methods=['POST'])
def rag_query():
    """
    Process a RAG query and return LLM response with context.

    Expected JSON body:
    {
        "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."},
            ...
        ],
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

        if not data or 'messages' not in data:
            return jsonify({'error': 'Missing "messages" in request body'}), 400

        messages = data['messages']
        n_results = data.get('n_results', 3)

        # Get the latest user message for RAG context retrieval
        user_messages = [m for m in messages if m['role'] == 'user']
        if not user_messages:
            return jsonify({'error': 'No user messages found'}), 400
        
        latest_user_prompt = user_messages[-1]['content']

        # Get relevant context from RAG
        context_items = get_rag_context(latest_user_prompt, n_results)

        # Format context for LLM
        context_text = "\n\n".join([
            f"[Source: {item['metadata']['source']}]\n{item['text']}"
            for item in context_items
        ])

        # Create system message with RAG context
        system_message = f"""You are a helpful agricultural assistant with access to a knowledge base.
Use the provided context to answer the user's questions accurately. If the context doesn't contain
relevant information, acknowledge this and provide your best general answer. In your response, do not state 
the words, \"the provided context\", \"the given information\", and phrases similar to these.

Context from knowledge base:
{context_text}"""

        # Build the messages array for the LLM with conversation history
        llm_messages = [{"role": "system", "content": system_message}]
        
        # Add conversation history (excluding any existing system messages)
        for msg in messages:
            if msg['role'] != 'system':
                llm_messages.append({"role": msg['role'], "content": msg['content']})

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
                "messages": llm_messages
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