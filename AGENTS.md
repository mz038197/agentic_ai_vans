# AGENTS.md

本工作區：`agentic_ai_vans`（南一中 Agent 課程、神通帶班、Vans Router）。下列路徑與邊界給進這個 repo 的 agent 用。

教案真相來源：

`G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\台南一中\南一中-Agent課程-12堂.md`

改課表改那一份。本 repo 根目錄同名 md 只是路標。不要改 `南一中-Agent課程規劃.md`。其他工作區也讀這條絕對路徑，不要在 vans 找全文。

---

## 神通 Agent Builder 文件

官方手冊與操作說明一律在：

`G:\我的雲端硬碟\Obsidian\Agent\raw\materials\神通科技\Agent_Builder`

這是 Obsidian Agent vault 的 `raw/materials`，不是本 repo。讀文件時直接開這個絕對路徑，不要在 `agentic_ai_vans` 裡找 PDF／手冊。

使用者說「神通文件」「神通手冊」「Mitac 說明書」「Agent Builder 操作說明」「MCP 操作說明」或要對照官方能力時，先列這個資料夾再讀檔。

目前可見檔名（會增減，以磁碟為準）：

- `MiTAC Agent Builder操作說明書V9_技能管理整合版_含目錄與截圖.pdf`
- `MiTAC MCP操作說明書_v1.1.4.pdf`

邊界：

- 官方 PDF／手冊視為 `raw`：不修改、不刪、不搬既有檔。摘錄與更正寫進 `wiki/`，或寫進本 repo 的 `handoff.md`。
- 帶班教案例外：`神通科技\台南一中\南一中-Agent課程-12堂.md` 是共用活檔，改課表改那份。不要因為「不改 raw」拒改，也不要改回 vans。
- 本 repo 唯一接續檔是 `handoff.md`（REST 精簡筆記也在那裡），不是官方手冊。產品操作以這個資料夾的 PDF 為準。
- 舊本機路徑 `C:\Users\mz038\Desktop\MitacAgentBuilder-API-docs-v1.2.2\` 不再當預設，除非使用者明確指定。

---

## 課堂看板（南一中 12 堂）

老師課室看板與占用／海報／申請 API 的專案在 GitHub，不在 `agentic_ai_vans`：

https://github.com/mz038197/club-booking-board

改看板、對契約、實作占用／海報／兩種申請（待補件→兩張齊了才准）時先讀該 repo（`docs/specs`、`backend/`、`frontend/`），不要在本 repo 另做一套。

兩份不要混：

- **課室看板**：第 3–5 堂上課投影，不要在上面演示 AI 寫碼或接 `run_sse`。
- **看板練習版**：從上面那個 repo 另開一份。第 6–7 堂用。第 7 堂老師放對話空殼，學生用練習版薄後端打神通 login／Session／`run_sse`，不經 Router HTTP。第 8 堂學生產品不要交這份。
- **專題空殼**：第 8 堂另發（Vite＋React＋TS／FastAPI）。先 prototype 再 grill。不要 fork 練習版，也不要做在課室看板上。

它不是神通官方手冊；產品操作仍以上面的 Agent_Builder 資料夾為準。本機若已 clone 在 `C:\Users\mz038\Desktop\peas-agent\` 底下，用那個目錄；沒有就對 GitHub 或先 clone。
