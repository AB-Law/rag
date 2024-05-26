import json
from vector_db import VectorDBFactory  # Assuming this is the correct path
from document_loader.pdf_loader import PDFLoader  # Import the specific loader you want to use

def main():
    pdf_path = 'sample.pdf'  # Replace with the path to your PDF file

    # Load configuration
    with open('config/config.json', 'r') as f:
        config = json.load(f)

    # Create vectorDB instance for Milvus
    vector_db = VectorDBFactory.create_vector_db(config)
    collection_name = "pdfs"  # Need to change if not using partitioning

    # Load documents from PDF using the specified loader
    loader = PDFLoader()
    documents = loader.load_docs(pdf_path, user_owner="")
    print(len(documents))
    
    # Store embeddings in Milvus
    vector_db.store_embeddings(documents, collection_name=collection_name)

    # Query embeddings using Milvus
    #query_result = vector_db.query_db("where did i work?", collection_name, user_owner="")
    query_result = vector_db.query_db("where did i work?", collection_name)
    print(query_result)

if __name__ == "__main__":
    main()
