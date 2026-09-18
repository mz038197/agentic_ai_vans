# Handoff: 南一中 12 堂課（2026-09-17）

Date: 2026-09-17（同日續寫：Session 併進第 3 堂；Planning 四層畫布改到第 4 堂）  
Workspace: `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans`  
This session: Cursor Ask then Agent; working teaching doc updated.

Prior handoffs (still valid except where this file supersedes):

- Course + 神通帶班：`handoff-nanyi-mitac-agent-course.md`（2026-09-06）
- Mitac REST 事實：`handoff-mitac-agent-builder-api.md`

**教案真相來源：** `南一中-Agent課程-12堂.md`  
**不要改：** `南一中-Agent課程規劃.md`

神通官方手冊（raw，不改）：`G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\Agent_Builder`  
API HTML：該資料夾下 `MitacAgentBuilder-API-docs-v1.2.2\`（Ch.12 五種 agent type；Ch.17 MCP；Ch.18 API Server 建立要 Admin；Ch.19 Call API Tool）。舊本機 `C:\Users\mz038\Desktop\MitacAgentBuilder-API-docs-v1.2.2\` 不當預設。

---

## Goal for the next session

定第 5 堂要上什麼，或實作老師側占用／海報 API＋看板（占用表＋海報頁、能一起重設、多週三午休種子）。改課表只動 `南一中-Agent課程-12堂.md`。

---

## 本對話已寫進 12 堂檔（勿當未決）

### 第 1–2 堂角色 vs 內容

- 第 1 堂**角色仍是 User**。內容使用者另有安排，**本稿不寫教案**。
- 第 2 堂**角色仍是 Builder**。舊第 1 堂教室登記那套（走完老師 App、兩套身份、Idea Bank）**整段併進第 2 堂開場**，然後從零建 LLM、交 v0.1。
- 總表角色欄不要寫「使用者→Builder」。曾誤改成第 2 堂前半 User，使用者糾正後已改回。

`handoff-nanyi-mitac-agent-course.md` 裡「第 1 堂兩小時草案」**作廢**。

### 第 3 堂（已定案，含原獨立 Session 堂）

細節以 12 堂檔「第 3 堂」節＋主線「老師課前備好」為準。摘要：

- Builder／Lv6 Tools。仍是第 2 堂那塊 LLM。同一堂後半指認 Lv5：神通 Session 自動有，學生不建造。
- 老師：占用 API（神通打得到）＋ Space 一個 API Server＋手填 Call API Tool（`check_slot`、`reserve_slot`；第 4 堂才掛 `post_poster`）＋課室看板（只讀、無預約鈕、能重設）。示範 App 也掛查／訂。後半對照用占用表，不另做記憶 API／回想工具。
- 學生：自己把兩支時段工具掛上 LLM、改 instruction、跑搶視聽教室；神通要看到 tool，看板要動。接著同一筆問「我剛訂了哪」；新開一筆再問（答不出、格子仍亮）；新對話問「這格有沒有人」可查表。
- 不填 `base_url`、不建 API Server（需 Space Admin，全班各建一份會炸）。不 MCP、不 OpenAPI。天氣不當主線。
- 「誰」＝`預留`／`貼海報` 的社團名，不是神通 `user_id`（API Server 預設 `principal_propagation_mode=none` 不會帶帳號）。不開 `assertion_auth`。
- 看板是老師儀表板，不是第 6–9 堂作業。工具不自動改推下一格。

### 第 4 堂（原第 5 堂 Planning，已落稿四層）

同一支第 3 堂登記助理往上加，不是四張無關作業：

1. SEQ 先查再訂（練這層要有空格：重設或指定更後面的週三）。
2. PAR：確定空之後同時訂教室＋寫招生海報。
3. LOOP：海報改到能貼（規定寫死、最多 3 版）再 `post_poster`。這圈不換日期。
4. RTR：第一次查若已滿，同一間、同一個午休，最多再查 3 個週三；找到空接回 2～3；仍滿則不訂不貼。

看板：占用＋海報同一站，一鍵重設兩邊。種子下一週三已被占；表上要有後續週三。換日成功時種子格仍是別人，社團和海報在更後面的週三。

第 8 堂仍是網站決策瞬間＋人按確認。這裡 RTR 是 Builder 分流。

### 第 5 堂

待定。原 Planning 已換到第 4 堂。

---

## 本對話討論過、已落稿者勿當未決

畫布四層＋`post_poster`＋海報頁：**已寫進第 4 堂**。舊建議「PAR＝兩間教室一起查／LOOP＝換午休當主 LOOP／只認臉不交」**作廢**。

---

## 仍有效的舊約束

見 `handoff-nanyi-mitac-agent-course.md`：Router 兩入口不要混；勿改輪廓 md；勿把金鑰／VPN／JWT 寫進檔；勿 commit／push 除非要求；學生產品不要本機再做一套 `ChatOpenAI` + tool loop。練習 Space 2「Vans測試」；勿動 ESG／創新AI／Vietnam／sharon。

本 session **未打神通 API、未做占用 API／看板／海報程式**。

---

## Do not

- 把第 3 堂改回「老師幫每人掛工具」。
- 讓學生第 3 堂填 API Server／升全班 Admin（除非使用者改口）。
- 把課室看板做成學生產品交件。
- 把第 4 堂恢復成獨立 Session 堂，或恢復「PAR／LOOP／RTR 只認臉不交」。
- 在 `reserve_slot`／`check_slot` 裡自動改推日期。
- 把海報 LOOP 和換日 RTR 揉成同一顆 LOOP。

---

## Resume checklist

1. 讀 `南一中-Agent課程-12堂.md`（第 1–4 堂已定；第 5 堂待定）。
2. 問下一刀：第 5 堂主題，還是老師占用／海報 API＋看板實作。
3. 實作 API 時：神通不要填學生 localhost；Call API Tool／API Server 建立要 Admin。占用表要多週三；`post_poster` 與占用同一可重設資料。
4. REST 細節：`handoff-mitac-agent-builder-api.md`＋神通資料夾 HTML。Token 向使用者要，不落盤。

---

## Suggested skills

- `handoff`：這條線再拆對話時。
- `python-cli-from-template`：要做占用／海報 API／最小神通 CLI／`main_mitac.py` 時。
- `developing-with-streamlit` 或專案既有網頁棧：課室看板（占用＋海報頁）。
- `agents-md-guide`／`writing-for-agents`：Router MCP 組裝神通時。
- `playwright-cli`／`chrome-devtools`：核對神通 UI 掛工具流程時。

不要套用 CoreLab／Gamma／quiz-template／exam-OCR，除非換題。
