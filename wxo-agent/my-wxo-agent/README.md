# 팀 wxo Agent 작업 폴더

이 폴더에 팀의 wxo Agent 코드를 작성하세요.

## 권장 디렉토리 구조

```
my-wxo-agent/
  agents/
    my_agent.yaml          # name: 필드 == 파일명 stem
  tools/
    my_tool.py             # @tool 함수명 == 파일명 stem
    my_tool_test.py        # 테스트 (pytest tools/)
  connections/
    my_app.yaml            # app_id == 파일명 stem
  tests/
    my_test.json           # Journey Success 테스트 케이스
  requirements.txt
  .env                     # setup/.env.example 복사 후 작성
```

## 가장 중요한 규칙 하나

**파일명 stem == `@tool` 함수명 == agent YAML `name:` == `tools:` 리스트 항목**

```
tools/get_weather.py           ← 파일명 stem
  └─ def get_weather(...)      ← @tool 함수명
agents/weather_agent.yaml
  ├─ name: weather_agent
  └─ tools: [get_weather]      ← 정확히 일치
connections/openweather.yaml
  └─ app_id: openweather
```

이 세 곳이 일치하지 않으면 tool이 silently 동작하지 않습니다 (Pitfall #1).

## 시작하기

1. `setup/.env.example` → `my-wxo-agent/.env` 로 복사 후 실제 값 채우기
2. `skills/wxo-adk-agent/references/tool_template.py` 복사 → `tools/my_tool.py` 수정
3. `skills/wxo-adk-agent/references/agent_collaborator.yaml` 복사 → `agents/my_agent.yaml` 수정
4. `pytest tools/` 로 로컬 테스트
5. `source .env && bash setup/scripts/deploy.sh ...` 로 배포

## 참고 자료

- 템플릿: [`skills/wxo-adk-agent/references/`](../skills/wxo-adk-agent/references/)
- 예제: [`skills/wxo-adk-agent/examples/`](../skills/wxo-adk-agent/examples/)
- 배포 가이드: [`skills/wxo-adk-agent/references/deploy_recipe.md`](../skills/wxo-adk-agent/references/deploy_recipe.md)
- 원격 환경 설정: [`skills/wxo-adk-agent/references/remote_setup.md`](../skills/wxo-adk-agent/references/remote_setup.md)
- 함정 목록: [`skills/wxo-adk-agent/references/pitfalls.md`](../skills/wxo-adk-agent/references/pitfalls.md)
