# 팀 wxo Agent 작업 폴더

이 폴더에 팀의 wxo Agent 코드를 작성하세요.

## 디렉토리 구조

```
my-wxo-agent/
  agents/
    my_agent.yaml        ← Agent 정의 (name: my_agent)
  tools/
    my_tool.py           ← @tool 함수 (def my_tool)
  connections/           ← 외부 API 인증이 필요한 경우
  tests/                 ← pytest 테스트 케이스
  .env                   ← setup/.env.example 복사 후 실제 값 입력
```

## 가장 중요한 규칙

**파일명 stem == `@tool` 함수명 == agent YAML `name:` == `tools:` 리스트 항목**

```
tools/my_tool.py       ← 파일명 stem: my_tool
  └─ def my_tool(...)  ← @tool 함수명: my_tool
agents/my_agent.yaml
  ├─ name: my_agent
  └─ tools: [my_tool]  ← 정확히 일치
```

이 세 곳이 일치하지 않으면 tool이 silently 동작하지 않습니다.

## 시작하기

### 1. 환경 변수 설정

```bash
cp setup/.env.example wxo-agent/my-wxo-agent/.env
# .env 파일을 열어 WO_INSTANCE_URL, WO_INSTANCE_API_KEY 실제 값 입력
```

### 2. Agent 개발

Bob에게 자연어로 요청하는 것이 가장 빠릅니다.

```
"wxo-agent/my-wxo-agent 폴더에 날씨를 조회하는 agent를 만들어줘"
```

직접 작성할 경우:
- [`tools/my_tool.py`](tools/my_tool.py) — `@tool` 함수를 실제 로직으로 교체
- [`agents/my_agent.yaml`](agents/my_agent.yaml) — `description`, `instructions` 수정

### 3. 배포

```bash
# deploy.sh가 .env를 자동 로드합니다 (별도 source 불필요)
bash setup/scripts/deploy.sh \
    --tool wxo-agent/my-wxo-agent/tools/my_tool.py \
    --agent wxo-agent/my-wxo-agent/agents/my_agent.yaml
```

외부 API 인증이 필요한 경우 (`ExpectedCredentials` 사용 시):

```bash
bash setup/scripts/deploy.sh \
    --connection wxo-agent/my-wxo-agent/connections/my_app.yaml \
    --tool wxo-agent/my-wxo-agent/tools/my_tool.py \
    --app-id my_app \
    --agent wxo-agent/my-wxo-agent/agents/my_agent.yaml
```

## 참고 자료

- 템플릿: [`skills/wxo-adk-agent/references/`](../skills/wxo-adk-agent/references/)
- 예제: [`skills/wxo-adk-agent/examples/`](../skills/wxo-adk-agent/examples/)
- 배포 가이드: [`skills/wxo-adk-agent/references/deploy_recipe.md`](../skills/wxo-adk-agent/references/deploy_recipe.md)
- 흔한 실수 정리: [`skills/wxo-adk-agent/references/pitfalls.md`](../skills/wxo-adk-agent/references/pitfalls.md)
