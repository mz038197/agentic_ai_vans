# Handoff: Mitac Agent Builder API → agentic_ai_vans

Date: 2026-09-05
Prior chat workspace: `C:\Users\mz038\Desktop\temp`
Continue in: `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans`
Git branch (local only): `feat/mitac-agent-builder-api` (created from `master` @ `7b047de`)

## Goal for the next session

Keep teaching / driving the Mitac Agent Builder **REST API** (not the web UI), then implement whatever the user wants **inside `agentic_ai_vans`**. They already said they want API, and asked the agent to fire the calls for them. They also asked to move this work into the vans project and carry this session over.

Do not invent a client library until they ask. Next useful API step they left open: inspect space `2` (`Vans測試`) providers / apps / agents, then follow docs Ch.2 steps 4–9 (Space already exists → provider → agent → app → session → `run_sse`).

## What this project is

`agentic_ai_vans` is the classroom reference agent (Agent Dungeon / Shell Agent). See `CONTEXT.md`. Root `main.py` is the finished CLI agent; `main_shell.py` is the Shell template. Unrelated to Mitac until this branch.

## Docs vs live API

- Offline HTML manual (v1.2.2): `C:\Users\mz038\Desktop\MitacAgentBuilder-API-docs-v1.2.2\index.html`
- Can serve with `py -3 -m http.server 8080` from that folder → `http://localhost:8080`
- Manual examples use `http://localhost:5011`. **This user’s base URL is `http://172.16.36.62`** (also works as `http://172.16.36.62:5011`). All paths under `/api/v1`.
- Live product: `GET /api/v1/version` → `micore-backend` **1.4.0** (newer than the 1.2.2 manual). Prefer live responses when they disagree.
- Auth: JWT `Authorization: Bearer <access_token>` except public login/register/version.
- Roles: USER(5) < MANAGER(10) < ADMIN(15) < SUPER_ADMIN(20). Creating a Space needs Super Admin.

Resource tree: Space → App → Agent / Session; also Provider, MCP, API Server, Folder/File, Extension.

## Access (redacted)

Two separate logins. **Do not put secrets in repo or this file.** User has them in chat history; ask the user if you need them again.

1. **FortiClient SSL-VPN** (only if `172.16.36.62` is unreachable)
   - Gateway and custom port were provided in the prior session (internal VPN).
   - FortiClient is installed: `C:\Program Files\Fortinet\FortiClient\FortiClient.exe`
2. **Agent Builder web + API**
   - UI: `http://172.16.36.62/`
   - Login: `POST /api/v1/auth/login` JSON `{email, password}`
   - User already logged into the UI successfully.

On 2026-09-05 from the previous machine, LAN to `172.16.36.62:80` was already up (VPN likely connected). Login API returned 200.

## Proven API results (no secrets)

`POST /api/v1/auth/login` → 200  
Fields: `access_token`, `refresh_token`, `token_type=bearer`, `expires_in=10800`, `user_id` present.

`GET /api/v1/users/me` → 200  
- username: Vans  
- role: 20 / `super_admin`  
- status: active  
- `joined_groups`: []  
- `default_password_check`: false  

`GET /api/v1/spaces` → 200, 8 spaces:

| id | name | default LLM |
|----|------|-------------|
| 2 | Vans測試 | none — **use this for practice** |
| 4 | 創新AI 教育空間 | none |
| 6 | ESG | none |
| 7 | test_for_sharon | none |
| 8 | Vietnam_Lesson | none |
| 1 | defaults | `gpt-oss-120b` (provider 1) |
| 3 | 艾迪訊workshop | `qwen-qwen3-5-122b-a10b-gptq` (provider 13) |
| 9 | test | none |

Earlier list of apps/agents on all spaces came back empty (`apps: []`, `agents: []`). Re-check space 2 and maybe 1/3 before creating duplicates. Do not mutate ESG / 創新AI / Vietnam / sharon spaces.

## Agent habits from this session

- User wants **step-by-step**, then switched to “you call the API”.
- **Do not persist tokens** unless they ask. Previous agent re-logged in every new Python process (token only in that process memory). Temp JSON under Desktop `temp` was deleted after read.
- Full JWT was shown once in chat when they asked where the token lives; do not repeat it into files.
- PowerShell mangles Chinese / regex: write a `.py` file or print UTF-8 to a temp file and Read it. Do not `Out-File` API JSON.
- Offline docs search works better via local HTTP than `file://`.

## First-conversation-to-SSE path (manual Ch.2)

Already done: login, `/users/me`, `/spaces`.  
Still to do if they want a talking agent via API:

1. `GET /api/v1/spaces/2` and `GET /api/v1/spaces/2/providers` (and apps/agents).
2. If no provider on space 2, copy pattern from space 1 or create provider (Ch.13) then set space default LLM.
3. Create LLM agent (Ch.12) — `name` must be a valid Python identifier.
4. Create app (Ch.11) and `attach_agent`.
5. Create session (Ch.15).
6. `POST .../run_sse` (Ch.14). Stream has `partial: true` deltas then a full `partial: false` summary; print only partials to avoid duplicate text.

## Suggested skills

- `handoff` — already used; re-run if this thread splits again.
- `python-cli-from-template` — only if they ask for a small Mitac API CLI in this repo.
- `agents-md-guide` / `writing-for-agents` — if they want AGENTS.md notes for the Mitac client.
- `playwright-cli` / `chrome-devtools` — only if they go back to the web UI; they said they want API.
- `user-md-guide` — if they want a USER.md for this branch’s workflow.

Do **not** apply CoreLab / Gamma / quiz-template / exam-OCR rules unless the user switches topics.

## Out of scope / do not do

- Commit or push unless asked. Branch is unpushed.
- Store VPN password, UI password, or JWT in git.
- Edit `wiki/index.md` or Obsidian vault for this work.
- Treat 1.2.2 HTML as newer than live 1.4.0.

## Resume checklist

1. `cd C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans` and confirm branch `feat/mitac-agent-builder-api`.
2. Confirm `http://172.16.36.62/api/v1/version` is reachable; if not, user must connect FortiClient.
3. Ask user for login if you need a token; do not scrape old chat for passwords to write to disk.
4. Ask whether next step is continue API probes on space 2, or start coding against Mitac inside this repo.
