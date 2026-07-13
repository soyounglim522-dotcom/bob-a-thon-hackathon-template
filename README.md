# 팀명 (Team Name)

> **IBM Korea Bob-a-thon** — 팀 결과물 제출 레포지토리

---

## 팀원 (Team Members)

| 이름 | 역할 |
|---|---|
| 홍길동 | wxo Agent 설계 |
| 김철수 | Instana 대시보드 구성 |
| 이영희 | 소개 웹페이지 제작 |

---

## 프로젝트 개요 (Project Overview)

> 한 문단으로 팀의 프로젝트를 설명해 주세요.
> 어떤 문제를 해결하고자 했는지, 어떤 기술을 활용했는지 작성해 주세요.

---

## 빠른 시작 (Quick Start)

### 0. 사전 준비 — `uv` 설치

```bash
# uv가 없는 경우 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. 의존성 설치 및 환경 변수 설정

```bash
# 레포 루트에서 실행 — pyproject.toml이 setup/ 안에 있으므로 setup/ 에서 설치
cd setup
uv sync
cd ..

# 환경 변수 파일 복사 후 실제 값 입력
cp setup/.env.example wxo-agent/my-wxo-agent/.env
# .env 파일을 열어 WO_INSTANCE_URL, WO_INSTANCE_API_KEY 등 실제 값 입력
```

### 2. Bob에 MCP 서버 등록 (wxo 연동)

Bob의 MCP 설정에 `setup/mcp/mcp.json` 내용을 추가하세요.

```json
{
  "mcpServers": {
    "adk": {
      "command": "uvx",
      "args": ["ibm-watsonx-orchestrate-mcp-server"]
    }
  }
}
```

### 3. wxo Agent 개발

```bash
# ※ 모든 명령은 레포 루트에서 실행

# 하위 디렉토리 생성
mkdir -p wxo-agent/my-wxo-agent/{agents,tools,connections,tests}

# 툴 / 에이전트 템플릿 복사 후 수정
cp wxo-agent/skills/wxo-adk-agent/references/tool_template.py \
   wxo-agent/my-wxo-agent/tools/my_tool.py
cp wxo-agent/skills/wxo-adk-agent/references/agent_collaborator.yaml \
   wxo-agent/my-wxo-agent/agents/my_agent.yaml

# 로컬 테스트 (테스트 파일이 없으면 "no tests ran" 정상)
uv run --project setup pytest wxo-agent/my-wxo-agent/tools/ || true

# 배포
source wxo-agent/my-wxo-agent/.env
bash setup/scripts/deploy.sh \
    --tool wxo-agent/my-wxo-agent/tools/my_tool.py \
    --agent wxo-agent/my-wxo-agent/agents/my_agent.yaml
```

> 📖 상세 가이드: [`wxo-agent/skills/wxo-adk-agent/references/deploy_recipe.md`](wxo-agent/skills/wxo-adk-agent/references/deploy_recipe.md)

---

## 아키텍처 요약 (Architecture Summary)

> 전체 시스템 구성을 간략히 설명해 주세요.
> 상세 내용은 [docs/architecture.md](docs/architecture.md) 를 참고하세요.

```
[사용자] → [Bob] → [wxo Agent] → [watsonx Orchestrate]
                 ↘ [Instana 대시보드]
```

---

## 구현 결과 (Implementation Results)

### 1. wxo Agent

- **기능 설명**: (어떤 기능을 하는 Agent인지 작성)
- **활용 Skill**: (사용한 Skill 목록)
- **스크린샷**: [`wxo-agent/screenshots/`](wxo-agent/screenshots/)

### 2. Instana 대시보드

- **대시보드 구성**: (어떤 지표를 모니터링하는지 작성)
- **스크린샷**: [`instana-dashboard/screenshots/`](instana-dashboard/screenshots/)

### 3. 소개 웹페이지 _(선택)_

- **URL / 파일**: [`showcase-page/index.html`](showcase-page/index.html)
- **설명**: (웹페이지에서 소개하는 내용 작성)

---

## 테스트 결과 요약 (Test Summary)

> 상세 테스트 계획 및 수행 결과는 [docs/test-plan.md](docs/test-plan.md) 를 참고하세요.

| 항목 | 결과 |
|---|---|
| wxo Agent 응답 정확도 | ✅ / ❌ |
| Instana 대시보드 데이터 반영 | ✅ / ❌ |
| 소개 웹페이지 정상 렌더링 | ✅ / ❌ |

---

## 레포지토리 구조 (Repository Structure)

```
.
├── README.md                          ← 이 파일
├── docs/
│   ├── architecture.md                ← 아키텍처 설계 문서
│   └── test-plan.md                   ← 테스트 계획 및 결과
│
├── wxo-agent/
│   ├── README.md                      ← Agent 설명
│   ├── screenshots/                   ← Agent 동작 스크린샷
│   ├── my-wxo-agent/                  ← 팀 Agent 코드 작업 폴더
│   │   ├── agents/                    ← Agent YAML 파일
│   │   ├── tools/                     ← @tool Python 파일
│   │   ├── connections/               ← Connection YAML 파일
│   │   └── .env                       ← 환경변수 (setup/.env.example 복사)
│   └── skills/
│       └── wxo-adk-agent/
│           ├── SKILL.md               ← Bob에게 wxo 빌드 방법 가이드
│           ├── references/            ← 템플릿 파일 (tool, agent, connection, ...)
│           └── examples/              ← 예제 프로젝트 목록
│
├── instana-dashboard/
│   ├── README.md                      ← 대시보드 설명
│   └── screenshots/                   ← 대시보드 스크린샷
│
├── showcase-page/
│   └── index.html                     ← 소개 웹페이지 (선택)
│
├── setup/                             ← wxo 연동 인프라 (수정 불필요)
│   ├── .env.example                   ← 환경변수 템플릿
│   ├── .python-version                ← Python 3.13
│   ├── pyproject.toml                 ← 의존성 (ibm-watsonx-orchestrate 등)
│   ├── AGENTS.md                      ← Bob 작업 가이드
│   ├── mcp/
│   │   └── mcp.json                   ← Bob MCP 서버 설정
│   └── scripts/
│       └── deploy.sh                  ← 자동 배포 스크립트
│
└── .github/
    └── pull_request_template.md       ← 제출 체크리스트
```

---

## 제출 체크리스트 (Submission Checklist)

- [ ] `docs/architecture.md` 작성 완료
- [ ] `docs/architecture-diagram.*` 다이어그램 파일 업로드
- [ ] `docs/test-plan.md` 작성 완료
- [ ] `wxo-agent/screenshots/` 스크린샷 업로드
- [ ] `instana-dashboard/screenshots/` 스크린샷 업로드
- [ ] _(선택)_ `showcase-page/index.html` 작성 완료
