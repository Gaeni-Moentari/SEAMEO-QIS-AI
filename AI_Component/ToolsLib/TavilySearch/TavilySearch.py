from langchain_community.tools.tavily_search import TavilySearchResults
from crewai.tools import BaseTool
import os 

os.environ['TAVILY_API_KEY'] = os.getenv("tavilyapi_key")

class TavilySearch(BaseTool):
    name: str = "TavilySearch"
    description: str = "Search related information using this tools"
    
    def _run(self,query:str):
        search = TavilySearchResults(k=5)
        return search.invoke({'query':f'{query}'})
