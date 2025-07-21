import os

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from fastmcp import Client

from agents.management.modules.models import get_openai_model


async def verify_instagram_content(
    content_text: str, content_type: str = "text"
) -> str:
    """
    비동기적으로 인스타그램 컨텐츠 검증 MCP 서버에 요청을 보내고, 응답을 반환합니다.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[MCP 클라이언트] verify_instagram_content 호출: {content_text}, {content_type}")
    logger.info(f"[langgraph] verify_instagram_content 쿼리: {content_text}, {content_type}")

    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

    async with Client(mcp_server_url) as client:
        tools = await load_mcp_tools(client)
        print("사용 가능한 도구:", tools)

        graph = create_react_agent(model=get_openai_model(), tools=tools)

        query = (
            f"다음 인스타그램 컨텐츠를 검증해주세요: "
            f"{content_text} (유형: {content_type})"
        )
        response = await graph.ainvoke({"messages": query})

        if "messages" in response:
            messages = response["messages"]
            for message in messages:
                if hasattr(message, "content") and message.content:
                    last_content = message.content
                    break

        return last_content


async def search_instagram_policies(keywords: str) -> str:
    """
    비동기적으로 인스타그램 정책 검색 MCP 서버에 요청을 보내고, 응답을 반환합니다.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[langgraph] search_instagram_policies 쿼리: {keywords}")

    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

    async with Client(mcp_server_url) as client:
        tools = await load_mcp_tools(client)
        print("사용 가능한 도구:", tools)

        graph = create_react_agent(model=get_openai_model(), tools=tools)

        query = f"다음 키워드로 인스타그램 정책을 검색해주세요: {keywords}"
        response = await graph.ainvoke({"messages": query})

        if "messages" in response:
            messages = response["messages"]
            for message in messages:
                if hasattr(message, "content") and message.content:
                    last_content = message.content
                    break

        return last_content


async def analyze_content_risks(content_text: str) -> str:
    """
    비동기적으로 컨텐츠 위험 분석 MCP 서버에 요청을 보내고, 응답을 반환합니다.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[langgraph] analyze_content_risks 쿼리: {content_text}")

    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

    async with Client(mcp_server_url) as client:
        tools = await load_mcp_tools(client)
        print("사용 가능한 도구:", tools)

        graph = create_react_agent(model=get_openai_model(), tools=tools)

        query = f"다음 컨텐츠의 위험 요소를 분석해주세요: {content_text}"
        response = await graph.ainvoke({"messages": query})

        if "messages" in response:
            messages = response["messages"]
            for message in messages:
                if hasattr(message, "content") and message.content:
                    last_content = message.content
                    break

        return last_content
