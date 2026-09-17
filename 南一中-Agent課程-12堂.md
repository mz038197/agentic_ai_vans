# 南一中 Agent 課程：12 堂帶班規劃

成長曲線：Agent 使用者 → Agent Builder → AI Coder → Product Builder。

最終產出：每組一件可 Demo、可參賽的 Agent 產品。不是「會呼叫模型」，是「拿掉 Agent 之後產品明顯變弱」。

---

## Agent User 定義

**Agent User 是使用現成 Agent 完成任務的人，不是改 Agent 的人。**

當堂目標一句話：I can use an Agent.

算 User：

- 用老師做好的神通 App 走完一輪真實任務
- 能指出這次是「為了目標採取行動」，還是只是聊天
- 能判斷什麼生活問題適合交給 Agent
- 能說出用完後缺了什麼（不會做事、下堂才解鎖）

不算 User，從 Builder 起算：

- 改 Role／Goal／Instruction
- 掛或挑選工具
- 管 Session
- 打 API、寫網頁

「同一個模型、不同 instruction 行為會變」第 1 堂只由老師示範給學生看。學生自己改 instruction，是第 2 堂 Builder。

---

## Agent Builder 定義

**Agent Builder 是改 Agent 本身的人，不是寫產品網站的人。**

當堂目標一句話：I can build an Agent.

改的對象是神通上的 App：它是誰、會呼叫什麼、對話記在哪、任務怎麼拆。產出是一支比較能做事的 Agent，不是一個 repo。

算 Builder：

- 改 Role／Goal／Instruction／Constraints
- 選或掛老師準備好的工具（何時該呼叫）
- 用 Session 當短期記憶，並能說出換 session 會怎樣
- 把複雜任務寫進步驟（仍是單一 Agent）

不算 Builder：

- 只用現成 Agent、不改任何設定（那是 User）
- 在 VS Code 寫網頁、拆 Spec、用 AI 改檔（那是 AI Coder）
- 想產品給誰用、決策瞬間夠不夠（那是 Product Builder）

第 2–5 堂。不開 VS Code 當主場地。

**天花板（第 5 堂結束）：** 一支以 **LLM** 為主的神通 Agent，有自己的身份、會在對的時候呼叫老師掛好的工具、同一條 Session 記得這輪對話、步驟寫在 instruction 或（進階）包在 **SEQ** 裡。能指認畫布上五塊編排積木各做什麼。學生能講「我改了什麼、它因此做了什麼」。

到此為止，不是 coding 能力。未包含：自寫 MCP／API Server、`run_sse` 客戶端、VS Code、網頁、自己的資料庫／RAG。PAR／LOOP／RTR 認得出即可，不當作業。那些分別是 Coder（第 6–7）和 Product Builder（第 8–9）。

舊版從零一路走到 Router 寫碼，Builder 和 Coder 是同一條坡。新版在第 5 堂切斷：神通 Builder 交的是「會改 Agent」，不是「會做軟體」。

對齊 Agent Dungeon 的**能力層名稱與編號**，不對齊上課順序，也不對齊「學生自己寫 Python」。Lv1–3 神通已經給了，第 1 堂只當使用者體驗，Builder 不重做。

| 堂 | 本堂 Lv | 學生實際改的 | 不做（留給後面） |
|---|---|---|---|
| 2 | **Lv4 Identity** | Role／Goal／Instruction／Constraints | 工具、Session |
| 3 | **Lv6 Tools** | 何時呼叫老師已掛的工具 | 自寫 `@tool`／MCP／API Server。完整 Observe→Decide→Act 是 Lv7，第 8 堂 |
| 4 | **Lv5 Memory** | 神通 Session＝這輪短期記憶 | 長期占用表／DB／RAG（第 9 堂） |
| 5 | **Planning**（Dungeon 沒有獨立關卡） | instruction 步驟；老師帶 SEQ／PAR／LOOP／RTR | 不要叫 Lv8。作業不交 PAR／LOOP／RTR |

編號會跳：2→4、3→6、4→5。跟學生講「這堂練的能力叫什麼」，不要講「我們在衝 Dungeon 第幾關」。

### 兩種積木，不要混

能力積木是 Lv：Identity、Tools、Memory、Planning。編排積木是神通畫布上的型別，API 叫 `llm`／`sequential`／`parallel`／`loop`／`custom`，UI 是 **LLM／SEQ／PAR／LOOP／RTR**。

| 畫布 | 一句話 | 哪堂帶 | 學生交什麼 |
|---|---|---|---|
| LLM | 一塊會想、會講、可掛工具的代理 | 第 2 堂從零就建這個 | 第 2–5 堂主線 |
| SEQ | 子代理照順序走完 | 第 5 堂，Planning 的可視版 | 認得出；進階組可把「了解→做」拆成兩個 LLM 再塞進 SEQ |
| PAR | 子代理同時跑 | 第 5 堂老師示範 | 不交 |
| LOOP | 同一段重複 N 次 | 第 5 堂老師示範 | 不交 |
| RTR | 依條件走哪一條（`custom`） | 第 5 堂認臉，對齊以後的 Lv7 | 不交。產品決策瞬間仍是第 8 堂 |

第 3–4 堂工具和 Session 是掛在 **LLM** 上，不是新的畫布積木。

---

## AI Coder 定義

**AI Coder 是用 AI 當開發夥伴、寫出軟體的人，不是在 IDE 裡重做一個 Agent runtime。**

當堂目標一句話：I can build software with AI.

寫的對象是學生電腦上的產品：規格、網頁、接到神通的線。VS Code + Router 展示的是 coding 能力。神通 App 在這段是**被接上去的元件**，不是被取代的本機 agent。

算 AI Coder：

- 先寫 Spec 再拆 Task，不說「幫我做一個 XXX 網站」
- 用 Router 在 VS Code 寫碼、跑、除錯
- 把 Web 接到 Router HTTP，再打到自己的神通 App（`run_sse`）
- 必要時用 Router MCP **代操**神通（改 instruction、查看 App），評的仍是軟體有沒有做出來

不算 AI Coder：

- 只在神通後台改人設、選工具（那是 Builder，不必開 VS Code）
- 在網站裡再寫一套 `ChatOpenAI` + 本機 tool loop（兩套 runtime）
- 以為接上聊天框就交差（還沒進 Product Builder 的判斷題）

第 6–7 堂。Router 在 VS Code 裡是 coding 夥伴；在網站後方是神通的電話。兩件事都是 Coder，都不是「神通取代 Router」。

---

## 帶班約束

第 1 堂只當使用者。第 2–5 堂的 agent **住在神通**：改 instruction、選現成工具、用 Session。不在 Python 裡 `bind_tools`。

第 6 堂起進 VS Code。Vans Router 有兩個入口，不要混：

- VS Code MCP：組裝神通上的 App（建 agent、掛工具、改 instruction）
- HTTP：學生網站打進來，Router 代打 login／session／`run_sse`

工具執行在神通。學生後端不跑 tool loop。自訂 REST 等學生有自己的 API 再掛，第 3 堂不做。

本機 `main.py`（Agent Dungeon）只當對照，不當作業主線。

帳號：每生一個神通帳號。Router 用「當堂 login + 連線記憶體 + refresh」，不存全班 `access_token`。練習空間固定，不碰其他 Space。

---

## 12 堂總表

| 堂 | 角色 | 主題 | 本堂 Lv | 當堂解鎖 | Runtime | 當堂產出 |
|---|---|---|---|---|---|---|
| 1 | 使用者 | 用現成 Agent | 體驗 Lv1–3（不實作） | 分辨 Agent vs Chatbot | 老師做好的神通 App | Idea Bank（含「用完缺什麼」） |
| 2 | Builder | 從 Prompt 到身份 | Lv4 Identity | Role、Instruction、Constraints | 學生改神通 instruction | Personal Agent v0.1 |
| 3 | Builder | 它開始會做事 | Lv6 Tools | 現成 Tool、何時呼叫 | 神通，老師先掛 1–2 個工具 | 會選工具的 Agent |
| 4 | Builder | 它怎麼記住 | Lv5 Memory | Session＝短期記憶 | 同一條／換一條 session | 有狀態的對話流程 |
| 5 | Builder | 複雜任務 | Planning | Instruction 裡的步驟 | 單一 Agent，不寫 Multi-Agent | 多步驟 Agent |
| 6 | AI Coder | 用 AI 寫軟體 | Lv8 Coding 起算 | Spec → Task → 寫碼 | VS Code | 產品 Spec + 第一個網頁殼 |
| 7 | AI Coder | 網站接到 Agent | Lv8（接上神通） | Router HTTP、`run_sse` | Web → Router → 神通 | Agent Web App v1 |
| 8 | Product Builder | 不是加聊天框 | Lv7 Decision | Observe→Decide→Act、人在迴圈裡 | 同一套 Web + 神通 | Web App v2（有決策瞬間） |
| 9 | Product Builder | 資料從哪來 | Data（非 Dungeon 關卡） | 自己的 JSON／DB／RAG／外部 API | 神通工具打學生資料 | 有專屬資料的 Agent |
| 10 | Product Builder | 專題 Sprint | — | Product Canvas | 文件 + 原型 | Proposal + 架構圖 |
| 11 | Product Builder | 做出來、測、改 | — | 功能／決策／失敗／亂講 | 專題 repo | Beta |
| 12 | Product Builder | Demo Day | — | Pitch | 現場 | 競賽版 Demo |

---

## 1–9 堂主線：教室時段登記

練習產品固定這一件。人物固定「高一的小明，週三午休要為社團登記視聽教室」。第 10 堂才換他們自己的專題。Idea Bank 第 1 堂就寫自己的題，不當堂做。

目標句（第 9 堂結束要能 Demo）：小明在網站提出時段 → Agent 先查占用再決定准或改建議 → 衝突出現時畫面看得到這次判斷 → 關掉重開，預約還在。

老師課前備好、九堂共用：

- 一支示範用神通 App（第 1 堂全班用）。要真的查時段、擋住衝突，不能只回「好啊你去跟總務說」。
- 同一支的第二套 instruction：嚴格總務 vs 好說話的學長。
- 一支時段工具（老師掛）：`查空檔(教室, 日期)`、`預留(教室, 時段, 社團)`。第 3 堂起掛在學生自己的 LLM 上。天氣不當主線工具。
- 第 4 堂對照用的「假占用表 API」可選；沒有就用換 session 證明失憶。
- 第 9 堂學生 repo 裡一份 `data/rooms.json`（教室、時段、誰借走）。

| 堂 | 小明這堂碰到什麼 | 當堂只新加 | 還缺、下堂才給 |
|---|---|---|---|
| 1 | 用老師的登記 App 走完一輪：要視聽教室、看到查過占用、准或被拒。再看老師切兩套身份。 | 當使用者走完；Idea Bank | 不能改人設 |
| 2 | 自己在神通從零建一支 LLM 登記助理，寫成嚴格或好說話，同一題對照。 | Identity | 它還是只會講，不會查真的空檔 |
| 3 | 老師把時段工具掛上。學生寫「要查占用或預留時才呼叫」。親眼看 tool。 | Tools | 換分頁就忘這輪已預留哪一間 |
| 4 | 同一 session：查空檔 → 預留 → 接著問「我剛訂了哪」。新開一條，它不認得這筆。 | Session | 明天再開仍是空白 |
| 5 | instruction 寫死步驟：問需求 → 查空檔 → 看衝突 → 登記或改建議 → 回報。老師用同一輪示範 SEQ／PAR／LOOP／RTR。 | Planning；認畫布五塊 | 還在神通對話框裡 |
| 6 | 為「教室登記網站」寫 Spec。做出有「教室／日期／時段／我的預約」區塊的殼，按鈕是假的。 | Spec、網頁殼 | 殼還不能打電話 |
| 7 | 網站經 Router 打自己的神通助理，畫面上跟它說話。 | `run_sse` | 看起來仍像聊天框 |
| 8 | 同一時段已有人：Agent 不准或改推下一個空檔，網站標出這次判斷。真的鎖教室要按確認。 | 決策瞬間（Lv7） | 重整後預約沒了 |
| 9 | `rooms.json` 住在他們後端。重開網站先讀檔；預留成功就寫回。下週那格還是小明社團的。 | 自己的資料 | 第 10 堂才換專題題材 |

主線工具不要換。第 3 堂天氣是菜單上的雜訊，會把九堂拆成九個故事。

第 8 堂確認鈕是主線：鎖定教室、取消別人的預留，都要人按一下。對應神通 tool confirmation 或網站自己的按鈕。

第 9 堂主線用 JSON，不用 RAG。RAG 留口頭對照：上傳「教室使用規則」是另一種「我們的資料」，時段占用不要塞進 RAG。

---

## 第一段：Agent 使用者（僅第 1 堂）

### 第 1 堂：用一個現成的 Agent

核心問題：我現在是使用者。這個東西跟聊天機器人差在哪？什麼問題值得交給它？

演進只講到能聽懂即可：

```text
LLM 會回答
→ 加上任務（Instruction）
→ 加上行動（Tool）
→ 加上狀態（還記得現在怎樣）
→ 為了目標持續行動＝Agent
```

當堂三件事，都不要讓學生改 Agent：

1. 全班用老師做好的神通 App 走完一輪任務（必須看得到一次「它做了什麼」而不只是回話）。
2. 老師切換兩套 instruction、同一題，學生只觀察行為差在哪。
3. 每人寫 Idea Bank。每則：誰、痛點、Agent 要做的判斷、**我剛用完還缺什麼**。

「還缺什麼」是後面的鉤子：不會真的做事 → 第 3 堂；每次忘記 → 第 4 堂；一步做不完 → 第 5 堂。

不做：改 instruction、開自己的 App、API、帳密、寫程式。

第一段結束檢查：學生能當使用者講完「我請它做了什麼、它行動了沒、我還想做什麼產品」。還不能改 Agent。

---

## 第二段：Agent Builder（第 2–5 堂）

### 第 2 堂：同一個模型，不同 Agent

本堂 Lv：**Lv4 Identity**。神通上的 Role／Goal／Instruction／Constraints，對齊 Dungeon 的 soul／user，只是寫在 App 後台，不寫 `build_system_prompt`。畫布積木用 **LLM**，不要一開始就拉 SEQ。

核心問題：為什麼換 Role／Goal／Constraints，行為就不一樣？我要開始改它。

當堂：每人（或每組）在神通 UI 從零建 App／Agent（型別 LLM）、選模型、存、確認能說話。再改自己的 instruction，產出 Personal Agent v0.1。對照兩個版本（嚴格總務 vs 好說話的學長）同一題：週三午休視聽教室，記下差異。

產出格式固定：Role、Goal、Constraints、Context、Output。

不做：工具、自己打 `run_sse`。

### 第 3 堂：它只會講，不會做

本堂 Lv：**Lv6 Tools**。學生改的是「什麼時候該呼叫」，不是工具本體。那半步像 Lv7 Decision，本堂不掛那個名字；產品裡的決策瞬間留第 8 堂。

核心問題：知道答案和真的做完一件事差在哪？

解鎖：Tool。流程只畫一輪：選工具 → 執行 → 拿結果 → 再說話。

當堂：老師把主線時段工具掛上學生的登記助理。學生改 instruction，讓 Agent **要查占用或預留時才呼叫**。看一次實際 tool 發生。

天氣當菜單口頭提一句即可，不當堂換主線。

不做：學生寫 `@tool`、自架 MCP、填 API Server 表格。

### 第 4 堂：它怎麼每次都忘記

本堂 Lv：**Lv5 Memory**。對齊物是神通 Session，不是本機 `message_history`。換 session 失憶，用來證明這是短期。長期資料不叫 Memory 升級，叫第 9 堂的 Data。

核心問題：短期記憶和「產品要長期記住的資料」不是同一件事。

解鎖：神通 Session。同一條 session 連續對話會記得；換一條就失憶。這是 short-term。

當堂：主線跑完一輪（查空檔 → 預留 → 接著問剛訂了哪）。用同一 session。對照「新開 session」會怎樣。

Long-term（誰已借走哪一格）先點名，實作放到第 9 堂。若當堂要演「依既有占用改建議」，用老師準備的假占用表，不要假裝 Session 會永遠記得。

### 第 5 堂：複雜任務一次做不完

本堂 Lv：**Planning**。Dungeon 沒有這一關，不要順手叫 Lv7 或 Lv8。Lv7 Decision 的產品版是第 8 堂；Lv8 Coding 是第 6 堂才開場。

核心問題：大任務怎麼拆成可檢查的步驟？

解鎖：步驟。先寫在同一個 LLM 的 instruction（了解需求 → 查 → 整理 → 做 → 檢查 → 輸出）。再打開畫布，認五塊編排積木。

當堂：

1. 把 v0.1 改成「必須依步驟走，每步可看出來」（主線，仍是一塊 LLM）。
2. 老師用同一題拼一次對照：SEQ（先查再登記）、PAR（兩間教室同時查）、LOOP（沒空就換下一個午休再查）、RTR（空就准、衝突就改推）。學生填一張表：哪塊在做順序、並行、重複、分流。
3. 進階組才把「了解／執行」拆成兩個 LLM，用 SEQ 串起來。PAR／LOOP／RTR 看過就收，不要當作業。

RTR 只認臉。真正的決策瞬間（衝突不准、人按確認才鎖定）還是第 8 堂。

第二段結束檢查：學生能講自己的 Agent 用了什麼身份、什麼工具、記憶存在哪、步驟是什麼，並指認 LLM／SEQ／PAR／LOOP／RTR。還不能要求他們會組 MCP。

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

當堂案例用「聊天框答應幫你登記」對「真的在判斷的助理」：問需求 → 查占用 → 衝突就改推或拒絕 → 人確認才鎖定。Web App v2 必須能指出一次**決策瞬間**（例如同時段已有人就不准）。鎖定／取消教室做成確認鈕，對應神通的 tool confirmation 或你們自己的按鈕。

評：拿掉對話框之後，若只剩靜態頁，退回重做。

### 第 9 堂：模型知道很多，你們的資料在哪

核心問題：為什麼這不是 ChatGPT 套殼？

解鎖其一即可，不要全做：自己的 JSON／CSV、小資料庫、外部 API、神通 RAG（上傳該組真正在用的檔）。

當堂：Agent 經工具讀寫**這組產品的資料**。教室時段表必須是他們的 `rooms.json`，不是模型猜「那間應該沒人」。

Session 仍是對話短期記憶。誰借走哪一格進自己的資料，再讓工具去碰。

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

現場至少一次：**Agent 做出判斷或行動**。例如同時段衝突時拒絕或改推，而且依據看得到（占用表或 tool 結果）。

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
- 第 5 堂帶過畫布五塊（LLM／SEQ／PAR／LOOP／RTR）；作業主線仍是單塊 LLM，進階才交 SEQ。PAR／LOOP／RTR 不交。
- 第 6–7 堂才出現 Router；第 6 組裝、第 7 通話。
- Agent User 壓成第 1 堂；改 instruction 改列 Builder 第 2 堂。
- 第 11–12 堂收在 Product Builder 裡，不再另立第五段角色，避免曲線和課表對不齊。
