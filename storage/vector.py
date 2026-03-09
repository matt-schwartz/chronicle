import os
import chromadb

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devcontext.vector')

# Initialize client
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("dev_context")

# Store event with embedding
def store_with_embedding(id, content, type, project, timestamp) -> None:
    collection.add(
        documents=[content],
        metadatas=[{
            'type': type,
            'project': project,
            'timestamp': timestamp 
        }],
        ids=[id]
    )

