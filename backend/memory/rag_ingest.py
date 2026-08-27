



#   2. ingest_document(document_id: str, raw_text: str)
#       • Use collection.add() to insert the chunks. Remember, Chroma requires three lists: documents (the text),
#       metadatas (e.g., {"source": document_id}), and ids (e.g., f"{document_id}_chunk_1").


#   At the bottom of the file, write a quick test block:

import chromadb

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str] | None:
        text = text.strip()
        if not text:
            return None

        chunks: list[str] = []
        text_length: int = len(text)

        left = 0

        while left < text_length:
            chunk: str = text[left : left + chunk_size]

            if left + chunk_size >= text_length:
                chunks.append(chunk)
                break 

            chunk = chunk.rsplit(" ", 1)[0]
            chunks.append(chunk)

            left = left + len(chunk) - overlap

        return chunks




def ingest_document(document_id: str, raw_text: str):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="lune_knowledge")
    chunks = chunk_text(raw_text)
    chunks_ids = [f"id{x}" for x in range(len(chunks))]
    metadata = [{"source": document_id} for _ in range(len(chunks))]
    collection.add(ids=chunks_ids, documents= chunks, metadatas=metadata)

if __name__ == "__main__":
    test_text = "This is a massive wall of text simulating a PDF document. " * 50
    ingest_document("test_doc_01", test_text)
    print("Ingestion complete.")
