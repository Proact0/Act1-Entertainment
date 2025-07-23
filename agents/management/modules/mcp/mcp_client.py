import os
import logging
import json
import asyncio
from typing import Any, Dict

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession

from agents.management.modules.models import get_openai_model


async def verify_instagram_content(
    content_text: str, content_type: str = "text"
) -> Dict[str, Any]:
    logger = logging.getLogger(__name__)
    logger.info(
        f"[MCP 클라이언트] verify_instagram_content 호출 - content_text: {content_text}, content_type: {content_type}"
    )
    # 서버 실행 명령어와 인자 지정
    mcp_server_command = os.getenv("MCP_SERVER_COMMAND", "python3")
    mcp_server_args = os.getenv(
        "MCP_SERVER_ARGS", "agents/management/modules/mcp/mcp_contents_verify_server.py"
    ).split()
    logger.info(
        f"[MCP 클라이언트] MCP_SERVER_COMMAND: {mcp_server_command}, MCP_SERVER_ARGS: {mcp_server_args}"
    )

    command = [mcp_server_command] + mcp_server_args
    command_str = " ".join(command)
    logger.info(f"[MCP 클라이언트] Executing command: {command_str}")

    proc = await asyncio.create_subprocess_shell(
        command_str,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )

    try:
        async with ClientSession(proc.stdout, proc.stdin) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print("사용 가능한 도구:", tools)

            graph = create_react_agent(model=get_openai_model(), tools=tools)

            query = (
                f"다음 인스타그램 컨텐츠를 검증해주세요: "
                f"{content_text} (유형: {content_type})"
            )
            response = await graph.ainvoke({"messages": [("user", query)]})

            last_content = None
            if "messages" in response:
                messages = response["messages"]
                for message in reversed(messages):
                    if hasattr(message, "content") and message.content:
                        last_content = message.content
                        break
            if last_content:
                try:
                    return json.loads(last_content)
                except json.JSONDecodeError:
                    logger.error(
                        f"Failed to decode JSON from LLM response: {last_content}"
                    )
                    # Return a dict that indicates an error
                    return {"error": "Invalid JSON response from model"}

            return {"error": "No content received from model"}
    finally:
        proc.kill()
        await proc.wait()
