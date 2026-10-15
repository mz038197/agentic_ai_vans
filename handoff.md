# Handoff：南一中 12 堂 × 神通

Date: 2026-09-22  
Workspace: `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans`  
本檔是本 repo **唯一** handoff。已刪：`handoff-nanyi-12堂-2026-09-17.md`、`handoff-nanyi-mitac-agent-course.md`、`handoff-mitac-agent-builder-api.md`。

**教案真相來源：** `G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\台南一中\南一中-Agent課程-12堂.md`（第 1–8 堂已定；第 9–12 堂一堂一個 checkpoint）  
本 repo 根目錄同名 md 只是路標。  

**不要改：** `南一中-Agent課程規劃.md`  
**工作區指令：** `AGENTS.md`（Cursor 會讀）

神通官方手冊（raw，不改）：`G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\Agent_Builder`  
API HTML：該資料夾下 `MitacAgentBuilder-API-docs-v1.2.2\`（Ch.11 App；Ch.12 Agent 型別；Ch.14 `run_sse`；Ch.15 Session；Ch.17 MCP；Ch.18 API Server 要 Admin；Ch.19 Call API Tool）。舊本機 `C:\Users\mz038\Desktop\MitacAgentBuilder-API-docs-v1.2.2\` 不當預設。

課堂看板 repo：[club-booking-board](https://github.com/mz038197/club-booking-board)（課室看板；練習版另開，不在 vans 另做一套後端）

---

## Goal for the next session

對齊看板與第 5 堂契約：兩種申請、待補件（缺社團簡介）、兩張齊了才准、占用／海報／申請同一站重設。老師備 RAG 與第一種 Skill zip；第二種規格紙給學生寫，Admin 代傳。改課表只動 `G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\台南一中\南一中-Agent課程-12堂.md`。不要做學生面對的 Admin 代傳網站。

---

## 已落稿（勿當未決）

- 第 1 堂角色仍是 User，本稿不寫教案。舊「第 1 堂兩小時草案」作廢。
- 第 2 堂仍是 Builder。舊第 1 堂教室登記整段當開場，再從零建 LLM。總表不要寫「使用者→Builder」。
- 第 3 堂：學生自己掛 `check_slot`／`reserve_slot`。Session 自動有，同一堂用看板對照換對話。不建 API Server、不填 `base_url`。社團名走工具參數，不是神通 `user_id`。看板不是學生產品。
- 第 4 堂：同一支助理 SEQ／PAR／LOOP／RTR＋`post_poster`。LOOP 打磨海報，換日走 RTR。舊「只認臉不交」作廢。
- 第 5 堂：RAG＋兩種申請，MCP 不當主軸。規定在資料夾、做法在 Skill，兩邊不准互抄；RAG 不啟動 Skill。第一種老師 Skill（場地）→ `submit_application` → 待補件，畫面寫還要交社團簡介。第二種學生寫 Skill（社團名稱／用途／活動），老師代傳 zip、學生勾上 → `submit_club_profile`。兩張齊了老師才核准。只交第一張不准走格子。改期／駁回仍在第一張練。另要：公告停借那天 API 是空的仍駁回；換辦法 B、Skill 不動，裁決跟著檔走。兩份文件打架當加分。不要第三張、當堂不考會簽申請。Skill 不教寫海報、不准抄條號。`reserve_slot` 不當本堂最後一槌。占用不進 RAG。學生不進 Admin。不要學生網頁代 Admin 上傳。
- 第 6–7 堂改看板練習版（從 club-booking-board 另開），不是課室看板、不是學生產品。第 6 堂 grill → spec → tickets → implement → review；老師當 PM 加一條並先示範整輪。第 7 堂老師在練習版放對話空殼（輸入框／訊息區／新對話，送出只顯示在畫面）。學生 AI coding 接神通：`login` 拿該生 token（記憶體、不落盤）、Ch.15 建／重用 Session、Ch.14 `run_sse`（`streaming: true`，只印增量）。過關句是第 3 堂那片（週三午休視聽教室幫社團訂）；練習版格子要動，課室板不能動。熱線「你是誰」不算過關。不經 Router HTTP、不代登入。神通 API Server 由老師改指練習版，學生不填 `base_url`。第 8 堂角色仍是 AI Coder（不是 Product Builder）。專題開場：老師另發空殼（Vite＋React＋TS／FastAPI，Matt skill 在裡），先 prototype 再第一輪 grill，產出架構後放手。Product Builder 從第 9 堂起。第 9–12 堂 checkpoint：第 9 接線＋一份 JSON；第 10 確認鈕＋Canvas（MCP 自選）；第 11 Beta 五向測試；第 12 現場判斷或行動。不要第 9 堂做完產品。練習版不准 fork 當專題。當堂不接神通。確認鈕與決策瞬間第 9–11 堂。棧不准自選。不要用 Cadence 當專題。第 6 堂也不要用 Cadence／ai-coding-crash-course 當作業庫。
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

Router：VS Code MCP 組裝神通。第 7 堂是練習版薄後端 → 神通 login／Session／`run_sse`，不要網站打進 Router 再轉。token 不當堂存全班、不落盤。學生產品不要本機再做一套 `ChatOpenAI` + tool loop。

本線 **未** 實作占用／海報／兩種申請後端（那是看板 repo），也未在本 session 打神通 API。Skill 上傳走 Admin；USER 只能勾 Space 裡已有的技能。

---

## Do not

- 改輪廓 md；commit／push 除非要求；更新 wiki／`wiki/index.md` 除非攝取。
- 第 3 堂改回老師幫每人掛工具，或讓學生填 API Server／升全班 Admin。
- 課室看板當第 6–12 堂學生產品交件。第 6–7 堂只改練習版；第 8 堂不要交練習版或另 `npm create` 換棧。
- 第 7 堂用 Router 代登入，或把聊天空殼連假後端一起做完留給學生只改 URL。
- 第 9 堂一次做完接線、確認鈕、Canvas、MCP。
- 恢復獨立 Session 堂，或第 4 堂只認臉不交積木。
- API 裡自動改推日期；海報 LOOP 與換日揉成一顆。
- 第 5 堂用 Skill 教寫海報，把辦法條文抄進 Skill，或 MCP／占用 RAG 當主軸。
- 第 5 堂加第三種申請，或把 40 人會簽做成過關。
- 學生進 Admin 上傳，或做學生面對的網站代老師權限傳 zip。
- 只交第一張場地申請就核准借走。
- 把金鑰／VPN 密碼／JWT 寫進任何檔。

---

## Resume checklist

1. 讀 `AGENTS.md`、以及 `G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\台南一中\南一中-Agent課程-12堂.md`（第 1–5、第 7、第 8 堂已寫）。
2. 看板契約讀 club-booking-board 的 `docs/specs` 與 API。第 5 堂要的兩種申請／待補件／兩張齊了才准若還沒有，在該 repo 加，不要在 vans 另做。
3. 打神通先 ping version；Token 向使用者要。
4. 改課表只動 12 堂檔。

---

## Suggested skills

- `handoff`：再拆對話時更新**本檔**，不要另開第二份。
- 看板／占用／兩種申請實作：到 club-booking-board 用該 repo 的棧；`python-cli-from-template` 僅當要在 vans 寫最小神通 CLI。老師代傳 Skill 用本機 CLI，不要學生站。
- `playwright-cli`／`chrome-devtools`：核對神通 UI 掛工具、資料夾、技能時。
- `agents-md-guide`／`writing-for-agents`：改 `AGENTS.md` 時。

不要套用 CoreLab／Gamma／quiz-template／exam-OCR，除非換題。
