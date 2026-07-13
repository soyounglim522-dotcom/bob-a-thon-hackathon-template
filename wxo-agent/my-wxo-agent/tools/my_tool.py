"""
팀의 첫 번째 wxo Agent 툴.

파일명 stem(my_tool) == @tool 함수명(my_tool) == agents/my_agent.yaml의 tools: 항목
이 세 곳을 항상 동일하게 유지하세요.
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def my_tool(query: str) -> str:
    """
    사용자의 질문에 답변합니다.

    Args:
        query: 사용자가 입력한 질문 또는 검색어.

    Returns:
        질문에 대한 답변 문자열.
    """
    # TODO: 이 부분을 실제 로직으로 교체하세요.
    return f"'{query}'에 대한 결과입니다. (실제 구현으로 교체 필요)"
