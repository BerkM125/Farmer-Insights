import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

client = chromadb.PersistentClient(path="./chroma_db")

embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="static_knowledge_base",
    embedding_function=embedding,
    metadata={"description": "A collection using all-MiniLM-L6-v2 embeddings"}
)

print(f"Collection created: {collection.name}")
print(f"Collection count before: {collection.count()}")

def semantic_chunking(text: str, similarity_threshold: float = 0.5, min_chunk_size: int = 100, max_chunk_size: int = 1500):
    """
    Split text into semantically coherent chunks based on sentence similarity.

    Args:
        text: Input text to chunk
        similarity_threshold: Threshold for semantic similarity (0-1). Lower = more chunks
        min_chunk_size: Minimum characters per chunk
        max_chunk_size: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    # Initialize sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 1:
        return [text]

    # Get embeddings for each sentence
    embeddings = model.encode(sentences)

    # Calculate similarity between consecutive sentences
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
        similarities.append(sim)

    # Find split points where similarity drops below threshold
    chunks = []
    current_chunk = [sentences[0]]
    current_length = len(sentences[0])

    for i, sentence in enumerate(sentences[1:]):
        sentence_length = len(sentence)

        # Check if we should split based on similarity or size constraints
        should_split = False

        if i < len(similarities):
            # Split if similarity is low OR chunk is getting too large
            if similarities[i] < similarity_threshold or current_length + sentence_length > max_chunk_size:
                # Only split if current chunk meets minimum size
                if current_length >= min_chunk_size:
                    should_split = True

        if should_split:
            # Save current chunk and start new one
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            # Add to current chunk
            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for space

    # Add the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

knowledge_base_path = Path("./static_knowledge_base")
documents = []
ids = []
metadatas = []

if knowledge_base_path.exists() and knowledge_base_path.is_dir():
    for text_file in knowledge_base_path.glob("*.txt"):
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                # Chunk the content using semantic chunking
                chunks = semantic_chunking(content, similarity_threshold=0.5)

                # Add each chunk as a separate document
                for idx, chunk in enumerate(chunks):
                    documents.append(chunk)
                    ids.append(f"doc_{text_file.stem}_chunk_{idx}")
                    metadatas.append({
                        "source": str(text_file.name),
                        "path": str(text_file),
                        "chunk_index": idx,
                        "total_chunks": len(chunks)
                    })

    print(f"Found {len(set([m['source'] for m in metadatas]))} text files in {knowledge_base_path}")
    print(f"Created {len(documents)} chunks from all files")

    # Add documents to the collection
    if documents:
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"Added {len(documents)} documents to the collection")
        print(f"Collection count after: {collection.count()}")
    else:
        print("No documents found to add")
else:
    print(f"Directory {knowledge_base_path} does not exist")