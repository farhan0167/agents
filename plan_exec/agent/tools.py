from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool


tools = [TavilySearchResults(max_results=3)]
tools_by_name = {tool.name: tool for tool in tools}