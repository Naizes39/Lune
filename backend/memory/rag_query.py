import chromadb

def query_knowledge(query_text: str, n_results: int = 3):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="lune_knowledge")
    return collection.query(query_texts=[query_text], n_results=n_results)


if __name__ == "__main__":
    result = query_knowledge(query_text="Is this a PDF document?")
    print(result)