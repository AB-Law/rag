from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.docstore.document import Document
from typing import List, Tuple


def create_retriever(embeddings, collection_name, partition_name=None):
    embeddings = OpenAIEmbeddings()
    if partition_name is None:
        vector_db = Milvus(
                embeddings,
                collection_name=collection_name
                )
    else:
        #Add connection string method
        vector_db = Milvus(
                embeddings,
                collection_name=collection_name,
                partition_key_field=partition_name
            )
    
    retriever = Milvus.as_retriever(vector_db)


    milvus_tool = create_retriever_tool(
    retriever,
    "search_pdfs",
    "Searches and returns excerpts from the stored pdfs",
)

    return milvus_tool

def similarity_search_with_relevance_scores(query: str, collection_name: str, partition_name: str = None) -> List[Tuple[Document, float]]:
    """
    Perform a similarity search on the Milvus vector store and return the results with relevance scores.

    Args:
        query (str): The query to search for.
        collection_name (str): The name of the Milvus collection to search.
        partition_name (str, optional): The name of the Milvus partition to search.

    Returns:
        List[Tuple[Document, float]]: A list of tuples containing the retrieved documents and their relevance scores.
    """
    embeddings = OpenAIEmbeddings()

    if partition_name is None:
        vector_db = Milvus(
            embeddings,
            collection_name=collection_name
        )
    else:
        vector_db = Milvus(
            embeddings,
            collection_name=collection_name,
            partition_key_field=partition_name
        )

    # Perform the similarity search with scores
    docs_and_scores = vector_db.similarity_search_with_score(query, k=4)

    # Create a list of Document objects with the retrieved documents and their scores
    docs_and_scores_with_docs = [(Document(page_content=doc.page_content, metadata=doc.metadata), score) for doc, score in docs_and_scores]

    return docs_and_scores_with_docs
