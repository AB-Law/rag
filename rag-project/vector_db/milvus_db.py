import json
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
from vector_db.base import VectorDB  # Assuming VectorDB is defined in base.py
from langchain_community.vectorstores import Milvus
import fitz  # PyMuPDF

class MilvusVectorDB(VectorDB):
    def __init__(self, host='127.0.0.1', port='19530'):
        self.host = host
        self.port = port
        self.embeddings = OpenAIEmbeddings()
        self._connect()

    def _connect(self):
        connections.connect(host=self.host, port=self.port)

    def store_embeddings(self, docs, collection_name, user_owner=None):
        if user_owner is None:
            vector_db = Milvus.from_documents(
                docs,
                self.embeddings,
                connection_args={"host": self.host, "port": self.port},
                collection_name=collection_name
            )
        else:
            vector_db = Milvus.from_documents(
                docs,
                self.embeddings,
                connection_args={"host": self.host, "port": self.port},
                collection_name=collection_name,
                partition_key_field="userOwner"
            )

    def query_db(self, query, collection_name, user_owner = None):
        vector_db = Milvus(
            self.embeddings,
            connection_args={"host": self.host, "port": self.port},
            collection_name=collection_name,
            partition_key_field="userOwner"
        )
        if user_owner is None:
            retriever = vector_db.as_retriever()
        else:
            retriever = vector_db.as_retriever(search_kwargs={"expr": f'userOwner == "{user_owner}"'})
        return retriever.invoke(query)
