from ..tools.searx import create_searx_tool
from ..tools.milvus_retriever import create_retriever, similarity_search_with_relevance_scores
from ..embedder import currentEmbedding
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import OpenAIEmbeddings

def rag_chat(query, collection_name, partition_name=None, host="http://localhost:8888", relevance_threshold=0.6):
    vector_db_tool = create_retriever(OpenAIEmbeddings(), collection_name, partition_name)
    searx_tool = create_searx_tool(host)
    tools = [vector_db_tool]
    llm = ChatOpenAI(temperature=0)
    prompt = hub.pull("hwchase17/openai-tools-agent")

    # First, try the vector database search
    docs_and_scores = similarity_search_with_relevance_scores(query, collection_name, partition_name)
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
    # return docs_and_scores

    #Check the relevance score of the vector database results
    if docs_and_scores and docs_and_scores[0][1] > relevance_threshold:
        # If the vector database results are not relevant enough, use the Searx tool
        tools = [searx_tool]
        agent = create_openai_tools_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
        result = agent_executor.invoke({"input": query})
        
    else:
        result = agent_executor.invoke({"input": query})

    return result