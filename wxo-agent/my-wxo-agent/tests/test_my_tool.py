"""
my_tool 단위 테스트 템플릿.

실행:
    cd setup
    uv run pytest ../wxo-agent/my-wxo-agent/tests/ -v

requests를 HTTP 경계에서 mock 처리하여 실제 네트워크 없이 테스트합니다.
"""

import sys
import os

# tools/ 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from unittest.mock import MagicMock, patch

import pytest
import requests as requests_lib

from my_tool import my_tool


def test_my_tool_happy_path() -> None:
    """정상 응답 시 is_success=True, tool_output에 결과가 담긴다."""
    # TODO: 실제 API 응답 형식에 맞게 json_data를 수정하세요.
    with patch("my_tool.requests.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {},  # TODO: 실제 API 응답 구조로 교체
        )
        mock_get.return_value.raise_for_status = MagicMock(return_value=None)

        result = my_tool(query="테스트 질문")
        response = result.content if hasattr(result, "content") else result

        assert response.is_success is True
        assert response.error_details is None
        assert response.tool_output is not None
        # TODO: tool_output의 실제 필드를 검증하는 assert를 추가하세요.


def test_my_tool_network_error() -> None:
    """네트워크 오류 시 is_success=False, error_details에 원인이 담긴다."""
    with patch("my_tool.requests.get") as mock_get:
        mock_get.side_effect = requests_lib.exceptions.ConnectionError("연결 실패")

        result = my_tool(query="테스트 질문")
        response = result.content if hasattr(result, "content") else result

        assert response.is_success is False
        assert response.tool_output is None
        assert response.error_details is not None
