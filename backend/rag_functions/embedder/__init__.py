from langchain_openai import OpenAIEmbeddings



def currentEmbedding():
    # Todo: Implement a way to switch between different embeddings
    embedding = OpenAIEmbeddings()
    return embedding