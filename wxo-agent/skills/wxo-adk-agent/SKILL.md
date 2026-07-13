---
name: wxo-adk-agent
description: Build and deploy a watsonx Orchestrate ADK native agent — Python @tool functions, agent YAML (collaborator or manager), connection configs, and shipping via the `orchestrate` CLI directly to a hosted Orchestrate instance (no local Docker server required). Use when the user mentions watsonx Orchestrate, wxo, WXO, Orchestrate ADK, ADK tool, ADK agent, collaborator agent, manager agent, @tool decorator, ToolResponse, agents import, tools import, env add, env activate, draft vs live, or a hackathon agent.
---

# Building a watsonx Orchestrate enterprise agent

You are helping the user build and deploy a native ADK agent for IBM watsonx
Orchestrate. The agent is composed of three primitives: **tools** (Python
functions), **agents** (YAML), and **connections** (YAML). You will author each
locally, run unit tests with `pytest`, then push the artifacts straight to a
shared hosted Orchestrate instance with the `orchestrate` CLI. No local Docker
server, no Lite stack — the CLI talks directly to the hosted instance.

## When this skill applies

- "Build me a watsonx Orchestrate agent that …"
- "Write an ADK tool for …"
- "I need a manager + collaborator setup for …"
- "How do I deploy this to Orchestrate?"
- Anything mentioning `@tool`, `ToolResponse`, `agents import`, Draft/Live connections, or `groq/openai/gpt-oss-120b`.

## Pick a target

If the user hasn't said what they're building, suggest one of these. Start with
**Tier 1** unless they explicitly want more.

### Tier 1 — Single-tool collaborator (≈ 2 hours)
1. **PTO balance lookup** (HR). One tool against a mock HR endpoint or a tiny FastAPI stub.
2. **GitHub PR digest** (dev tools). `list_open_prs(username)` against the GitHub REST API — free tokens, no enterprise auth.
3. **Next meeting** (Productivity). Google Calendar or a Notion DB stand-in.
4. **Expense lookup** (Finance). Mock Concur/SAP endpoint.
5. **Weather-aware travel reminder** (the fun one). OpenWeather — pure focus on instruction-writing.

### Tier 2 — Multi-tool collaborator (≈ half day)
6. **IT helpdesk ticket assistant**: `search_kb` → `create_ticket` → `get_ticket_status`.
7. **Sales lead enricher**: `lookup_account` → `get_recent_news` → `summarize_account`.
8. **Procurement RFP tracker**: `list_open_rfps` → `get_rfp_details` → `check_approval_status`.
9. **Document summarizer**: `list_documents` → `get_document_text` → `summarize` (Box / Drive / Dropbox).

### Tier 3 — Manager + collaborators (full day)
10. **Employee onboarding orchestrator**: HR manager → `hr_records_agent`, `it_provisioning_agent`, `facilities_agent`.
11. **Customer support triage**: support manager → `refund_agent`, `shipping_agent`, `kb_agent`.
12. **Finance close assistant**: finance manager → `journal_entries_agent`, `reconciliation_agent`, `variance_explainer_agent`.

## Workflow

1. **Write code locally** — `@tool` functions in `tools/`, agent specs in `agents/`, connection configs in `connections/`.
2. **Test with `pytest`** — `pytest tools/` exercises the tool's HTTP logic against mocks.
3. **`orchestrate env list`** before every import — confirm the hosted env is the active one.
4. **Import → hosted instance** — `connections add` → `tools import` → `agents import`, in that order.
5. **Test in the hosted chat UI**.

## Mental model

- **Tool** = a Python `@tool`-decorated function. The decorator's docstring is what the agent's LLM reads to decide whether to call it.
- **Agent** = a YAML spec with a `name`, an `llm`, `instructions`, a list of `tools` (function-name strings), and a list of `collaborators` (other agents).
- **Connection** = a YAML config naming an `app_id` and an auth kind.
- **Manager vs collaborator** = pure-router vs worker. Managers have empty `tools:` and a non-empty `collaborators:`. Collaborators are the opposite.
- **Draft vs Live** = the hosted instance keeps two credential slots per connection.

## Recommended project layout

**Filename stem == `@tool` function name == agent YAML `name:` == string in `tools:`.**

```
my-wxo-agent/
  agents/my_agent.yaml          # name: my_agent
  tools/my_tool.py              # def my_tool(...)
  tools/my_tool_test.py
  connections/my_app.yaml       # app_id: my_app
  .env                          # copy from setup/.env.example
  requirements.txt
```

## Reference files

- `references/tool_template.py` — runnable `@tool` skeleton with `ToolResponse`/`ErrorDetails` inlined.
- `references/tool_test_template.py` — pytest happy + error path templates.
- `references/agent_collaborator.yaml` — worker agent template.
- `references/agent_manager.yaml` — router agent template.
- `references/connection_basic_auth.yaml` — `key_value` and `basic` auth configs.
- `references/connection_oauth.yaml` — `oauth_auth_code_flow` config.
- `references/yaml_schema.md` — full field-by-field schema for agents and connections.
- `references/deploy_recipe.md` — end-to-end commands for the hosted instance.
- `references/remote_setup.md` — one-time hosted instance registration + Draft → Live promotion.
- `references/evaluation_template.json` — Journey Success test case skeleton.
- `references/evaluation_recipe.md` — upload helper, grading rules, common failures.
- `references/pitfalls.md` — eight traps with wrong vs right code.

## Examples

Working end-to-end examples live in `examples/`. Each sub-directory is a
self-contained project you can study, copy, or deploy as-is.

| Directory | Pattern | What it shows |
|---|---|---|
| `examples/personal_banking/` | Multi-tool collaborator | `list_accounts`, `transfer_money`, `get_contact`, `change_contact` |
| `examples/customer_care/` | Manager + two collaborators | Separate `customer_care` and `servicenow` tool packages |
| `examples/customer_care_planner/` | Planner-style agent | Same domain as `customer_care` but uses the `planner` style |
| `examples/healthcare_provider/` | OpenAPI tool (no Python) | Imports a pre-built OpenAPI spec directly |
| `examples/ibm_knowledge/` | Knowledge-base agent | Pairs a `stock_price` tool with a vector knowledge base |
| `examples/agentic_memory/` | Agentic memory / ticket creation | Minimal structure, great for learning the shape |
| `examples/voice_enabled_elevenlabs/` | Voice channel | Shows how to attach an ElevenLabs TTS voice config |

## Common pitfalls (one-line each)

Full wrong/right examples in `references/pitfalls.md`.

1. **`tools:` strings drift from function names** — keep the three-way match.
2. **Manager with a non-empty `tools:`** — managers route only; always `tools: []`.
3. **Missing Google docstring** — every arg under `Args:`, plus `Returns:`.
4. **Raising in a `@tool`** — always return `ToolResponse` with `error_details`.
5. **LLM string typos** — stick to `groq/openai/gpt-oss-120b`.
6. **Wrong import order** — connections → tools → agents.
7. **Forgetting `orchestrate env list` before every import**.
8. **`Scope not found` on env activate** — wrong `--iam-url` for the instance tier.
