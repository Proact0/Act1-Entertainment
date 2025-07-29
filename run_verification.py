import json
import sys
import logging
import os
from dotenv import load_dotenv
from agents.management.modules.tools import verify_instagram_content_tool
#/Pseudo-Entertainment$ uv run run_verification.py '{"content_text": "오나전 야마", "content_type": "text"}'
# .env 파일에서 환경 변수 로드
load_dotenv()

# LangSmith 추적 설정
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# 기본 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def main():
    """
    LangGraph 프레임워크를 우회하여 인스타그램 컨텐츠 검증 도구를 직접 실행합니다.
    JSON 입력을 커맨드 라인 인수로 받습니다.
    """
    if len(sys.argv) < 2:
        print(json.dumps({"error": "JSON input is required as a command-line argument."}))
        sys.exit(1)

    try:
        # 커맨드 라인 인수에서 JSON 문자열을 파싱
        input_str = sys.argv[1]
        input_data = json.loads(input_str)
        
        content_text = input_data.get("content_text")
        content_type = input_data.get("content_type", "text")

        if not content_text:
            print(json.dumps({"error": "'content_text' field is required in the JSON input."}))
            sys.exit(1)

        # 도구를 직접 호출
        result = verify_instagram_content_tool(content_text, content_type)
        
        # 결과를 JSON 형태로 출력
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON format in command-line argument."}))
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(json.dumps({"error": "An unexpected error occurred.", "details": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
