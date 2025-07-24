import json
import logging
import sys
import asyncio
import base64
from agents.management.modules.mcp.mcp_contents_verify_server import verify_instagram_content

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, format=("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("MCP Contents Verify 서버 시작 (모듈 실행 모드)...")
    
    input_data = None
    try:
        if len(sys.argv) < 2:
            raise ValueError("필요한 커맨드 라인 인수가 없습니다.")
        
        encoded_input = sys.argv[1]
        decoded_input = base64.b64decode(encoded_input).decode('utf-8')
        input_data = json.loads(decoded_input)

    except (json.JSONDecodeError, ValueError, IndexError) as e:
        logger.error(f"입력 데이터를 읽거나 파싱하는 데 실패했습니다: {e}")
        print(json.dumps({"error": "Invalid or missing input data", "details": str(e)}))
        sys.exit(1)

    content_text = input_data.get("content_text", "")
    content_type = input_data.get("content_type", "text")
    
    result = asyncio.run(verify_instagram_content(content_text, content_type))
    
    print(json.dumps(result, ensure_ascii=False))
    logger.info("작업 완료, 서버 종료.")
