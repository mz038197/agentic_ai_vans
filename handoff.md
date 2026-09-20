# Handoff：南一中 12 堂 × 神通

Date: 2026-09-20  
Workspace: `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans`  
本檔是本 repo **唯一** handoff。已刪：`handoff-nanyi-12堂-2026-09-17.md`、`handoff-nanyi-mitac-agent-course.md`、`handoff-mitac-agent-builder-api.md`。

**教案真相來源：** `南一中-Agent課程-12堂.md`（第 1–5 堂已定，細節以該檔為準，勿在此複誦全文）  
**不要改：** `南一中-Agent課程規劃.md`  
**工作區指令：** `AGENTS.md`（Cursor 會讀）

神通官方手冊（raw，不改）：`G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\Agent_Builder`  
API HTML：該資料夾下 `MitacAgentBuilder-API-docs-v1.2.2\`（Ch.11 App；Ch.12 Agent 型別；Ch.14 `run_sse`；Ch.15 Session；Ch.17 MCP；Ch.18 API Server 要 Admin；Ch.19 Call API Tool）。舊本機 `C:\Users\mz038\Desktop\MitacAgentBuilder-API-docs-v1.2.2\` 不當預設。

課堂看板 repo：[club-booking-board](https://github.com/mz038197/club-booking-board)（不在本 repo 另做一套）

---

## Goal for the next session

對齊看板與第 5 堂契約：待審、准駁、占用／海報同一站重設。老師備 RAG 資料夾與 Skill zip（表單範本在 `references`）。改課表只動 `南一中-Agent課程-12堂.md`。

---

## 已落稿（勿當未決）

- 第 1 堂角色仍是 User，本稿不寫教案。舊「第 1 堂兩小時草案」作廢。
- 第 2 堂仍是 Builder。舊第 1 堂教室登記整段當開場，再從零建 LLM。總表不要寫「使用者→Builder」。
- 第 3 堂：學生自己掛 `check_slot`／`reserve_slot`。Session 自動有，同一堂用看板對照換對話。不建 API Server、不填 `base_url`。社團名走工具參數，不是神通 `user_id`。看板不是學生產品。
- 第 4 堂：同一支助理 SEQ／PAR／LOOP／RTR＋`post_poster`。LOOP 打磨海報，換日走 RTR。舊「只認臉不交」作廢。
- 第 5 堂：RAG＋Skill，MCP 不當主軸。Skill 不教寫海報；`references` 放申請表。`submit_application` → 看板待審。`reserve_slot` 不當本堂最後一槌。占用不進 RAG。
- `.cursor/rules` 已改成根目錄 `AGENTS.md`。

---

## 神通 REST（精簡，無密）

- 資源樹：Space → App → Agent／Session；另有 Provider、MCP、API Server、Folder、Skill（操作說明 V9 有技能管理；舊 1.2.2「沒有 Skill」作廢）。
- 學生產品接神通：login + session + `run_sse`。組裝用其他章。
- 主線工具：API Server + Call API Tool。神通打的是填進去的 URL，不是學生 localhost。建立 API Server 要 Admin。
- Live 曾見 `GET /api/v1/version` → `micore-backend` 1.4.0，新於手冊 1.2.2 時以 live 為準。
- 練習 Space **2「Vans測試」**。勿動 ESG／創新AI／Vietnam／sharon。
- Token 向使用者要，只放行程式記憶體，不落盤、不寫進本檔。Base URL／VPN 向使用者要，不要把帳密、JWT 寫進 repo。
- 勿發明 client library，除非使用者要求。PowerShell 易亂碼：打 API 用 `.py` 或 UTF-8 檔再讀。

Router 兩入口不要混：VS Code MCP 組裝神通；HTTP 是學生網站 → Router → `run_sse`。Router 不當堂存全班 `access_token`。學生產品不要本機再做一套 `ChatOpenAI` + tool loop。

本線 **未** 實作占用／海報／待審後端（那是看板 repo），也未在本 session 打神通 API。

---

## Do not

- 改輪廓 md；commit／push 除非要求；更新 wiki／`wiki/index.md` 除非攝取。
- 第 3 堂改回老師幫每人掛工具，或讓學生填 API Server／升全班 Admin。
- 看板當第 6–9 堂學生產品交件。
- 恢復獨立 Session 堂，或第 4 堂只認臉不交積木。
- API 裡自動改推日期；海報 LOOP 與換日揉成一顆。
- 第 5 堂用 Skill 教寫海報，或 MCP／占用 RAG 當主軸。
- 把金鑰／VPN 密碼／JWT 寫進任何檔。

---

## Resume checklist

1. 讀 `AGENTS.md`、`南一中-Agent課程-12堂.md`（第 1–5 堂）。
2. 看板契約讀 club-booking-board 的 `docs/specs` 與 API。第 5 堂要的待審若還沒有，在該 repo 加，不要在 vans 另做。
3. 打神通先 ping version；Token 向使用者要。
4. 改課表只動 12 堂檔。

---

## Suggested skills

- `handoff`：再拆對話時更新**本檔**，不要另開第二份。
- 看板／占用／待審實作：到 club-booking-board 用該 repo 的棧；`python-cli-from-template` 僅當要在 vans 寫最小神通 CLI。
- `playwright-cli`／`chrome-devtools`：核對神通 UI 掛工具、資料夾、技能時。
- `agents-md-guide`／`writing-for-agents`：改 `AGENTS.md` 時。

不要套用 CoreLab／Gamma／quiz-template／exam-OCR，除非換題。
