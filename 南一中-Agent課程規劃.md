# 南一中 Agent 課程規劃

## 課程定位

本課程以 **Agent 的理解、製作與產品化** 為主軸，搭配 Vans 自建的 Router，預設串接神通科技提供的 API。

最終目標不是只讓學生學會呼叫模型，而是讓每組學生完成一個：

> **真正結合 Agent 能力、可作為專題參賽的產品應用。**

整門課同時以 **AI Coding** 作為開發流程，讓學生逐步培養：

- 問題定義
- 需求拆解
- Agent 設計
- 軟體開發
- 測試與迭代
- 產品思維
- 專題簡報與 Demo

---

## 學生成長曲線

**Agent 使用者 → Agent Builder → AI Coder → Product Builder → Project Team**

這條成長曲線作為整門課的主骨架。

### 1. Agent 使用者

學生先理解：

- Agent 與 Chatbot 的差異
- LLM 能做什麼
- Prompt / Instruction 如何改變模型行為
- 什麼樣的問題適合交給 Agent

目標：

> I can use an Agent.

### 2. Agent Builder

學生開始理解並實作：

- Tool
- State
- Memory
- Workflow
- Planning

目標：

> I can build an Agent.

### 3. AI Coder

學生開始把 AI 當成開發夥伴，學習：

- 需求描述
- Spec
- Task 拆解
- AI Coding
- Debug
- Iterate

目標：

> I can build software with AI.

### 4. Product Builder

學生開始思考：

- 誰是使用者？
- 解決什麼問題？
- 為什麼需要 Agent？
- Agent 在產品中做了什麼決策？
- 需要哪些 Tools / Data？
- 如何形成使用者流程？

目標：

> I can design an Agent product.

### 5. Project Team

學生完成：

- 專題實作
- 測試
- 評估
- Demo
- Pitch
- 競賽作品整理

目標：

> I can ship and present a product.

---

# 核心教學理念

## 不是先學完整技術，再做專題

本課程採用：

> **在做產品的過程中遇到問題，再解鎖對應的 Agent 技術。**

例如：

### 「它只會回答，不能真的做事」

→ 解鎖 **Tools**

### 「它每次都忘記我」

→ 解鎖 **State / Memory**

### 「複雜任務一次完成不了」

→ 解鎖 **Workflow / Planning**

### 「模型不知道我們自己的資料」

→ 解鎖 **Database / RAG / External Data**

因此 Tool、Memory、RAG、Workflow 都不是因為「Agent 課程應該教」，而是：

> **產品需要，所以我們才學。**

---

# Agent 專題判斷原則

學生作品不能只是：

> 一個網站 + 一個 ChatGPT 聊天框

核心判斷標準：

> **如果把 Agent 拿掉，產品功能幾乎沒有差異，就不算真正的 Agent 專題。**

學生必須能回答：

1. 你們解決什麼問題？
2. 誰會使用？
3. 為什麼需要 Agent？
4. Agent 做了什麼判斷或決策？
5. 使用了哪些 Tools？
6. 使用了哪些 Data？
7. 和一般 ChatGPT 有什麼不同？

---

# 技術底座

預計架構：

```text
Student App
    ↓
Vans Router
    ↓
神通科技 API
    ↓
LLM
```

之後再逐步加入：

```text
User
 ↓
Web UI
 ↓
Backend
 ↓
Vans Router
 ↓
LLM
 ↓
Tools / Data / Memory
```

Router 的定位是：

> **幫學生隱藏 Provider、API Key、模型切換等底層複雜度，讓學生把注意力放在 Agent 與產品本身。**

---

# 12 堂課初版規劃

| 堂次 | 學生角色 | 核心主題 | Agent 能力 | 專題能力 | 當堂產出 |
|---|---|---|---|---|---|
| 1 | Agent 使用者 | Agent 到底是什麼？ | Agent vs Chatbot、Goal、Action | 發現生活問題 | 第一個 Agent 體驗 + Idea Bank |
| 2 | Agent 使用者 | 從 Prompt 到 Agent | Role、Goal、Instruction、Context | 描述需求 | Personal Agent v0.1 |
| 3 | Agent Builder | Agent 開始會做事 | Tool Calling | 功能拆解 | 具備 Tool 的 Agent |
| 4 | Agent Builder | Agent 如何記住事情 | State / Memory | 使用者流程 | 有狀態的 Agent |
| 5 | Agent Builder | Agent 如何完成複雜任務 | Workflow / Planning | 任務拆解 | 多步驟 Agent |
| 6 | AI Coder | 用 AI Coding 開始做產品 | Spec → Code → Debug | 需求規格 | 第一版 Web App |
| 7 | AI Coder | Agent × Web Application | Frontend / Backend / Router / API | 系統架構 | Agent Web App v1 |
| 8 | Product Builder | 有 Agent 不代表好產品 | Agentic UX / Human-in-the-loop | 使用者體驗 | Agent Web App v2 |
| 9 | Product Builder | Data × Agent | RAG / Database / External Data | 資料設計 | 有資料來源的 Agent |
| 10 | Product Builder | 專題設計 Sprint | Agent Product Design | Product Thinking | Proposal + Prototype |
| 11 | Project Team | Build & Iterate | Debug / Evaluation / Guardrails | 測試與迭代 | 專題 Beta |
| 12 | Project Team | Demo Day | Agent Evaluation | Pitch / Demo / Storytelling | 競賽版專題 Demo |

---

# 第一階段：Agent 使用者

## 第 1 堂：Chatbot → Agent

### 核心問題

> 什麼時候我們需要 Agent？

概念演進：

```text
LLM
↓
回答問題

LLM + Instruction
↓
有任務

LLM + Tool
↓
能做事

LLM + State
↓
知道目前狀態

Agent
↓
為了目標持續採取行動
```

### 當堂任務

讓每位學生建立自己的：

**Agent Idea Bank**

例如：

- 讀書規劃 Agent
- 英文錯題 Agent
- 社團器材管理 Agent
- 校園導覽 Agent
- 健身 Agent
- 行程規劃 Agent

---

## 第 2 堂：Prompt → Agent Identity

學生理解：

> 同一個模型，因為 Goal、Role、Context、Constraints 不同，會形成不同的 Agent 行為。

核心元素：

- Role
- Goal
- Constraints
- Context
- Output

產出：

**Personal Agent v0.1**

---

# 第二階段：Agent Builder

## 第 3 堂：它只會講，不會做

問題情境：

> Agent 什麼都知道，但什麼都不能真的做。

解鎖：

**Tool Calling**

流程：

```text
Agent
 ↓
選擇 Tool
 ↓
Tool 執行
 ↓
取得結果
 ↓
Agent 繼續回答 / 行動
```

可使用工具：

- Calculator
- Search
- Weather
- Todo
- Quiz
- Database Query
- 自訂 Function

---

## 第 4 堂：它怎麼每次都忘記？

解鎖：

**State → Memory**

先理解 State：

```text
目前等級：3
錯題數：5
學習進度：70%
```

再延伸：

- Short-term State
- Long-term Memory

產品案例：

**英文學習 Coach**

Agent 根據學生歷史錯誤，調整下一輪練習。

---

## 第 5 堂：複雜任務怎麼辦？

解鎖：

**Workflow / Planning**

例如：

```text
了解需求
↓
查資料
↓
整理資訊
↓
執行任務
↓
檢查結果
↓
輸出
```

本階段先以：

> **Single Agent + Tools + State + Workflow**

為主，不急著導入 Multi-Agent。

---

# 第三階段：AI Coder

## 第 6 堂：AI Coding Workflow

教學生建立固定開發流程：

```text
Idea
 ↓
Problem
 ↓
Requirement
 ↓
Spec
 ↓
Tasks
 ↓
AI Coding
 ↓
Run
 ↓
Debug
 ↓
Improve
```

避免：

> 幫我做一個 XXX 網站。

改成先拆：

- User
- Problem
- Core Flow
- Features
- MVP
- Constraints

---

## 第 7 堂：Agent × Web App

讓學生第一次理解完整系統：

```text
User
 ↓
Web UI
 ↓
Backend
 ↓
Vans Router
 ↓
神通 API
 ↓
LLM
 ↓
Tools / Data
```

核心認知：

> **我做的不是 AI Demo，而是一個 System。**

---

# 第四階段：Product Builder

## 第 8 堂：不是加 Chatbox 就叫 Agent

比較：

### 普通 AI 功能

```text
Input
↓
AI
↓
Output
```

### Agentic Product

```text
Observe
↓
Decide
↓
Act
↓
Receive Result
↓
Decide Again
```

案例：

### 普通作文批改

輸入作文 → AI 回答

### Agentic 英文學習 Coach

```text
分析作文
↓
找出弱點
↓
產生練習
↓
學生作答
↓
再次分析
↓
調整下一輪內容
```

---

## 第 9 堂：Data × Agent

目的：

> 避免所有作品最後都變成 ChatGPT Wrapper。

可加入：

- JSON
- CSV
- Database
- External API
- RAG

核心問題：

> 模型知道很多，但你的產品真正有價值的資料在哪裡？

---

## 第 10 堂：Project Sprint

每組建立一份：

# Agent Product Canvas

包含：

### User
誰會使用？

### Problem
解決什麼痛點？

### Agent Goal
Agent 的任務？

### Agent Loop
如何 Observe → Decide → Act？

### Tools
需要哪些工具？

### Data
需要哪些資料？

### MVP
最小可行版本？

### Why Agent?
為什麼不是普通程式？

產出：

- Proposal
- Prototype
- Project Architecture

---

# 第五階段：Project Team

## 第 11 堂：Build → Test → Improve

專題測試方向：

### Functional
功能能不能正常使用？

### Agent
Agent 是否做出合理決策？

### UX
使用者是否知道 Agent 正在做什麼？

### Failure
Tool 或 API 失敗時怎麼辦？

### Hallucination
Agent 亂講時怎麼辦？

### Cost
每件事情都需要 LLM 嗎？

逐步帶入：

**Agent Engineering**

---

## 第 12 堂：Demo Day

學生不只介紹技術。

Pitch Flow：

```text
Problem
↓
Existing Pain
↓
Our Idea
↓
Why Agent
↓
Live Demo
↓
Impact
```

Demo 至少要展示一次：

> **Agent 真正做出判斷或決策的瞬間。**

例如：

> 因為學生連續錯三題，所以 Agent 自動調整下一輪練習難度與內容。

---

# 教學核心檢查問題

每學一個 Agent 技術，都必須回答：

> **它解決了產品的什麼問題？**

每堂課結束也可以檢查：

> **學生今天是否更接近下一個角色？**

最終希望學生完成：

```text
Agent 使用者
↓
Agent Builder
↓
AI Coder
↓
Product Builder
↓
Project Team
```

而不是單純完成：

```text
12 堂課
=
12 個 AI 技術名詞
```

---

# 後續待設計

- [ ] 每堂實際時間配置
- [ ] Hook / Mini Lesson / Build / Challenge / Reflection
- [ ] 每堂課的學生任務單
- [ ] 每堂課的程式模板
- [ ] Router 使用方式
- [ ] 神通 API 整合方式
- [ ] 專題評分 Rubric
- [ ] Agent Product Canvas
- [ ] Demo Day 評分標準
- [ ] 競賽作品提交規格
