# 팀명 (Team Name)

> **IBM Korea Bob-a-thon** — 팀 결과물 제출 레포지토리
>
> 이 레포는 **팀 결과물 제출용 템플릿**이면서, 동시에 참가자가 직접 **watsonx Orchestrate Agent**와 **Instana 대시보드**를 Bob과 함께 만들 수 있도록 가이드와 템플릿을 함께 포함합니다.
>
> 오전·오후 세션 순서대로 진행하세요.
>
> | 세션 | 시간 | 목표 | 시작 가이드 |
> |---|---|---|---|
> | **세션 1** | 오전 | Bob ↔ watsonx Orchestrate Agent | [`wxo-agent/my-wxo-agent/README.md`](wxo-agent/my-wxo-agent/README.md) |
> | **세션 2** | 오후 | Bob ↔ Instana 대시보드 | [`instana-dashboard/README.md`](instana-dashboard/README.md) |

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

## 세션 1 (오전) — Bob ↔ watsonx Orchestrate Agent

### 0. 사전 준비 — `uv` 설치

```bash
# uv가 없는 경우 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. 의존성 설치 및 환경 변수 설정

```bash
# 레포 루트에서 실행
cd setup
uv sync
cd ..

# 환경 변수 파일 복사 후 실제 값 입력
cp setup/.env.example wxo-agent/my-wxo-agent/.env
# .env 파일을 열어 WO_INSTANCE_URL, WO_INSTANCE_API_KEY 등 실제 값 입력
```

### 2. Bob에 wxo MCP 서버 등록

Bob 설정 창(MCP Servers)에 아래 내용을 추가하세요. 동일한 내용이 `setup/mcp/mcp.json`에도 있습니다.

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

> ✅ 등록 후 Bob에게 `"list agents"` 라고 입력해 watsonx Orchestrate에 연결됐는지 확인하세요.

### 3. wxo Agent 개발

Bob에게 직접 Agent 작성을 요청하는 것을 권장합니다.
Bob은 [`wxo-agent/skills/wxo-adk-agent/SKILL.md`](wxo-agent/skills/wxo-adk-agent/SKILL.md)의 가이드를 참고해 tool · agent 파일을 생성하고 배포까지 도와줍니다.

```
"wxo-agent/my-wxo-agent 폴더에 [원하는 기능]을 하는 agent를 만들고 watsonx Orchestrate에 업로드해줘"
```

직접 작성하려면 아래 참고 문서를 확인하세요.

> 📖 상세 가이드:
> - 작업 폴더 안내: [`wxo-agent/my-wxo-agent/README.md`](wxo-agent/my-wxo-agent/README.md)
> - 배포 절차: [`wxo-agent/skills/wxo-adk-agent/references/deploy_recipe.md`](wxo-agent/skills/wxo-adk-agent/references/deploy_recipe.md)
> - 흔한 실수 정리: [`wxo-agent/skills/wxo-adk-agent/references/pitfalls.md`](wxo-agent/skills/wxo-adk-agent/references/pitfalls.md)

---

## 세션 2 (오후) — Bob ↔ Instana 대시보드
Bob에 Instana MCP 서버를 등록하면, Bob이 Instana API를 직접 호출해 데이터를 조회·분석하거나 대시보드를 생성할 수 있습니다.

### 1. Instana API 토큰 발급

Instana 웹 콘솔 → **Settings → User settings → Personal API Tokens → New Personal API Token**에서 토큰을 발급합니다.

| 권한 | 필요 여부 |
|---|---|
| Read configuration | 필수 |
| Access infrastructure and platform data | 필수 |
| Read application monitoring | 권장 |
| Read custom dashboards | 권장 |

### 2. Bob에 Instana MCP 서버 등록

> ⚠️ **사전 준비 (최초 1회만)**
> 이 데모 서버(`demo-instana.automation.ibmce-kr.com`)는 자체 서명(self-signed) 인증서를 사용합니다. 아래 준비 없이 바로 등록하면 `SSLCertVerificationError` / `certificate verify failed` 오류가 발생합니다.
>
> 터미널(macOS/Linux, Windows는 WSL 또는 Git Bash)에서 아래 3줄을 그대로 복사해서 실행하세요.
>
> ```bash
> # 1) 서버 인증서 추출
> openssl s_client -connect demo-instana.automation.ibmce-kr.com:443 \
>   -servername demo-instana.automation.ibmce-kr.com </dev/null 2>/dev/null \
>   | openssl x509 -outform PEM > instana-selfsigned.pem
>
> # 2) 인증서 패키지 준비 (이미 설치돼 있다면 생략 가능)
> pip3 install certifi --break-system-packages
>
> # 3) 공인 인증서 목록 + 이 서버 인증서를 합쳐서 하나의 파일로 생성
> cat "$(python3 -c 'import certifi; print(certifi.where())')" instana-selfsigned.pem > combined-ca.pem
> ```
>
> 실행 후 `pwd` 명령으로 현재 폴더의 **절대 경로**를 확인해두세요. (예: `/Users/hong/hackathon-repo`) 아래 설정의 `<combined-ca.pem-절대경로>` 자리에 `그 경로/combined-ca.pem`을 넣으면 됩니다.

Bob 설정 창(MCP Servers)에 아래 내용을 추가하세요.

```json
{
  "mcpServers": {
    "instana": {
      "command": "uvx",
      "args": [
        "mcp-instana==0.9.9",
        "--transport",
        "stdio"
      ],
      "env": {
        "INSTANA_BASE_URL": "https://demo-instana.automation.ibmce-kr.com",
        "INSTANA_API_TOKEN": "<your-api-token>",
        "SSL_CERT_FILE": "<combined-ca.pem-절대경로>",
        "REQUESTS_CA_BUNDLE": "<combined-ca.pem-절대경로>"
      }
    }
  }
}
```

> `INSTANA_API_TOKEN`과 `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE` 값만 본인 환경에 맞게 교체하세요. 등록 후에는 **Bob을 완전히 종료했다가 다시 실행**해야 설정이 반영됩니다.

### 3. 연결 확인

Bob에게 아래와 같이 입력해 Instana 데이터가 정상적으로 응답되는지 확인하세요.

```
"Instana에서 현재 인프라 호스트 목록을 가져와줘"
"Instana에서 최근 1시간의 서비스별 응답 시간을 요약해줘"
```

### 4. Bob에게 대시보드 생성 요청

연결이 확인되면 아이디어를 자연어로 바로 요청하면 됩니다.

```
"Instana 데이터를 바탕으로 서비스 응답 시간과 에러율을 보여주는 대시보드를 만들어줘"
"Instana에서 CPU 사용률 상위 5개 호스트를 뽑아 HTML 대시보드로 시각화해줘"
"Instana 알림 이벤트를 기반으로 장애 현황 요약 페이지를 만들어줘"
```

### 아이디어 예시

| # | 아이디어 | Bob 요청 예시 |
|---|---|---|
| 1 | 서비스 상태 요약 대시보드 | "서비스별 응답 시간·에러율을 한눈에 볼 수 있는 HTML 대시보드를 만들어줘" |
| 2 | 인프라 리소스 Top-N 분석 | "CPU·메모리 사용률 상위 5개 호스트를 테이블로 정리해줘" |
| 3 | 배포 전후 성능 비교 | "특정 서비스의 배포 전후 P99 응답 시간을 Instana에서 비교해줘" |
| 4 | SLO 달성률 보고서 | "지난 7일간 서비스 가용성(SLO)을 집계해 요약 보고서를 만들어줘" |
| 5 | 이상 감지 알림 요약 | "최근 발생한 Instana 이벤트를 심각도별로 분류해 정리해줘" |
| 6 | 장애 타임라인 시각화 | "최근 인시던트를 타임라인 형태의 HTML 페이지로 시각화해줘" |

---

## 아키텍처 요약 (Architecture Summary)

> 전체 시스템 구성을 간략히 설명해 주세요.
> 상세 내용은 [docs/architecture.md](docs/architecture.md) 를 참고하세요.

```
세션 1 (오전):  [참가자] → [Bob] ── MCP(adk) ─────→ [watsonx Orchestrate]  →  wxo Agent 배포·관리
세션 2 (오후):  [참가자] → [Bob] ── MCP(instana) ──→ [Instana API]          →  대시보드·분석 결과 생성
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
│   │   ├── tests/                     ← pytest 테스트 케이스
│   │   ├── requirements.txt           ← 툴 외부 패키지 목록
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
│   │   └── mcp.json                   ← Bob MCP 서버 설정 (wxo ADK)
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
