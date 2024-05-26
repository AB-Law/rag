from langchain_community.document_loaders import PyMuPDFLoader
from document_loader.base import DocumentLoader

class PDFLoader(DocumentLoader):
    def load_docs(self, file_path, user_owner=None):
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        for doc in documents:
            metadata = doc.metadata
            metadata["userOwner"] = user_owner
        return documents
