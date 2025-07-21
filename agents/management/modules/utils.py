"""
유틸리티 및 보조 함수 모듈

이 모듈은 Management Workflow에서 사용할 수 있는 다양한 유틸리티 함수를 제공합니다.
인스타그램 컨텐츠 검증, 정책 검색, 위험 요소 분석에 필요한 유틸리티 함수들을 포함합니다.

추후 개발 시 필요한 유틸리티 함수를 이 모듈에 추가하여 코드 재사용성을 높일 수 있습니다.
예를 들어, 텍스트 전처리, 포맷팅, 데이터 변환 등의 기능을 구현할 수 있습니다.
"""

from typing import Any, Dict


def format_verification_result(result: Dict[str, Any]) -> str:
    """
    인스타그램 컨텐츠 검증 결과를 포맷팅합니다.

    Args:
        result: 검증 결과 딕셔너리

    Returns:
        str: 포맷팅된 결과 문자열
    """
    if "error" in result:
        return f"오류: {result['error']}"

    status = "승인" if result.get("is_approved", False) else "거부"
    score = result.get("score", 0.0)
    risk_level = result.get("risk_level", "unknown")

    formatted = f"""
인스타그램 컨텐츠 검증 결과:
상태: {status}
점수: {score:.2f}
위험도: {risk_level}

승인/거부 이유:
"""

    for reason in result.get("reasons", []):
        formatted += f"- {reason}\n"

    if result.get("warnings"):
        formatted += "\n경고사항:\n"
        for warning in result["warnings"]:
            formatted += f"- {warning}\n"

    if result.get("suggestions"):
        formatted += "\n개선 제안:\n"
        for suggestion in result["suggestions"]:
            formatted += f"- {suggestion}\n"

    if result.get("policy_references"):
        formatted += "\n참조한 정책:\n"
        for policy in result["policy_references"]:
            formatted += f"- {policy}\n"

    if result.get("similar_cases"):
        formatted += "\n유사한 사례:\n"
        for case in result["similar_cases"]:
            formatted += f"- {case}\n"

    return formatted
