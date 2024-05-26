import json
from vector_db.faiss_db import FAISSVectorDB
from langchain_openai import OpenAIEmbeddings
from document_loader.pdf_loader import PDFLoader


import os

def main():
    pdf_path = 'sample.pdf'

    # Load configuration
    with open('config/config.json', 'r') as f:
        config = json.load(f)

    vector_db = FAISSVectorDB()
    embeddings = OpenAIEmbeddings()

    index_path = "faiss_index"
    loader = PDFLoader()
    if os.path.exists(index_path):
        try:
            vector_db.load_local(index_path)
            print("FAISS index loaded successfully.")
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")
            print("Proceeding to store embeddings in a new FAISS index.")
            documents = loader.load_docs(pdf_path, user_owner="")
            vector_db.store_embeddings(documents, embeddings)
            vector_db.save_local(index_path)
    else:
        print("FAISS index not found. Storing embeddings in a new FAISS index.")
        documents = loader.load_docs(pdf_path, user_owner="")
        vector_db.store_embeddings(documents, embeddings)
        vector_db.save_local(index_path)

    # Query embeddings using FAISS
    query_result = vector_db.as_retriever("sample query")
    print(query_result)

if __name__ == "__main__":
    main()