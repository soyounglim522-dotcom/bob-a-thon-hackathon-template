"""
팀의 첫 번째 wxo Agent 툴.

파일명 stem(my_tool) == @tool 함수명(my_tool) == agents/my_agent.yaml의 tools: 항목
이 세 곳을 항상 동일하게 유지하세요.
"""

from typing import Generic, Optional, TypeVar

import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, computed_field
from pydantic.dataclasses import dataclass

# ---------------------------------------------------------------------------
# ToolResponse / ErrorDetails — 반드시 각 tool 파일에 인라인으로 포함하세요.
# (공유 모듈에서 import 하지 마세요 — AGENTS.md 참고)
# ---------------------------------------------------------------------------

T = TypeVar("T")


@dataclass
class ErrorDetails:
    """툴 오류 정보를 담는 통합 래퍼."""

    status_code: Optional[int]
    url: Optional[str]
    reason: Optional[str]
    details: Optional[str]
    recommendation: Optional[str]


class ToolResponse(BaseModel, Generic[T]):
    """모든 툴 응답을 감싸는 통합 래퍼."""

    error_details: Optional[ErrorDetails]
    tool_output: Optional[T]

    @computed_field  # type: ignore[misc]
    @property
    def is_success(self) -> bool:
        return self.error_details is None


# ---------------------------------------------------------------------------
# 응답 데이터 모델 — 툴이 반환하는 데이터 구조를 여기에 정의하세요.
# ---------------------------------------------------------------------------

@dataclass
class MyToolResult:
    """TODO: 실제 반환 데이터에 맞게 필드를 수정하세요."""

    summary: str


# ---------------------------------------------------------------------------
# @tool 함수 — 파일명 stem과 함수명이 반드시 일치해야 합니다.
# ---------------------------------------------------------------------------

@tool
def my_tool(query: str) -> ToolResponse[MyToolResult]:
    """
    사용자의 질문에 답변합니다.

    Args:
        query: 사용자가 입력한 질문 또는 검색어.

    Returns:
        MyToolResult를 담은 ToolResponse. 오류 시 error_details에 원인이 담깁니다.
    """
    # TODO: 아래 예시 코드를 실제 API 호출 로직으로 교체하세요.
    try:
        # 예시: API 호출
        # response = requests.get("https://api.example.com/...", params={"q": query}, timeout=10)
        # response.raise_for_status()
        # data = response.json()
        pass
    except requests.exceptions.RequestException as exc:
        return ToolResponse(
            tool_output=None,
            error_details=ErrorDetails(
                status_code=getattr(getattr(exc, "response", None), "status_code", None),
                url=None,
                reason=str(exc),
                details=None,
                recommendation="네트워크 상태를 확인하거나 잠시 후 다시 시도하세요.",
            ),
        )

    return ToolResponse(
        error_details=None,
        tool_output=MyToolResult(summary=f"'{query}'에 대한 결과입니다. (실제 구현으로 교체 필요)"),
    )
