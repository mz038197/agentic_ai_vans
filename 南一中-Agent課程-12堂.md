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

第 1 堂仍是 User，內容另有安排，本稿不寫該堂教案。

舊第 1 堂教室登記那套（用老師 App 走一輪、兩套身份對照、Idea Bank 鉤子）整段併進第 2 堂開場。第 2 堂角色仍是 Builder：開場先當一次使用者，接著自己改 instruction。

---

## Agent Builder 定義

**Agent Builder 是改 Agent 本身的人，不是寫產品網站的人。**

當堂目標一句話：I can build an Agent.

改的對象是神通上的 App：它是誰、會呼叫什麼、對話記在哪、任務怎麼拆。產出是一支比較能做事的 Agent，不是一個 repo。

算 Builder：

- 改 Role／Goal／Instruction／Constraints
- 在自己的 LLM 上勾老師已建好的工具，並改何時該呼叫
- 用 Session 當短期記憶，並能說出換 session 會怎樣
- 把複雜任務寫進步驟（仍是單一 Agent）

不算 Builder：

- 只用現成 Agent、不改任何設定（那是 User）
- 在 VS Code 寫網頁、拆 Spec、用 AI 改檔（那是 AI Coder）
- 想產品給誰用、決策瞬間夠不夠（那是 Product Builder）

第 2–5 堂。不開 VS Code 當主場地。

**天花板（第 5 堂結束；Planning 在第 4 堂交件）：** 一支神通 Agent，有自己的身份、學生自己掛上老師建好的時段工具與貼海報工具、會在對的時候呼叫、同一條 Session 記得這輪對話。第 4 堂把登記助理升級成畫布：SEQ／PAR／LOOP／RTR 都要跑過，看板看得到占用和海報。學生能講「我改了什麼、它因此做了什麼」。

到此為止，不是 coding 能力。未包含：自寫 MCP／API Server、`run_sse` 客戶端、VS Code、學生產品網頁、自己的資料庫／RAG。課室看板仍是老師的站。Coder 是第 6–7 堂，產品決策瞬間是第 8 堂。

舊版從零一路走到 Router 寫碼，Builder 和 Coder 是同一條坡。新版在第 5 堂切斷：神通 Builder 交的是「會改 Agent」，不是「會做軟體」。

對齊 Agent Dungeon 的**能力層名稱與編號**，不對齊上課順序，也不對齊「學生自己寫 Python」。Lv1–3 神通已經給了。第 1 堂另有 User 安排，不重做教室登記。舊第 1 堂那套 Lv1–3 體驗改在第 2 堂開場走一次，然後才進 Builder。

| 堂 | 本堂 Lv | 學生實際改的 | 不做（留給後面） |
|---|---|---|---|
| 2 | **Lv4 Identity** | Role／Goal／Instruction／Constraints | 工具 |
| 3 | **Lv6 Tools**（順帶 **Lv5 Memory** 指認） | 自己把時段工具掛上 LLM；改何時呼叫。用同一筆／新開對話對照：聊天忘了，占用表還在 | 不建 API Server、不填 `base_url`、不寫 MCP／OpenAPI。完整 Observe→Decide→Act 是 Lv7，第 8 堂。長期占用表／DB／RAG 仍是第 9 堂 |
| 4 | **Planning**（Dungeon 沒有獨立關卡） | 同一支登記助理升級：SEQ 先查再訂；空則 PAR 訂＋寫招生海報；LOOP 海報改到能貼再 `post_poster`；滿則 RTR 換週三再查 | 不要叫 Lv8。產品決策瞬間與確認鈕仍是第 8 堂。不在 API 裡自動改推 |
| 5 | **待定** | 原 Planning 已換到第 4 堂。本格主題未定 | — |

編號會跳：2→4、3→6，Memory 不再單獨占一堂。跟學生講「這堂練的能力叫什麼」，不要講「我們在衝 Dungeon 第幾關」。

### 兩種積木，不要混

能力積木是 Lv：Identity、Tools、Memory、Planning。編排積木是神通畫布上的型別，API 叫 `llm`／`sequential`／`parallel`／`loop`／`custom`，UI 是 **LLM／SEQ／PAR／LOOP／RTR**。

| 畫布 | 一句話 | 哪堂帶 | 學生交什麼 |
|---|---|---|---|
| LLM | 一塊會想、會講、可掛工具的代理 | 第 2 堂從零就建這個 | 第 2–3 堂主線；第 4 堂起當子塊 |
| SEQ | 子代理照順序走完 | 第 4 堂 | 先查再訂 |
| PAR | 子代理同時跑 | 第 4 堂 | 確定有空之後，同時訂教室與寫招生海報 |
| LOOP | 同一段重複 N 次 | 第 4 堂 | 海報改到能貼（不是拿來換日期） |
| RTR | 依條件走哪一條（`custom`） | 第 4 堂 | 第一次查若已滿，換後面的週三午休再查。產品確認鈕仍是第 8 堂 |

第 3 堂工具和對話紀錄都掛在 **LLM** 上，不是新的畫布積木。神通進 App 講話就有 Session，學生不用另外建造。

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

第 1 堂只當使用者，內容另有安排。第 2 堂是 Builder，但開場先做完舊第 1 堂的教室登記使用者體驗，再改 Agent。第 2–5 堂的 agent **住在神通**：改 instruction、選現成工具、用 Session。不在 Python 裡 `bind_tools`。

第 6 堂起進 VS Code。Vans Router 有兩個入口，不要混：

- VS Code MCP：組裝神通上的 App（建 agent、掛工具、改 instruction）
- HTTP：學生網站打進來，Router 代打 login／session／`run_sse`

工具執行在神通。學生後端不跑 tool loop。第 3 堂學生只勾 `check_slot`、`reserve_slot`。第 4 堂再勾老師已建的 `post_poster`。`base_url`／新建 API Server 等學生有自己的 REST 再填（第 7、9 堂）。

本機 `main.py`（Agent Dungeon）只當對照，不當作業主線。

帳號：每生一個神通帳號。Router 用「當堂 login + 連線記憶體 + refresh」，不存全班 `access_token`。練習空間固定，不碰其他 Space。

---

## 12 堂總表

| 堂 | 角色 | 主題 | 本堂 Lv | 當堂解鎖 | Runtime | 當堂產出 |
|---|---|---|---|---|---|---|
| 1 | 使用者 | 另有安排 | 體驗 Lv1–3（不實作） | 分辨 Agent vs Chatbot | （該堂自訂） | （該堂自訂） |
| 2 | Builder | 用現成再寫身份 | 開場體驗 Lv1–3；本堂 Lv4 Identity | Role、Instruction、Constraints | 老師 App → 學生自己的 LLM | Idea Bank 鉤子＋Personal Agent v0.1 |
| 3 | Builder | 它開始會做事 | Lv6 Tools；順帶 Lv5 指認 | 掛現成 Tool、何時呼叫；同一筆／新開對話對照 | 神通 LLM＋老師的預約 API＋課室看板 | 會呼叫時段工具的 Agent；能說聊天和占用表不是同一個抽屜 |
| 4 | Builder | 複雜任務拆開做 | Planning | SEQ／PAR／LOOP／RTR；掛 `post_poster` | 神通畫布＋老師占用／海報 API＋課室看板 | 四層都跑過；看板有占用也有海報 |
| 5 | Builder | 待定 | 待定 | 原 Planning 已換到第 4 堂 | 待定 | 待定 |
| 6 | AI Coder | 用 AI 寫軟體 | Lv8 Coding 起算 | Spec → Task → 寫碼 | VS Code | 產品 Spec + 第一個網頁殼 |
| 7 | AI Coder | 網站接到 Agent | Lv8（接上神通） | Router HTTP、`run_sse` | Web → Router → 神通 | Agent Web App v1 |
| 8 | Product Builder | 不是加聊天框 | Lv7 Decision | Observe→Decide→Act、人在迴圈裡 | 同一套 Web + 神通 | Web App v2（有決策瞬間） |
| 9 | Product Builder | 資料從哪來 | Data（非 Dungeon 關卡） | 自己的 JSON／DB／RAG／外部 API | 神通工具打學生資料 | 有專屬資料的 Agent |
| 10 | Product Builder | 專題 Sprint | — | Product Canvas | 文件 + 原型 | Proposal + 架構圖 |
| 11 | Product Builder | 做出來、測、改 | — | 功能／決策／失敗／亂講 | 專題 repo | Beta |
| 12 | Product Builder | Demo Day | — | Pitch | 現場 | 競賽版 Demo |

---

## 1–9 堂主線：教室時段登記

練習產品固定這一件。人物固定「高一的小明，週三午休要為社團登記視聽教室」。第 10 堂才換他們自己的專題。第 1 堂 User 內容另有安排，不在本稿寫死。舊第 1 堂教室登記體驗改在第 2 堂開場。Idea Bank 第 2 堂寫自己的題，不當堂做專題。

目標句（第 9 堂結束要能 Demo）：小明在網站提出時段 → Agent 先查占用再決定准或改建議 → 衝突出現時畫面看得到這次判斷 → 關掉重開，預約還在。

老師課前備好、九堂共用：

- 一支示範用神通 App（第 2 堂開場全班用）。要真的查時段、擋住衝突，不能只回「好啊你去跟總務說」。
- 同一支的第二套 instruction：嚴格總務 vs 好說話的學長。
- 一支占用＋海報 API（神通打得到的網址）＋ Space 內一個 API Server。第 3 堂先兩支手填 Call API Tool：`check_slot`（教室、日期）、`reserve_slot`（教室、時段、社團）。第 4 堂再加 `post_poster`（社團、教室、日期、時段、文案）。契約仍是 `查空檔`／`預留`，外加 `貼海報`。不要 OpenAPI、不要 MCP、不要天氣當主線。工具本身不自動改推下一格。
- 課室看板（老師的儀表板）：只讀。占用表顯示誰先搶到、後到衝突。另頁或同站一欄顯示已貼海報。網站上沒有預約按鈕。課前一鍵重設：格子和海報一起清。種子：視聽教室下一個週三午休已有社團占用；表上要有後續幾個週三午休（給 RTR 換日）。
- 第 3 堂學生自己把 `check_slot`、`reserve_slot` 掛上 LLM。每組一個不會撞的社團名；API 認的是 `預留`／`貼海報` 傳來的社團，不是神通帳號。同一堂用占用表做對話對照：新開聊天，占用格還在。不要另做記憶 API，也不要新工具去「回想剛訂了什麼」。海報頁第 3 堂可以開著，當堂不要求貼上。
- 第 4 堂學生再掛 `post_poster`，把同一支助理做成 SEQ／PAR／LOOP／RTR。
- 第 5 堂主題待定（原 Planning 已換到第 4 堂）。
- 第 9 堂學生 repo 裡一份 `data/rooms.json`（教室、時段、誰借走）。

| 堂 | 小明這堂碰到什麼 | 當堂只新加 | 還缺、下堂才給 |
|---|---|---|---|
| 1 | User，內容另有安排。不走教室登記產品。 | — | — |
| 2 | 先用老師的登記 App 走完一輪：要視聽教室、看到查過占用、准或被拒。再看老師切兩套身份。然後自己從零建一支 LLM 登記助理，寫成嚴格或好說話，同一題對照。 | 當使用者走完；Identity | 自己那支還是只會講，不會查真的空檔 |
| 3 | 學生把時段工具掛上自己的 LLM，改 instruction 何時呼叫。同一題搶視聽教室：神通要看到 tool，看板要動。接著同一筆問「我剛訂了哪」，再新開一筆問同一句（答不出），看板那格仍亮；新對話若改問「這格有沒有人」去查表，會說有人。 | 掛工具；何時呼叫；指認聊天≠占用表 | 畫布拆步驟、招生海報、換日（第 4 堂）。明天重開、自己的 `rooms.json`（第 9 堂） |
| 4 | 同一支助理加四層：先查再訂；有空則同時訂＋寫招生海報；海報改到能貼再打 API 上看板；第一次若已被占，換後面的週三午休再查，找到再訂＋做海報。 | Planning；SEQ／PAR／LOOP／RTR；`post_poster` | 還在神通對話框裡。人按確認才鎖定是第 8 堂 |
| 5 | （待定。原 Planning 已換到第 4 堂。） | — | — |
| 6 | 為「教室登記網站」寫 Spec。做出有「教室／日期／時段／我的預約」區塊的殼，按鈕是假的。 | Spec、網頁殼 | 殼還不能打電話 |
| 7 | 網站經 Router 打自己的神通助理，畫面上跟它說話。 | `run_sse` | 看起來仍像聊天框 |
| 8 | 同一時段已有人：Agent 不准或改推下一個空檔，網站標出這次判斷。真的鎖教室要按確認。 | 決策瞬間（Lv7） | 重整後預約沒了 |
| 9 | `rooms.json` 住在他們後端。重開網站先讀檔；預留成功就寫回。下週那格還是小明社團的。 | 自己的資料 | 第 10 堂才換專題題材 |

`check_slot`／`reserve_slot` 契約不要換。第 4 堂只加 `post_poster`。第 3 堂天氣是菜單上的雜訊，會把九堂拆成九個故事。

第 8 堂確認鈕是主線：鎖定教室、取消別人的預留，都要人按一下。對應神通 tool confirmation 或網站自己的按鈕。

第 9 堂主線用 JSON，不用 RAG。RAG 留口頭對照：上傳「教室使用規則」是另一種「我們的資料」，時段占用不要塞進 RAG。

---

## 第一段：Agent 使用者（第 1 堂）

角色仍是 User：I can use an Agent。內容另有安排，本稿不寫該堂教案、任務單、產出。

舊稿第 1 堂的教室登記展示不在這裡上，已併進第 2 堂開場。

---

## 第二段：Agent Builder（第 2–5 堂）

### 第 2 堂：同一個模型，不同 Agent

本堂角色是 Builder。開場先做完舊第 1 堂那套使用者體驗，再改 Agent。

本堂 Lv：開場體驗 Lv1–3（不實作）；接著 **Lv4 Identity**。神通上的 Role／Goal／Instruction／Constraints，對齊 Dungeon 的 soul／user，只是寫在 App 後台，不寫 `build_system_prompt`。畫布積木用 **LLM**，不要一開始就拉 SEQ。

核心問題：這個東西跟聊天機器人差在哪？為什麼換 Role／Goal／Constraints，行為就不一樣？我要開始改它。

演進只講到能聽懂即可：

```text
LLM 會回答
→ 加上任務（Instruction）
→ 加上行動（Tool）
→ 加上狀態（還記得現在怎樣）
→ 為了目標持續行動＝Agent
```

當堂順序：

1. 全班用老師做好的神通 App 走完一輪任務（必須看得到一次「它做了什麼」而不只是回話）。這一段不要讓學生改 Agent。
2. 老師切換兩套 instruction、同一題，學生只觀察行為差在哪。
3. 每人寫 Idea Bank。每則：誰、痛點、Agent 要做的判斷、**我剛用完還缺什麼**。
4. 每人（或每組）在神通 UI 從零建 App／Agent（型別 LLM）、選模型、存、確認能說話。再改自己的 instruction，產出 Personal Agent v0.1。對照兩個版本（嚴格總務 vs 好說話的學長）同一題：週三午休視聽教室，記下差異。

「還缺什麼」是後面的鉤子：不會真的做事 → 第 3 堂；一步做不完、要拆畫布 → 第 4 堂。學生自己那支當堂還不會查空檔，這是故意的。聊天和占用表不是同一個抽屜，第 3 堂掛完工具當場對照，不另開一堂。

產出格式固定：Role、Goal、Constraints、Context、Output。另交 Idea Bank。

不做：學生掛工具、自己打 `run_sse`。老師示範那支可以有工具，學生 v0.1 沒有。

### 第 3 堂：它只會講，不會做

本堂 Lv：**Lv6 Tools**。畫布不加新方塊，仍是第 2 堂那塊 LLM。學生要自己掛工具，並改「什麼時候該呼叫」。工具本體（API、API Server、兩支 Call API Tool）老師課前建好。那半步像 Lv7 Decision，本堂不掛那個名字；產品裡的決策瞬間留第 8 堂。

同一堂後半指認 **Lv5 Memory**，不另開一堂。神通進 App 講話就有對話紀錄（Session），學生不用建造。對照物就是第 3 堂那張占用表。海報頁給第 4 堂用，當堂不要求貼上。

核心問題：知道答案和真的做完一件事差在哪？做完之後，聊天裡記得的、網頁上登記走的，是不是同一件事？

解鎖：Tool。流程只畫一輪：選工具 → 執行 → 拿結果 → 再說話。接著用「歷史紀錄／新對話」證明：換聊天只清聊天，不清登記表。

老師課前：

- 占用 API 活著，神通打得到。種子：視聽教室下一個週三午休已被占。能重設。
- Space 裡一個 API Server、兩支手填 Call API Tool：`check_slot`、`reserve_slot`。示範 App 也掛上。
- 課室看板只讀占用表：誰先搶到、後到顯示衝突。沒有「我要預約」按鈕。這不是第 6–9 堂作業。占用表課前開著，後半對照用這一塊。海報欄／海報頁可以同一站，第 3 堂不評貼海報。

學生當堂：

1. 打開自己的登記助理。
2. 把 `check_slot`、`reserve_slot` 掛上這塊 LLM、存檔。
3. 改 instruction：要查才叫 `check_slot`，要訂才叫 `reserve_slot`；預留時填自己的社團名。
4. 跑「小明週三午休借視聽教室」。神通要看到 tool，看板要對得上這次呼叫（訂到或衝突）。
5. 同一筆對話接著問「我剛訂了哪」。要答得出。
6. 左側歷史紀錄新開一筆，再問「我剛訂了哪」。要答不出。看板上那格仍亮著。
7. 這筆新對話改問「這格有沒有人」。若它呼叫 `check_slot`，會說有人。那是又去查表，不是記得你。

每組一個不會撞的社團名。API 認社團字串，不是神通帳號，也不是總務／學長人設。工具不要自動改推下一格。

當堂成功：有 tool 紀錄，看板有對應變化，且能講出第 5–7 步那兩句話差在哪。只改人設、沒掛工具，當沒上。只掛工具、沒做新對話對照，Memory 那半沒過。

天氣當菜單口頭提一句即可，不當堂換主線。占用不要塞進 RAG。不要新工具去回想預約，不要在 API 依對話 ID 存「這輪訂了什麼」。

不做：寫 API、填 `base_url`、新建 API Server、架 MCP、匯 OpenAPI、升 Admin、在老師看板上按預約。`base_url` 留給第 7、9 堂有自己的後端再填。明天重開還在、自己的 `rooms.json`，仍是第 9 堂。

### 第 4 堂：複雜任務一次做不完

本堂 Lv：**Planning**。Dungeon 沒有這一關，不要順手叫 Lv7 或 Lv8。Lv7 Decision 的產品版是第 8 堂；Lv8 Coding 是第 6 堂才開場。原獨立 Session 堂已併進第 3 堂，本格改收原第 5 堂。

核心問題：大任務怎麼拆成可檢查的步驟？畫布上四塊各幹嘛？

解鎖：同一支第 3 堂的登記助理，加四層。不是四張無關作業。老師課前多一支 `post_poster`，占用表要有後續幾個週三午休。看板占用和海報同一站，能一起重設。

海報能貼的規定當堂寫死：社團名、教室、日期、時段、一句招生活動都要有；字數上下限老師訂；不准寫「保證錄取」。LOOP 最多 3 版，第 3 版仍不合格就不要呼叫 `post_poster`。

當堂（同一支 App 往上加，看板當成績單）：

1. **SEQ 先查再訂。** 空的才呼叫 `reserve_slot`。練這層時老師重設一格空的，或指定先查「再下下個週三」。否則種子「下一個週三已被占」，SEQ 快樂路徑會練不成。看板：他們社團亮在訂到的那格。
2. **PAR。** 查完確定空、日期已定，才同時做兩件事：訂教室、寫招生海報。海報文案要帶這次的社團、教室、日期、午休。沒訂成功就不要寫。
3. **LOOP。** 海報還沒到能貼就重寫。這圈只打磨文案，不拿來換日期。合格才呼叫 `post_poster`。看板：海報出現在該格旁邊或海報頁，掛在訂到的那一格，不是種子被占的那格。
4. **RTR。** 第一次查若已滿：同一間視聽教室、同一個午休，改查再下一個週三，還滿再下一個，最多再查 3 個週三。中間找到空，接回第 2～3 步（訂＋海報＋能貼才貼上）。3 次仍滿，停下來告訴小明這幾個午休都不行，不要亂訂、不要貼海報。看板：種子那格仍是別人；他們社團和海報在更後面的週三。

兩圈 LOOP 不要揉成一顆：換日是 RTR 滿了才走的那岔；改海報是文案圈。

`check_slot` 只答有沒有人，`reserve_slot` 只訂傳進去的那格，`post_poster` 只貼文案。換日、重寫、合不合格，都是畫布在做。

當堂成功：四層都跑過；占用表和海報對得上最後訂到的那格。只改 instruction、畫布還是單塊 LLM，當沒上。

不做：學生寫 API、填 `base_url`、新建 API Server、在看板上按預約或手動貼海報。第 8 堂才是網站標出判斷、人按確認才鎖定。這裡換日並訂成，是 Builder 的分流。

### 第 5 堂：待定

原「複雜任務／畫布五塊」已換到第 4 堂。本格主題未定。

第二段結束檢查（第 4 堂後先用這份；第 5 堂有新內容再補）：學生能講自己的 Agent 用了什麼身份、什麼工具、記憶存在哪、步驟在畫布哪幾塊，並指認 LLM／SEQ／PAR／LOOP／RTR。還不能要求他們會組 MCP。

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

- 第 3 堂：老師建占用 API＋API Server＋兩支 Call API Tool＋課室看板；學生自己掛上 LLM 並改何時呼叫。不填 `base_url`。看板不是學生產品。掛完工具當場用占用表對照新開對話：聊天忘了，格子還在。自訂 API Server 延到第 7、9 堂。
- 第 4 堂：原 Session 堂取消後，改收 Planning。同一支助理交 SEQ／PAR／LOOP／RTR；加 `post_poster`；看板看占用也看海報。長期資料仍是第 9 堂。產品確認鈕仍是第 8 堂。
- 第 5 堂待定。
- 第 6–7 堂才出現 Router；第 6 組裝、第 7 通話。
- 第 1 堂仍是 User，內容另有安排，本稿不寫。舊第 1 堂教室登記內容（走完老師 App、兩套身份、Idea Bank）整段併進第 2 堂開場。第 2 堂角色仍是 Builder，開場之後才從零建 LLM、改 instruction。
- 第 11–12 堂收在 Product Builder 裡，不再另立第五段角色，避免曲線和課表對不齊。
