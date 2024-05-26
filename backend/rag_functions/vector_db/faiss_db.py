import faiss
from .base import VectorDB
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class FAISSVectorDB(VectorDB):
    def __init__(self, host='127.0.0.1', port='19530'):
        self.host = host
        self.port = port
        self.embeddings = OpenAIEmbeddings()
        self.db = None

    def store_embeddings(self, docs, embeddings, metadata=None):
        self.db = FAISS.from_documents(docs, embeddings)

    def search_embeddings(self, query, top_k):
        return self.db.similarity_search(query)

    def save_local(self, path="faiss_index"):
        self.db.save_local(path)

    def load_local(self, path="faiss_index"):
        self.db = FAISS.load_local(path, self.embeddings,allow_dangerous_deserialization=True)

    def as_retriever(self,query):
        retriever = self.db.as_retriever()
        return retriever.invoke(query)
