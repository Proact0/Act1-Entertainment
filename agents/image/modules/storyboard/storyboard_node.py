from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from agents.base_node import BaseNode
from agents.image.modules.storyboard.models import get_gemini_model

class StoryboardNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.llm = get_gemini_model()
    
    @asynccontextmanager
    async def mcp_client(self):
        async with MultiServerMCPClient(
            {
                "Story" : {
                    "command": "uv run python",
                    "args": ["./mcp_server.py"],
                    "transport": "stdio"
                }
            }
        ) as client:
            tools = client.get_tools()
            agent = create_react_agent(model= self.llm, tools=tools)
            yield agent
    
