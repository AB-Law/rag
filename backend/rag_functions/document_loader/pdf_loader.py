from typing import Optional, List, Dict
from langchain_community.document_loaders import PyMuPDFLoader
from .base import DocumentLoader

class PDFLoader(DocumentLoader):
    """A class for loading documents from PDF files."""
    
    def load_docs(self, file_path: str, user_owner: Optional[str] = None) -> List[Dict]:
        """
        Load documents from a PDF file.

        Parameters:
        file_path (str): The path to the PDF file.
        user_owner (Optional[str], optional): The owner of the document. Defaults to None.

        Returns:
        List[Dict]: A list of dictionaries containing document metadata.
        """
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        for doc in documents:
            metadata = doc.metadata
            metadata["userOwner"] = user_owner
        return documents
