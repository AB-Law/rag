from langchain_core.tools import Tool
from langchain_community.utilities import SearxSearchWrapper

def create_searx_tool(host = "http://localhost:8888"):
    searx_wrapper = SearxSearchWrapper(searx_host=host)
    searx_tool = Tool(
        name="searx-search",
        description="A tool for searching using SearxNg",
        func=searx_wrapper.run,
    )
    return searx_tool
