# 南一中 Agent 課程：12 堂帶班規劃

成長曲線：Agent 使用者 → Agent Builder → AI Coder → Product Builder。

最終產出：每組一件可 Demo、可參賽的 Agent 產品。不是「會呼叫模型」，是「拿掉 Agent 之後產品明顯變弱」。

---

## 帶班約束

前五堂的 agent **住在神通**。學生當使用者或改 instruction／選現成工具，不在 Python 裡 `bind_tools`。

第 6 堂起進 VS Code。Vans Router 有兩個入口，不要混：

- VS Code MCP：組裝神通上的 App（建 agent、掛工具、改 instruction）
- HTTP：學生網站打進來，Router 代打 login／session／`run_sse`

工具執行在神通。學生後端不跑 tool loop。自訂 REST 等學生有自己的 API 再掛，第 3 堂不做。

本機 `main.py`（Agent Dungeon）只當對照，不當作業主線。

帳號：每生一個神通帳號。Router 用「當堂 login + 連線記憶體 + refresh」，不存全班 `access_token`。練習空間固定，不碰其他 Space。

---

## 12 堂總表

| 堂 | 角色 | 主題 | 當堂解鎖 | Runtime | 當堂產出 |
|---|---|---|---|---|---|
| 1 | 使用者 | Agent 是什麼 | Goal、Action | 老師做好的神通 App | Idea Bank |
| 2 | 使用者 | 從 Prompt 到身份 | Role、Instruction、Constraints | 神通改 instruction | Personal Agent v0.1 |
| 3 | Builder | 它開始會做事 | 現成 Tool | 神通，老師先掛 1–2 個工具 | 會選工具的 Agent |
| 4 | Builder | 它怎麼記住 | Session＝短期記憶 | 同一條／換一條 session | 有狀態的對話流程 |
| 5 | Builder | 複雜任務 | Instruction 裡的步驟 | 單一 Agent，不寫 Multi-Agent | 多步驟 Agent |
| 6 | AI Coder | 用 AI 寫軟體 | Spec → Task → 寫碼 | VS Code | 產品 Spec + 第一個網頁殼 |
| 7 | AI Coder | 網站接到 Agent | Router HTTP、`run_sse` | Web → Router → 神通 | Agent Web App v1 |
| 8 | Product Builder | 不是加聊天框 | Observe→Decide→Act、人在迴圈裡 | 同一套 Web + 神通 | Web App v2（有決策瞬間） |
| 9 | Product Builder | 資料從哪來 | 自己的 JSON／DB／RAG／外部 API | 神通工具打學生資料 | 有專屬資料的 Agent |
| 10 | Product Builder | 專題 Sprint | Product Canvas | 文件 + 原型 | Proposal + 架構圖 |
| 11 | Product Builder | 做出來、測、改 | 功能／決策／失敗／亂講 | 專題 repo | Beta |
| 12 | Product Builder | Demo Day | Pitch | 現場 | 競賽版 Demo |

---

## 第一段：Agent 使用者

### 第 1 堂：什麼時候需要 Agent

核心問題：什麼時候需要 Agent，而不是聊天機器人？

演進只講到能聽懂即可：

```text
LLM 會回答
→ 加上任務（Instruction）
→ 加上行動（Tool）
→ 加上狀態（還記得現在怎樣）
→ 為了目標持續行動＝Agent
```

當堂：全班用老師做好的一支神通 App 玩一輪。每人建 Idea Bank（讀書規劃、錯題、社團器材、校園導覽等）。每則 idea 寫：誰、痛點、Agent 要做的判斷（不是「回答問題」）。

不做：API、帳密、寫程式。

### 第 2 堂：同一個模型，不同 Agent

核心問題：為什麼換 Role／Goal／Constraints，行為就不一樣？

當堂：每人（或每組）在指定 Space 改自己的 instruction，產出 Personal Agent v0.1。對照兩個版本（例如「嚴格學科助教」vs「會吐槽的學長」）同一題，記下差異。

產出格式固定：Role、Goal、Constraints、Context、Output。

不做：工具、自己打 `run_sse`。

---

## 第二段：Agent Builder

### 第 3 堂：它只會講，不會做

核心問題：知道答案和真的做完一件事差在哪？

解鎖：Tool。流程只畫一輪：選工具 → 執行 → 拿結果 → 再說話。

當堂：老師事先掛 1–2 個神通連得到的工具（例如天氣、課表）。學生改 instruction，讓 Agent **會決定何時呼叫**。看一次實際 tool 發生。

可預告菜單（下堂以後才做）：Search、Todo、Quiz、資料庫、自訂 REST。

不做：學生寫 `@tool`、自架 MCP、填 API Server 表格。

### 第 4 堂：它怎麼每次都忘記

核心問題：短期記憶和「產品要長期記住的資料」不是同一件事。

解鎖：神通 Session。同一條 session 連續對話會記得；換一條就失憶。這是 short-term。

當堂：設計一個最小使用者流程（例如英文練習：出題 → 作答 → 根據這輪對錯出下一題）。用同一 session 跑完。對照「新開 session」會怎樣。

Long-term（等級、累積錯題）先點名，實作放到第 9 堂。若當堂要演「依歷史出題」，用老師準備的假資料 API，不要假裝 Session 會永遠記得。

### 第 5 堂：複雜任務一次做不完

核心問題：大任務怎麼拆成可檢查的步驟？

解鎖：寫在 instruction 裡的 workflow（了解需求 → 查 → 整理 → 做 → 檢查 → 輸出）。仍是 **Single Agent + 現成 Tools + Session**。

當堂：把第 2 堂的 v0.1 改成「必須依步驟走，每步可看出來」。Demo 時能指認現在走到哪一步。

不做：`parallel`／`loop`／多 Agent。神通有這些型別，這堂碰了會把除錯時間吃光。

第二段結束檢查：學生能講自己的 Agent 用了什麼身份、什麼工具、記憶存在哪、步驟是什麼。還不能要求他們會組 MCP。

---

## 第三段：AI Coder

### 第 6 堂：用 AI 寫軟體，但先寫規格

核心問題：為什麼不能直接說「幫我做一個 XXX 網站」？

解鎖：固定開發流程。

```text
Idea → Problem → Requirement → Spec → Tasks → AI Coding → Run → Debug → Improve
```

Spec 至少有：User、Problem、Core Flow、Features、MVP、Constraints。

當堂：VS Code 上場。可以用 Router MCP 查看／微調他們在神通上的 App，但本堂產出是 **Spec + 一個還不能講話的網頁殼**（頁面、按鈕、假資料即可）。

不做：當堂接完 `run_sse`（那是第 7 堂）。

### 第 7 堂：網站接到 Agent

核心問題：我做的是一個系統，不是 AI Demo。

學生要能畫出並實作：

```text
使用者 → Web
       → （很薄的）Backend
       → Vans Router（HTTP）
       → 神通 run_sse
            → 該組的 App
            → 神通再打已掛上的工具
```

當堂：登入（或 Router 代登入）、開／重用 session、把輸入送進 `run_sse`、畫面只印增量文字、不要把最後整段再貼一次。產出 Agent Web App v1：網頁上跟**自己的**神通 App 說話。

自訂工具：若產品需要打他們第 6–7 堂寫的 REST，由老師或進階組用 API 登記 API Server，再掛上 Agent。全班不是作業必做。

不做：網站裡再接一套 `ChatOpenAI` + 本機 tools。

---

## 第四段：Product Builder

### 第 8 堂：不是加聊天框就叫 Agent

核心問題：使用者有沒有看到 Agent 在判斷、在行動？

對照：輸入→AI→輸出 vs Observe→Decide→Act→看結果→再決定。

當堂案例用「普通批改」對「英文 Coach」：分析 → 找弱點 → 出題 → 作答 → 再分析 → 改下一輪。Web App v2 必須能指出一次**決策瞬間**（例如連錯才降難度）。需要人確認的動作（寄信、刪資料）做成確認鈕，對應神通的 tool confirmation 或你們自己的按鈕。

評：拿掉對話框之後，若只剩靜態頁，退回重做。

### 第 9 堂：模型知道很多，你們的資料在哪

核心問題：為什麼這不是 ChatGPT 套殼？

解鎖其一即可，不要全做：自己的 JSON／CSV、小資料庫、外部 API、神通 RAG（上傳該組真正在用的檔）。

當堂：Agent 經工具讀寫**這組產品的資料**。錯題本、器材清單、社團課表，必須是他們的，不是模型常識。

Session 仍是對話短期記憶。等級、庫存、歷史錯題進自己的資料，再讓工具去碰。

### 第 10 堂：專題 Sprint

每組一份 Agent Product Canvas：

- User / Problem
- Agent Goal
- Agent Loop（Observe→Decide→Act）
- Tools（神通上實際掛了什麼）
- Data（檔、表、API 在哪）
- MVP
- Why Agent（為什麼不是普通程式）

產出：Proposal、可點的 Prototype、一張架構圖（必須出現 Router 與神通 App，不能只畫「前端＋GPT」）。

### 第 11 堂：做、測、改

五個測試方向都要留下紀錄：功能能不能用、決策合不合理、使用者知不知道 Agent 在幹嘛、工具失敗怎麼辦、亂講怎麼辦。順便問：這件事需要 LLM 嗎？

產出：Beta。沒過「拿掉 Agent 是否成立」不能進 Demo Day。

### 第 12 堂：Demo Day

Pitch 順序：Problem → 現況痛點 → Idea → Why Agent → Live Demo → Impact。

現場至少一次：**Agent 做出判斷或行動**。例如連續錯三題後自動改卷，而且改卷依據看得到（資料或 tool 結果）。

只展示「我們接了模型」當沒 Demo。

---

## 評分（對齊專題原則）

學生必須能回答：

1. 解決什麼問題、給誰用
2. 為什麼需要 Agent
3. Agent 做了哪一次判斷
4. 用了哪些神通工具
5. 用了哪些自己的資料
6. 和直接開 ChatGPT 差在哪

不及格典型：網站＋聊天框、工具全是假的、記憶只靠「請模型記住」、架構圖沒有神通 App。

---

## 和舊輪廓的差異（帶班用）

- 第 3 堂工具改為「體驗老師掛好的」，自訂 Function 延到第 7、9 堂有東西可掛。
- 第 4 堂記憶先只教 Session；長期資料明確留給第 9 堂。
- 第 5 堂不上 Multi-Agent。
- 第 6–7 堂才出現 Router；第 6 組裝、第 7 通話。
- 第 11–12 堂收在 Product Builder 裡，不再另立第五段角色，避免曲線和課表對不齊。
