import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
print(f"Collection count: {collection.count()}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

knowledge_base_path = Path("./static_knowledge_base")
documents = []
ids = []
metadatas = []

if knowledge_base_path.exists() and knowledge_base_path.is_dir():
    for text_file in knowledge_base_path.glob("*.txt"):
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                # Chunk the content
                chunks = text_splitter.split_text(content)

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
    else:
        print("No documents found to add")
else:
    print(f"Directory {knowledge_base_path} does not exist")

# Query the collection
query_text = "pesticide"
results = collection.query(
    query_texts=[query_text],
    n_results=3,
    include=["documents", "distances", "metadatas"]
)

print(f"\n{'='*60}")
print(f"Query: '{query_text}'")
print(f"{'='*60}")

for i, (doc, distance, metadata) in enumerate(zip(
    results['documents'][0],
    results['distances'][0],
    results['metadatas'][0]
), 1):
    print(f"\nResult {i}:")
    print(f"  Document: {doc}")
    print(f"  Distance: {distance:.4f}")
    print(f"  Metadata: {metadata}")
