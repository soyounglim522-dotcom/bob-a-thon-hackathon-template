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
5. `bash setup/scripts/deploy.sh ...` 로 배포 (`deploy.sh`가 `.env`를 자동 로드)

## 템플릿 복사 후 반드시 바꿔야 하는 항목

- [`wxo-agent/my-wxo-agent/tools/my_tool.py`](tools/my_tool.py): 파일명
- [`my_tool_function_name()`](tools/my_tool.py:77): `@tool` 함수명
- [`app_id="my_app"`](tools/my_tool.py:62): connection 식별자
- [`wxo-agent/my-wxo-agent/agents/my_agent.yaml`](agents/my_agent.yaml): agent `name:`
- [`wxo-agent/my-wxo-agent/agents/my_agent.yaml`](agents/my_agent.yaml): agent `tools:` 리스트 항목

위 다섯 항목이 서로 맞지 않으면 import는 되어도 tool 호출이 실패하거나, 배포 시 `--app-id` 관련 오류가 발생할 수 있습니다.

## Connection / app-id가 필요한 경우

- 외부 API 인증이나 비밀값이 필요한 tool이면 connection YAML과 `--app-id`가 필요합니다.
- tool에 [`ExpectedCredentials`](tools/my_tool.py:61)가 선언되어 있으면 배포 시 `--app-id`를 함께 넘겨야 합니다.
- 단순 로직이거나 외부 인증이 필요 없는 tool이면 connection 없이 시작해도 됩니다.

예시:

```bash
# connection 없는 경우
bash setup/scripts/deploy.sh \
  --tool wxo-agent/my-wxo-agent/tools/my_tool.py \
  --agent wxo-agent/my-wxo-agent/agents/my_agent.yaml

# connection 있는 경우
bash setup/scripts/deploy.sh \
  --connection wxo-agent/my-wxo-agent/connections/my_app.yaml \
  --tool wxo-agent/my-wxo-agent/tools/my_tool.py \
  --app-id my_app \
  --agent wxo-agent/my-wxo-agent/agents/my_agent.yaml
```

## 자주 헷갈리는 부분

- `The tool '...' requires an app-id '...'` 오류가 나면: tool이 connection을 요구하는 상태이므로 `--app-id`를 추가하세요.
- 템플릿을 복사한 뒤에는 파일명, `@tool` 함수명, agent YAML의 `tools:` 문자열을 반드시 서로 맞추세요.
- 처음 실습이라면 connection 없는 단일 tool + 단일 collaborator agent부터 시작하는 것이 가장 쉽습니다.

## 참고 자료

- 템플릿: [`skills/wxo-adk-agent/references/`](../skills/wxo-adk-agent/references/)
- 예제: [`skills/wxo-adk-agent/examples/`](../skills/wxo-adk-agent/examples/)
- 배포 가이드: [`skills/wxo-adk-agent/references/deploy_recipe.md`](../skills/wxo-adk-agent/references/deploy_recipe.md)
- 원격 환경 설정: [`skills/wxo-adk-agent/references/remote_setup.md`](../skills/wxo-adk-agent/references/remote_setup.md)
- 함정 목록: [`skills/wxo-adk-agent/references/pitfalls.md`](../skills/wxo-adk-agent/references/pitfalls.md)
