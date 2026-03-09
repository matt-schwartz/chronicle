import os
import anthropic

from storage.vector import collection
import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def search_context(query, project=None):
    # Search vector DB
    where_filter = {"project": project} if project else None
    results = collection.query(
        query_texts=[query],
        n_results=5,
        where=where_filter,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    # Build context from retrieved documents
    context = "\n\n".join(
        f"[Source: {id}]\n{doc}" for id, doc in zip(ids, documents)
    )

    # Use Claude to synthesize an answer
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Use the following context to answer the question. "
                    f"If the context doesn't contain enough information, say so.\n\n"
                    f"Context:\n{context}\n\n"
                    f"Question: {query}"
                ),
            }
        ],
    )

    answer = message.content[0].text

    sources = [
        {"id": id, "document": doc, "metadata": meta}
        for id, doc, meta in zip(ids, documents, metadatas)
    ]

    return {
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    query = input("Enter your query: ")
    result = search_context(query, project=None)
    print("\nAnswer:\n", result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"ID: {source['id']}, Metadata: {source['metadata']}, Document: {source['document']}")
