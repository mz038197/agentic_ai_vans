# Handoff: 南一中課程 × 神通 Agent Builder（接續）

Date: 2026-09-06
Workspace: `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans`
Git branch: `feat/mitac-agent-builder-api`（可與 origin 同步；勿擅自 commit／push）
Prior Mitac API handoff (still valid for REST facts): `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans\handoff-mitac-agent-builder-api.md`

## Goal for the next session

Continue **course design** for 南一中 Agent 課，runtime 以神通為主；不要把 VS Code + Vans Router 的 coding 展示用神通換掉。若使用者要實作，才打神通 API 或寫 Router／`main_mitac.py`。

Working teaching doc（可改）：`南一中-Agent課程-12堂.md`  
Contour doc（**不要改**，使用者已要求還原並維持）：`南一中-Agent課程規劃.md`

## What this conversation decided

### 神通 API（能力，細節見舊 handoff）

- 產品是 Google ADK 多代理人後端。資源樹：Space → App → Agent／Session；另有 Provider、MCP、API Server、Folder/File、Extension。
- 學生產品接神通的契約：login + session + `run_sse`。組裝用其他章。
- 工具兩條路：登記 MCP URL，或 API Server + Call API Tool／OpenAPI。執行在神通，檔案寫在 MCP process 所在機器。神通連的是填進去的 URL，不是學生 localhost。
- Artifact 要另 GET + URL-safe base64；不會自動進 LINE。
- **沒有 Skill 一級功能**（1.2.2 手冊無 `skill`）。接近物：instruction、MCP／REST、RAG、template。Cursor／Claude `SKILL.md` 神通吃不到。
- 文件 1.2.2 vs live `micore-backend` 1.4.0：以 live 為準。Base：`http://172.16.36.62/api/v1`。VPN：FortiClient。Token 不落檔。練習用 space 2「Vans測試」。勿動 ESG／創新AI／Vietnam／sharon。
- 勿發明 client library，除非使用者要求。

### 南一中課：角色定義（寫在 12 堂檔）

- **Agent User**：用現成 Agent，不改。僅第 1 堂。I can use an Agent.
- **Agent Builder**：改神通上的 Agent（身份、老師掛好的工具、Session、instruction 步驟）。第 2–5 堂。I can build an Agent。**不開 VS Code 當主場。**
- **AI Coder**：用 AI 寫學生電腦上的軟體；神通 App 是被接上的元件。第 6–7 堂。I can build software with AI。
- **Product Builder**：第 8–12 堂（含原 Project Team）。

### 神通 Builder 天花板（第 5 堂結束）

一支單一神通 Agent：自己的 instruction、會呼叫老師先掛的 1–2 個工具、Session＝短期記憶、步驟寫在 instruction。  
不含：自寫 MCP／API Server、`run_sse` 客戶端、VS Code、網頁、自己的 DB／RAG、Multi-Agent。

舊版 `南一中-Agent課程規劃.md` 是「從零爬到 Router coding」一條坡。新版在第 5 堂切斷；coding 是下一角色，不是 Builder 終點。

### Router 兩個入口（不要混）

1. VS Code MCP：coding 夥伴；可代操神通組裝。**這步不能被神通取代**（神通看不到學生 repo）。
2. HTTP：學生產品 → Router → `run_sse`。

學生各有神通帳號。Router 用 login + 連線記憶體 + refresh，不要存全班 access_token。`run_sse` 會覆寫 `user_id`。

### 第 1 堂（兩小時）草案

全程神通，含「只會聊」對照也用沒掛工具的神通 Agent，不要 ChatGPT vs 神通。

- 0:00–0:15 只會回話的 Agent（登記教室做不成）
- 0:15–0:45 會行動的現成 App，走完一輪
- 0:45–1:05 老師切兩套身份、同一道陷阱題，學生只填對照表（不進後台）
- 1:05–1:45 Idea Bank：誰／痛點／判斷／用完缺什麼，至少 3 則
- 1:45–2:00 抽講；作業補到 5 則

Idea Bank＝題目清單，不是系統。

### 實作狀態

- 未做 `main_mitac.py`、未做 Router MCP 包神通。
- `main.py` 仍是 Dungeon 通關成品（本機 ChatOpenAI + tools）。內有寫死金鑰，handoff 不抄。
- API 曾通：`GET /api/v1/version` → 1.4.0。本 session **未再 login**。

## Do not

- 改 `南一中-Agent課程規劃.md`（使用者明確禁止）。
- 把 VPN／UI／JWT／`main.py` 金鑰寫進 repo 或 handoff。
- Commit／push 除非使用者要求。
- 更新 wiki／`wiki/index.md`。
- 在學生網站裡再做一套 `ChatOpenAI` + 本機 tool loop。
- 第 5 堂上 Multi-Agent；第 3 堂讓學生自架 MCP 或填 API Server 表格。

## Resume checklist

1. 讀 `南一中-Agent課程-12堂.md`（定義 + 12 堂表 + Builder 天花板）。
2. 需要 REST 細節時讀 workspace 內 `handoff-mitac-agent-builder-api.md` 與 `C:\Users\mz038\Desktop\MitacAgentBuilder-API-docs-v1.2.2\`。
3. 問使用者下一刀：第 1 堂任務單、Router 最小工具清單、還是 space 2 實打 API。
4. 打 API 先 ping version；要 token 再向使用者要帳密，不落盤。

## Suggested skills

- `handoff`：若本線再拆對話。
- `python-cli-from-template`：使用者要最小神通 CLI／`main_mitac.py` 時。
- `agents-md-guide`／`writing-for-agents`：Router MCP 或 AGENTS.md 要寫組裝順序時。
- `user-md-guide`：這條 branch 的帶班／API 流程要進 USER.md 時。
- `playwright-cli`／`chrome-devtools`：只有回頭用神通網頁 UI 時；預設走 API。

不要套用 CoreLab／Gamma／quiz-template／exam-OCR，除非使用者換題。
