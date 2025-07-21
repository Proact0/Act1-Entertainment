"""
아래는 예시입니다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict, Optional, Dict, Any

from langgraph.graph.message import add_messages


class ManagementState(TypedDict):
    content_verification_result: Optional[Dict[str, Any]]
