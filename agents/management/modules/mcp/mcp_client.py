import os
import logging
import json
import subprocess
import base64
from typing import Any, Dict

logger = logging.getLogger(__name__)

def verify_instagram_content(
    content_text: str, content_type: str = "text"
) -> Dict[str, Any]:
    logger.info(
        f"[MCP 클라이언트] verify_instagram_content 호출 - content_text: {content_text}, content_type: {content_type}"
    )
    
    mcp_server_command = os.getenv("MCP_SERVER_COMMAND", "python3")
    # 모듈로 실행할 경로
    module_path = "agents.management.modules.mcp"
    
    input_payload = {
        "content_text": content_text,
        "content_type": content_type,
    }
    input_json = json.dumps(input_payload)
    encoded_input = base64.b64encode(input_json.encode('utf-8')).decode('utf-8')

    # python -m <module_path> <encoded_input> 형태로 커맨드 구성
    command = [mcp_server_command, "-m", module_path, encoded_input]
    logger.info(f"[MCP 클라이언트] Executing command: {' '.join(command)}")

    try:
        # subprocess.run을 사용하여 동기적으로 프로세스를 실행하고 결과를 기다립니다.
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            timeout=60.0,
            env=os.environ.copy()
        )

        if result.stderr:
            logger.error(f"[MCP 서버 stderr]\n{result.stderr.decode('utf-8', 'ignore').strip()}")

        if result.returncode != 0:
            logger.error(f"MCP 서버 프로세스가 비정상적으로 종료되었습니다. Exit code: {result.returncode}")
            return {"error": f"MCP 서버 오류 (exit code: {result.returncode})"}

        if not result.stdout:
            logger.error("MCP 서버로부터 응답이 없습니다.")
            return {"error": "MCP 서버로부터 응답을 받지 못했습니다."}
            
        try:
            return json.loads(result.stdout.decode('utf-8'))
        except json.JSONDecodeError:
            logger.error(f"MCP 서버의 응답을 파싱하는 데 실패했습니다: {result.stdout.decode('utf-8')}")
            return {"error": "MCP 서버로부터 유효하지 않은 JSON 응답을 받았습니다."}

    except subprocess.TimeoutExpired:
        logger.error("MCP 서버와의 통신 시간이 초과되었습니다.")
        return {"error": "MCP 서버 시간 초과"}
        
    except Exception as e:
        logger.error(f"MCP 클라이언트에서 예외가 발생했습니다: {e}")
        return {"error": f"클라이언트 오류: {e}"}

