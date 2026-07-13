# 아키텍처 설계 (Architecture Design)

## 1. 전체 시스템 구성도

> 아키텍처 다이어그램 이미지를 아래에 첨부해 주세요.
> 파일은 `docs/architecture-diagram.png` (또는 `.svg`, `.drawio`) 로 저장하고, 아래 주석을 해제하세요.

<!-- ![Architecture Diagram](./architecture-diagram.png) -->

---

## 2. 구성 요소 설명 (Components)

### Bob (AI Assistant)
- **역할**: 사용자와의 대화 인터페이스, wxo Agent 호출, Instana 연동 자동화
- **연동 방식**: (MCP / API 등 사용한 방식 기술)

### watsonx Orchestrate (wxo) Agent
- **역할**: (Agent가 수행하는 업무 설명)
- **구성 Agent, Tool, Knowledge Base, Connection 등 목록**:
  - Agent 1: (이름 및 기능)
  - Agent 2: (이름 및 기능)
- **트리거 조건**: (어떤 상황에서 Agent가 호출되는지)

### Instana 대시보드
- **역할**: (모니터링 대상 및 목적)
- **사용한 MCP Tool**:
  - 지표 1: (이름 및 의미)
  - 지표 2: (이름 및 의미)

### 소개 웹페이지 _(선택)_
- **역할**: 팀 결과물 시각적 소개
- **구현 방식**: Bob으로 생성한 HTML 단일 페이지

---

## 3. 데이터 흐름 (Data Flow)

```
1. 사용자가 Bob에게 질문/요청
2. Bob이 wxo Agent를 호출
3. wxo Agent가 Skill을 실행하여 결과 반환
4. Bob이 결과를 사용자에게 전달
5. (필요 시) Instana에서 관련 지표 대시보드 조회
```

> 실제 팀 시나리오에 맞게 위 흐름을 수정해 주세요.

---

## 4. 기술 스택 (Tech Stack)

| 구분 | 기술 |
|---|---|
| AI Assistant | IBM Bob |
| Agent Platform | watsonx Orchestrate |
| 모니터링 | IBM Instana |
| 프론트엔드 | HTML / CSS (선택) |

---

## 5. 설계 시 고려사항 및 의사결정 (Design Decisions)

> 아키텍처를 설계하면서 고민한 점, 선택한 이유, 트레이드오프 등을 자유롭게 작성해 주세요.

- **결정 1**: (예: Skill을 단일 Agent에 모은 이유)
- **결정 2**: (예: 특정 Instana 지표를 선택한 이유)

---

## 6. 고객에게 제안할 포인트

> 만들어낸 wxo와 Instana를 바탕으로 어떤식으로 고객에게 어필, 피칭할 것인지

- **결정 1**: (예: Skill을 단일 Agent에 모은 이유)
- **결정 2**: (예: 특정 Instana 지표를 선택한 이유)
