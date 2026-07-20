# Dataset Shell：學生 Agent 升級與記憶整合計畫

> **修訂註記（2026-07-19）**：長期記憶已從 `peas-agent-runtime` **分拆**為獨立套件 `peas-agent-memory`。Runtime 只負責 Session／LangChain 訊息序列化／契約檢查。Memory 的 API、記什麼、觸發方式、整併策略仍在討論——見 [`peas-agent-memory-scope-discussion.md`](./peas-agent-memory-scope-discussion.md)；本文件對其僅記錄已定邊界與待決題目，不凍結實作細節。Gate A 強制不依賴 memory，見 **§9.0**。  
> **同日補充（反悔）**：**不**支援 `peas-agent-core`；Shell 只認 `create_agent` + runtime（§1.8）。Session JSONL 仍只**格式**對齊 core，非套件依賴。  
> **同日補充**：已納入審查發現的六項風險凍結決策，見 **§1.6**。  
> **同日補充**：本地舊檔 `agent_core.py:Agent.from_env` **移除**；Shell 只認學生 `create_agent`（§1.8）。  
> **同日補充**：Dataset Shell 的 context 注入**對齊 Agent Studio Shell**：穩定環境進 **system**（`host_context`）、頁面快照進 **user**（`【目前頁面狀態】`）。見 **§1.7**、**§7.4**。  
> **同日補充**：`agentic_ai_vans` 參考重構**只改複本**；**禁止修改**既有 [`main.py`](main.py)。見 **§6.0**。  
> **同日補充**：Gate A 學生參考 **`main_shell` 先不支援附圖**；`image_path is not None` 必須明確 raise（§1.6 P2-1）。目標是讓學生檔保持短、好抄。

## 0. 文件用途

本文件是可交給其他 Agent 直接執行的工程計畫。它整理了以下專案之間的整合方式：

- `agentic_ai_vans`：目前的學生 Agent 參考專案
- `dataset-streamlit-shell-installer`：安裝 Dataset Streamlit Shell 的專案
- 新增的輕量執行期套件（暫名）`peas-agent-runtime`：**Session 與契約**（必裝）
- 新增的長期記憶套件（暫名）`peas-agent-memory`：**可選／規格討論中**

本計畫只走一條接線（見 §1.8）：

- **學生手寫 Agent**：`create_agent` + `peas-agent-runtime`；**不得**要求學生依賴 `peas-agent-core`；Shell **不**提供 core adapter。

目標仍是讓學生能把自己寫過的 Agent 接上 Shell。長期記憶另以獨立模組提供，不塞進 runtime。

---

## 1. 已確定的產品決策

### 1.1 學生只需要理解一個 Shell 入口

一般學生專案在根目錄 `main.py` 提供（**本 vans 參考專案例外**：複本 `main_shell.py`，原 `main.py` 不動，見 §6.0）：

```python
def create_agent(session_path=None, host_context=None):
    return student_agent
```

回傳的物件必須提供：

```python
def chat(
    self,
    user_text: str,
    *,
    image_path: str | None = None,
    on_token=None,
) -> str:
    ...
```

Dataset Shell 透過 `main:create_agent`（或 vans 的 `main_shell:create_agent`）建立 Agent，不讀取 LLM／tools 內部細節；傳入 `host_context`。CLI 可只呼叫 `create_agent()`（`host_context=None`）。**不提供** `peas-agent-core` 載入路徑（§1.8）。

### 1.2 學生保留 Agent 的核心學習內容

學生負責：

- 建立 LLM
- 撰寫 system prompt（含如何把 Shell 傳入的 `host_context` 併入 system，見 §1.7）
- 選擇與建立 tools
- 建立 `create_agent(session_path=None, host_context=None)`
- 把已完成的 ReAct/tool-calling 迴圈整理進 `chat()`
- 正確理解與加入 `HumanMessage`、帶有 `tool_calls` 的 `AIMessage`、`ToolMessage`

### 1.3 我們提供的工程基礎設施（分套件）

**`peas-agent-runtime`（接 Shell 必備）：**

- Session JSONL 讀寫
- LangChain message 的序列化與反序列化
- 保留 `tool_calls`、`tool_call_id` 等必要欄位
- 安全寫檔與損壞檔案錯誤訊息
- Session 路徑驗證
- Shell 契約檢查

**`peas-agent-memory`（可選，規格討論中）：**

- 長期記憶的儲存、查詢與（未來）整併介面
- **記憶條目的序列化／schema 自管**（不放在 runtime）

**`dataset-streamlit-shell-installer`／Shell：**

- Dataset Shell 的 Agent 載入器與 UI
- 只載入學生 `create_agent`（§1.8）；不支援 `peas-agent-core`

### 1.4 套件邊界（已定）

| 能力 | 歸屬 |
|---|---|
| Session／LangChain 訊息序列化 | `peas-agent-runtime`（**格式對齊 core，實作不依賴 core**） |
| 記憶條目序列化／schema | `peas-agent-memory` |
| `create_agent`／`chat` 契約檢查 | `peas-agent-runtime` |
| ReAct／`chat()` 迴圈 | 學生 `main.py`（不進老師套件黑箱） |

Session 與 memory 不為「都是 JSONL」強行共用 serializer。若之後 I/O 重複過多，最多另抽薄層原子寫檔 helper；第一版各套件各自實作即可。

### 1.5 不採用的方案

- **學生路徑**不要求依賴 `peas-agent-core`；runtime codec **格式對齊** core，但 runtime 本身不 import core
- **不把長期記憶實作放進 `peas-agent-runtime`**
- 不另發明與 core 不相容的 Session schema（例如早期草案的 `schema_version` + `type: human|ai|tool`）
- 不保留本地舊檔 `agent_core.py:Agent.from_env`（§1.8）；**不**改以 `peas-agent-core` 替代
- 不要求學生從零實作 Session JSONL codec、檔案鎖、資料遷移
- 不把完整 `chat()` 黑箱化到老師套件，否則學生原先寫過的 ReAct 迴圈失去意義
- 不以 AST 或文字替換任意改寫未知版本的學生 `main.py`
- 不讓 Shell 與 Agent 同時寫入同一份 Session JSONL
- 不把穩定 Dataset 環境說明整包只塞進 user、不進 system（須對齊 Studio 兩層，§1.7）
- 不在第一版（含 memory 定案前）加入 embeddings、向量資料庫或複雜記憶評分

### 1.6 審查風險凍結決策（P1／P2）

以下六項為計畫審查發現的缺口；**實作必須遵守本節，不得自行另解。**

#### P1-1 契約檢查不得需要 API key

**問題：** 若 `check_agent_factory` 為驗證「回傳物件有 `chat`」而呼叫 `create_agent()`，學生常在 factory 內建立 `ChatOpenAI`，Installer／CI 會被迫要 API key。

**凍結：**

- **預設（Installer 與一般模式）**：只做 import + signature 檢查  
  - 可 import `main`  
  - 存在 callable `create_agent`  
  - 接受 `session_path`、`host_context`（keyword 或相容 signature；見 §1.7）  
  - 若模組內可取得 Agent 類別／型別註解，檢查 `chat` 的 signature（含 `user_text`，相容 `image_path`、`on_token`）  
  - **禁止**呼叫 `create_agent()`、**禁止**呼叫 `chat()`、**禁止**打 LLM
- **可選深檢** `check_agent_factory(..., invoke=True)` 或 CLI 旗標：才實例化 factory；文件必須註明「可能需要 API key／`.env`」；單元測試用 fake／monkeypatch，不得依賴真實金鑰
- 參考教材可建議「LLM 延遲到第一次 `chat()` 再建」，但**不得**把 lazy-init 當契約硬性要求

#### P1-2 Session 唯一寫入者

**產品決策：** Shell 只走 `create_agent`（§1.8）；**移除**本地 `agent_core.py:Agent.from_env`。

**凍結：**

- 同一進程、同一 session 檔，只允許**一個**訊息寫入者
- **唯一寫入者** = 學生 Agent 內的 `SessionStore`（runtime）
- Shell 對訊息 JSONL 只做：**建立空檔／列舉／刪除／read 供 UI 顯示**；不得在 Agent 回覆後再寫入 user/assistant 列
- 不得同時啟用兩種 adapter 寫同一檔；UI 顯示目前 adapter
- 同一 session 檔仍不要多開 CLI／Shell 同時寫（見 P2-2）

#### P1-3 Session 路徑邊界凍結

**問題：** 計畫只寫「Session 路徑驗證」，未定義合法路徑規則，Shell 與 runtime 可能不一致。

**凍結（與現有 Dataset Shell 對齊並寫進 runtime）：**

- Shell 傳入 `create_agent(session_path=...)` 的值為**相對於專案根目錄**的相對路徑字串，且必須：
  - 以 `.jsonl` 結尾
  - path parts 含 `sessions`（例：`dataset_streamlit_shell/sessions/session_YYYYMMDD_HHMMSS_xxxxxx.jsonl`）
  - resolve 後落在專案根目錄之下（禁止 `..` 逃逸）
  - 指向的檔案在啟用 Agent 時必須已存在（由 Shell 先 `touch` 建立空檔）
- Runtime `SessionStore`：
  - `path=None`：記憶體模式，不寫檔
  - `path` 為相對或絕對皆可，但若由 Shell 呼叫，應傳上述相對路徑；runtime 以專案根（或明確 `base_dir`）resolve
  - 拒絕逃逸路徑；錯誤訊息需可教學（說明合法形式）
- CLI 教學階段可用 `path=None`，不強制 sessions 目錄規則

#### P2-1 圖片不可靜默忽略（Gate A：先不支援附圖）

**問題：** 參考骨架 `chat(..., image_path=None)` 若只當純文字處理，Shell 傳 `image_path` 時圖會被靜默丟掉。

**凍結（Gate A／`main_shell` 教學版）：**

- **先不支援附圖**：`image_path is not None` 時必須 **raise** 明確錯誤（例如 `NotImplementedError("尚未支援 image_path")`）
- **禁止**假裝成功、只存文字、或略過參數
- `chat` signature **仍保留** `image_path=None`（契約相容；Shell 可繼續傳）
- 契約檢查不要求真的處理圖片；只要求 signature 相容
- Runtime Session codec **仍可** round-trip 含 `image_path` 的 JSONL（格式能力保留）；學生參考 Agent 不實作寫入附圖列
- 附圖完整支援（history + 送模）列為後續里程碑，不進 Gate A 學生必讀檔

#### P2-2 原子寫入仍可能遺失更新

**問題：** 暫存檔 + replace 只防半份檔，不防兩個寫入者 last-write-wins，或「讀-改-寫」覆蓋。

**凍結：**

- 第一版 **不**做跨行程檔案鎖；以 **單一寫入者**（P1-2）為主防護
- 文件與教師除錯說明必須寫明：同一 session 不要多開 Shell／CLI 同時寫
- `SessionStore.save` 重寫整檔前，以該 store 實例內的 history／meta 為準；不在第一版做合併式 concurrent update
- 若未來需要多寫入者，另立計畫（檔案鎖或單一 writer 服務），不在本垂直切片範圍

#### P2-3 「可發布」≠「整體計畫完成」

**問題：** M6 寫「Session 垂直切片驗收後即可發布 Runtime／Installer tag」，易被當成整份升級計畫 DoD 已完成。

**凍結：**

- **可發布（release gate A）**：§12.1 Session 垂直切片 + M0–M3、M5、M6（不含記憶必驗）通過 → 可打 runtime／installer tag
- **整體計畫完成（release gate B）**：另含 §5／M4 memory 定案與實作、§12.2，以及文件中記憶教材——**未完成前不得宣稱「記憶整合計畫全部完成」**
- README／changelog 發布用語必須區分「Session／Shell 接線可用」與「長期記憶可用」

### 1.7 Context 注入對齊 Agent Studio Shell（已定）

對照 `agent-studio-installer` 的 `studio_shell`：**兩層注入，不要全部塞進 user。**

| 層 | Studio | Dataset（本計畫） | 進哪裡 |
|---|---|---|---|
| 穩定主機／環境說明 | `studio_base_context()` → `Agent.create(host_context=...)` → core `build_system_prompt` 的 `# Host Environment` | Shell 組 `dataset_base_context()`（或同等），呼叫 `create_agent(..., host_context=...)` | **System**：學生 Agent 併入自己的 system prompt |
| 當頁變動快照 | `format_extra_context(...)` → 每則 `【目前頁面狀態】` + `使用者問題：` | 頁面／資料集當下狀態 → 同樣格式組進本輪 `chat()` 字串 | **User**：本輪 HumanMessage |

**凍結規則：**

1. **System 層（`host_context`）**  
   - 內容：路徑慣例、working/ready/original 規則、scripts 目錄、cleaning log 約定、工具使用原則等**相對穩定**的 Dataset 環境說明（從現有 `dataset_context()` 中拆出「環境規則」部分）。  
   - 建立 Agent 時傳入一次；Agent 快取期間沿用。  
   - 學生參考實作必須把非空的 `host_context` 併進 system（建議標題 `# Host Environment`，與 Studio／core 用語對齊）。  
   - **不得**把整包 `host_context` 再重複貼進每一則 user 訊息。

2. **User 層（每輪）**  
   - 有頁面／資料快照時：

     ```text
     【目前頁面狀態】
     {extra_context}

     使用者問題：{使用者真正輸入}
     ```

   - 無 extra 時可僅 `使用者問題：...`（與 Studio 一致）。  
   - `extra_context` 只放**當頁／當下**狀態（欄位列表、目前頁名、工作檔是否已載入等快照）；禁【任務】／長篇指令語氣（對齊 Studio `format_extra_context` 慣例）。  
   - UI 顯示給使用者看的仍是短問題；送進 `chat()`／寫入 session 的是組好的字串。

3. **契約**  
   - `create_agent` 必須接受 `host_context` keyword（可預設 `None`）。  
   - 預設契約檢查（不 invoke）須確認 signature 含 `host_context`；缺了要明確提示。  
   - Runtime **不**組裝 Dataset 文案；文案仍由 Shell 產生。

4. **明確廢止**  
   - 廢止「把完整 dataset 環境說明 + 學生問題全部拼進單一 user prompt、且不進 system」的舊 Dataset 做法（現有 `data_ui.py` 的 `prompt = f"{context}\n\n學生問題：{user_text}"` 須在 M3 改成上述兩層）。

### 1.8 Shell 只認 `create_agent`（已定，不支援 peas-agent-core）

Dataset Shell **不提供** `peas-agent-core`／`peas_agent.Agent.create` 載入路徑。與 Agent Studio 的差異：**Studio 用 core；Dataset Shell 只用學生 factory + runtime**。

| 項目 | 凍結 |
|---|---|
| 建立 Agent | `create_agent(session_path=..., host_context=...)` |
| Session 寫入 | `peas-agent-runtime` `SessionStore` |
| 依賴 | **必裝** `peas-agent-runtime`；**不**安裝、**不** import `peas-agent-core` |

**載入順序（凍結）：**

1. 若設定／環境指定 factory（如 `DATASET_SHELL_AGENT_FACTORY=main_shell:create_agent`）→ 使用該 factory
2. 否則若存在合格 `main:create_agent` → 使用
3. 否則 → 未連接；提示實作 `create_agent` 並安裝 `peas-agent-runtime`
4. **永不**呼叫本地 `agent_core.py` 的 `Agent.from_env`
5. **永不** fallback 到 `peas_agent.Agent.create`

**其他凍結：**

- UI 顯示 agent 來源為 `create_agent`（或 factory 字串）；不顯示 core adapter
- Context 仍用 §1.7 兩層（`host_context` → system；頁面快照 → user）
- Installer：**只必裝** `peas-agent-runtime`（不裝 `peas-agent-core`）
- 契約檢查：只驗 `create_agent` signature（預設仍不打 LLM）
- Session JSONL **格式**對齊 core 僅指 on-disk codec 相容，**不是** Shell 依賴 core 套件

---

## 2. 目標學生流程

### 2.1 升級前

學生已有一個可執行的 CLI Agent：

```powershell
uv run main.py
```

其中已有：

- `ChatOpenAI`
- `build_system_prompt()`
- 自訂 tools
- 手寫 tool-calling 迴圈
- 程式執行期間的 `message_history`

### 2.2 學生完成一次小型重構

學生把既有邏輯整理成：

```python
class Agent:
    def chat(self, user_text, *, image_path=None, on_token=None):
        # 學生原本寫過的 ReAct/tool-calling 迴圈
        ...


def create_agent(session_path=None):
    return Agent(...)
```

CLI 與 Shell 必須共用同一個 `create_agent()`：

```python
def main():
    agent = create_agent()
    ...
```

參考重構**預設只接 Session（runtime）**；記憶範例等 `peas-agent-memory` 規格定案後再加。

### 2.3 安裝 Dataset Shell

最終學生只需要執行 Dataset Installer：

```powershell
uvx --from git+https://github.com/mz038197/dataset-streamlit-shell-installer.git add-dataset-streamlit-shell
```

Installer 應自動：

1. 複製 `dataset_streamlit_shell/`
2. 安裝 Dataset Shell 相依套件
3. 安裝 `peas-agent-runtime`（必裝）
4. （可選／後續）安裝 `peas-agent-memory`——**待 memory 規格定案後再決定是否納入預設安裝**
5. 檢查 `main:create_agent`
6. 顯示契約檢查結果
7. 顯示 Shell 啟動指令

啟動方式維持：

```powershell
uv run streamlit run dataset_streamlit_shell/app.py
```

---

## 3. 整體架構

```text
main.py（學生擁有）
├── LLM
├── prompt
├── tools
├── Agent.chat()       ← 學生的 ReAct 核心
└── create_agent()
          │
          ├── 使用 peas-agent-runtime（必備）
          │   ├── SessionStore
          │   ├── MessageCodec      ← Session／LangChain 訊息
          │   └── contract check
          │
          ├── 可選使用 peas-agent-memory（規格討論中）
          │   ├── 記憶條目序列化   ← 自管，不在 runtime
          │   └── remember／recall 等（API TBD）
          │
          └── 被 dataset_streamlit_shell 載入
              ├── Session 選擇
              ├── 對話 UI
              ├── Dataset context
              └── on_token 顯示
```

`dataset-streamlit-shell-installer` 是學生唯一需要知道的安裝入口。  
`peas-agent-runtime` 是接上 Shell／Session 的執行期相依套件。  
`peas-agent-memory` 為可選獨立模組；**第一個可展示垂直切片不依賴它**。

建議目錄布局（Session 與 memory 資料分開；memory 路徑是否沿用下列結構仍待討論）：

```text
dataset_streamlit_shell/
├── sessions/
│   ├── session_001.jsonl
│   └── session_002.jsonl
└── memory/                    ← 由 peas-agent-memory 使用（若啟用）
    └── （格式 TBD）
```

---

## 4. Runtime 套件設計

### 4.1 新專案位置與名稱

建議建立：

```text
C:\Users\mz038\Desktop\peas-agent\peas-agent-runtime
```

Python package：

```text
peas_agent_runtime
```

若實作前需要改名，必須先更新本計畫與 Installer 的 dependency，不可同時存在兩種名稱。

### 4.2 建議檔案結構

```text
peas-agent-runtime/
├── pyproject.toml
├── README.md
├── src/
│   └── peas_agent_runtime/
│       ├── __init__.py
│       ├── contract.py
│       ├── session.py
│       ├── serialization.py
│       └── errors.py
└── tests/
    ├── test_contract.py
    ├── test_session.py
    └── test_serialization.py
```

**不得**在本套件加入 `memory.py` 或長期記憶 API。

### 4.3 `SessionStore`

第一版公開 API（**role 字典**，不把 LangChain 訊息物件交給學生）：

```python
store = SessionStore(path)
history = store.load()  # list[dict]：role / content / timestamp …
history.append({"role": "user", "content": "你好"})  # 不必帶 timestamp
store.save(history)  # 寫檔時補 timestamp（已有則保留）
```

必要行為：

- 公開型別為 `list[dict]`（`role` 為 `user` / `assistant` / `tool`）；**不**對呼叫端洩出 `HumanMessage`／`AIMessage`／`ToolMessage`
- `path=None` 時使用純記憶模式，不寫檔，供 CLI 初學階段使用
- 路徑存在時載入完整歷史（略過首行 metadata，還原訊息列 dict，含磁碟上的 `timestamp`）
- 路徑不存在時回傳空 list
- 建立缺少的父目錄
- 寫入 UTF-8 JSONL（**core 相容**：首行 metadata + 訊息列）
- `save` 時對每則訊息列 **preserve-or-fill** `timestamp`：已有則保留，沒有才補 `datetime.now().isoformat()`（可就地寫回呼叫端 dict）
- 寫檔需採用暫存檔加原子替換，避免半份檔案（防半份檔，**不**防多寫入者互蓋；見 §1.6 P2-2）
- Store 內部保留 `session_meta`（含 `created_at`／`updated_at`／`last_consolidated`），`save` 時更新 `updated_at` 並重寫整檔
- 第一版可不實作 core 的歸檔／consolidate 邏輯；`last_consolidated` 預設 `0`，讀到既有值則原樣保留
- 遇到無效 JSON 或訊息列缺失必要欄位時，拋出具體的自訂錯誤（可比 core 更嚴：core 會略過壞行；runtime **不可靜默丟棄**損壞的訊息列）
- `role == "system"` 與 core 的 SystemMessage 相同：**不寫入** session JSONL
- 路徑驗證規則見 §1.6 P1-3
- LangChain codec（若仍保留）僅供 runtime 內部驗證／相容測試，**不是**學生 `SessionStore` 公開契約

### 4.4 Session 訊息序列化格式（對齊 `peas-agent-core`）

此節僅規範 **Session／LangChain 訊息**。記憶條目序列化見 §5，不屬於 runtime。

**已定：** on-disk 格式對齊 `peas-agent-core` 的 `save_session_jsonl` / `load_session_jsonl`（參考 `peas-agent-core/src/peas_agent/core.py`）。  
**仍禁止** `import peas_agent`／依賴 `peas-agent-core`；在 runtime 內自行實作相容 codec 與測試。

#### 檔案結構

1. **第 1 行**：metadata（`_type == "metadata"`）
2. **其後每行**：一則訊息（`role` 為 `user` / `assistant` / `tool`）

#### Metadata 列

```json
{"_type":"metadata","key":"session","created_at":"2026-07-19T12:00:00","updated_at":"2026-07-19T20:48:19.738792","metadata":{},"last_consolidated":0}
```

| 欄位 | 說明 |
|---|---|
| `_type` | 固定 `"metadata"` |
| `key` | 預設 `"session"` |
| `created_at` / `updated_at` | ISO datetime |
| `metadata` | 物件，預設 `{}` |
| `last_consolidated` | int；runtime 第一版不驅動 consolidate，但須能讀寫保留 |

#### 訊息列

| `role` | 對應 LangChain | 必要／常見欄位 |
|---|---|---|
| `user` | `HumanMessage` | `content`, `timestamp`；可選 `image_path`, `media_type` |
| `assistant` | `AIMessage` | `content`, `timestamp`；有工具時含 `tool_calls: [{name, args, id}]` |
| `tool` | `ToolMessage` | `content`, `tool_call_id`, `timestamp`；可選 `name` |

範例：

```json
{"_type":"metadata","key":"session","created_at":"2026-07-19T12:00:00","updated_at":"2026-07-19T12:01:00","metadata":{},"last_consolidated":0}
{"role":"user","content":"12 × 5 是多少？","timestamp":"2026-07-19T12:00:30"}
{"role":"assistant","content":"","timestamp":"2026-07-19T12:00:31","tool_calls":[{"name":"calculator","args":{"a":12,"b":5,"operation":"multiply"},"id":"call_123"}]}
{"role":"tool","content":"60","tool_call_id":"call_123","timestamp":"2026-07-19T12:00:32","name":"calculator"}
{"role":"assistant","content":"答案是 60。","timestamp":"2026-07-19T12:00:33"}
```

附圖 user（與 core 相同：圖以路徑欄位保存，不把多模態 list content 直接 dump）：

```json
{"role":"user","content":"see this","timestamp":"...","image_path":"images/x.png","media_type":"image/png"}
```

#### 驗收重點

- 與 core 產出之欄位名／`role` 值／`tool_calls` 形狀一致（可交叉用 core 寫出的 fixture 做 load 測試，但測試環境不把 core 當 runtime 依賴）
- `HumanMessage` / 一般 `AIMessage` / 多 `tool_calls` 的 `AIMessage` / `ToolMessage` round trip 後語意等價
- `ToolMessage.tool_call_id` 不可遺失
- tool error 也必須能序列化
- 多模態：採 core 的 `image_path`＋`media_type` 路徑；若收到無法依此規則處理的 list content，必須明確報錯，不可默默轉成字串
- **不**使用計畫早期草案的 `schema_version` + `type: human|ai|tool` 格式

實作者應對照 core 的 `_message_to_jsonl_line` / `_row_to_message` / `_default_metadata` 實作；**不要**改去依賴 LangChain 官方 message dump 當 on-disk 格式（與 core 不一致）。

### 4.5 契約檢查器

Runtime 提供可被 Installer 呼叫的檢查函式或 CLI：

```python
check_agent_factory("main:create_agent")
```

檢查內容與分級見 **§1.6 P1-1**（摘要）：

- **預設**：安全 import、找到 callable factory、`session_path` 與 `host_context` 相容、`chat` signature 相容（含 `image_path`、`on_token`）——**不**呼叫 factory、**不**打 LLM、**不**需要 API key
- **可選 `invoke=True`**：才實例化；可能需要金鑰；測試須 fake
- 契約**不**要求 Agent 依賴 `peas-agent-memory`

---

## 5. `peas-agent-memory`（獨立套件｜規格討論中）

**另開討論文件（主戰場）**：[`peas-agent-memory-scope-discussion.md`](./peas-agent-memory-scope-discussion.md)  
該文件含已定邊界、待凍結勾選清單、草案 API、與 Gate A 的強制分界。  
**未在討論文件勾選凍結前，不開始 M4；不阻塞 M0–M3／M5。**

### 5.1 已定決策

- 專案暫名：`peas-agent-memory`；Python package 暫名：`peas_agent_memory`
- 建議位置：`C:\Users\mz038\Desktop\peas-agent\peas-agent-memory`
- **記憶條目的序列化與 schema 由本套件自管**；`peas-agent-runtime` 不知道 fact／記憶列的格式
- 長期記憶資料與 Session JSONL **必須分開存放**
- 第一版垂直切片（Session ↔ Shell）**不依賴**本套件
- 自動「記憶滿了整併」不在 Session 垂直切片範圍；是否做、何時做，屬本套件討論題

### 5.2 尚未定案（討論區）

細節與草案見 [`peas-agent-memory-scope-discussion.md`](./peas-agent-memory-scope-discussion.md) §2。摘要：

- 要記什麼（facts / preference / summary 等）
- 公開 API 形狀（是否仍採 `remember` / `recall` / `list` / `delete`）
- 觸發方式（明確 API、remember tool、之後才自動）
- 儲存格式與是否沿用 `dataset_streamlit_shell/memory/`
- 是否／何時做 consolidator（含「滿了整併」）
- 與學生教材的最小接點要幾個
- Installer 預設必裝或選裝

定案後：**回填本節為凍結規格**，並改寫 Milestone 4／§12.2。

### 5.3 舊版構想（僅供討論參考，非正式凍結）

下列曾出現在分拆前的草稿，**可當討論起點，不是現行規格**（完整草案見討論文件 §2）：

```python
# 候選 API 形狀（TBD，勿當正式契約）
memory = LongTermMemory(memory_dir)
memory.remember("使用者喜歡簡潔的繁體中文回答", category="preference")
items = memory.recall("回答偏好", limit=5)
memory.list()
memory.delete(memory_id)
```

候選行為方向（同樣未凍結）：append-only、tombstone 刪除、第一版不用 embeddings、不得每輪自動打額外 LLM、自動整併偏後。

---

## 6. 學生 Agent 參考重構

### 6.0 `agentic_ai_vans`：只重構複本，不動原檔（已定）

在本參考專案內：

| 檔案 | 規則 |
|---|---|
| [`main.py`](main.py) | **禁止修改**。保留升級前 CLI／學生現況，供前後對照 |
| `main_shell.py`（新建） | 由複製 `main.py` 後再重構；放 `Agent`、`create_agent`、接 runtime／`host_context` |

凍結：

1. Milestone 2 **不得**改寫、覆寫或「順便整理」原 `main.py`（含移除硬編碼 key 也只做在複本；原檔若含敏感資訊，另以口頭／README 提醒撤銷，仍不直接改原檔）。
2. 本 repo 接 Dataset Shell 時，載入 **`main_shell:create_agent`**（不是 `main:create_agent`）。
3. 一般課堂教材仍可教學生「在自己的 `main.py` 做同樣重構」；**本 vans 專案用分檔示範**，避免毀掉可對照的原版。
4. 單元測試針對 `main_shell`（或自其 import 的模組），不強制改原 `main.py` 的行為。
5. 若實作者想用別的複本檔名，必須先改本節與 Shell 載入設定，且仍遵守「原 `main.py` 不動」。

### 6.1 參考類別骨架

`agentic_ai_vans/main_shell.py`（由 `main.py` 複製後重構）應採用以下概念；實作者不得直接以完整黑箱 `SimpleAgent.chat()` 取代學生 ReAct 邏輯；**不得**把下列完成版寫回原 `main.py`。

```python
class Agent:
    def __init__(self, *, llm, tools, session_path=None, host_context=None):
        self.llm = llm.bind_tools(tools)
        self.tool_map = {tool.name: tool for tool in tools}
        self.host_context = host_context
        self.session = SessionStore(session_path)
        # SessionStore 直接給／收 role 字典；勿在學生檔做 codec
        self.history = self.session.load()

    def chat(self, user_text, *, image_path=None, on_token=None):
        # 對齊 main.py：每輪才 build；訊息用 dict，不組 AIMessage／HumanMessage
        system_prompt = build_system_prompt(self.host_context)
        self.history.append({"role": "user", "content": user_text})

        for _ in range(8):
            response = self.llm.invoke([system_prompt, *self.history])
            tool_calls = getattr(response, "tool_calls", None) or []

            if not tool_calls:
                answer = str(response.content or "")
                self.history.append({"role": "assistant", "content": answer})
                self.session.save(self.history)
                if on_token is not None:
                    on_token(answer)
                return answer

            self.history.append({
                "role": "assistant",
                "content": str(response.content or ""),
                "tool_calls": tool_calls,
            })
            for tool_call in tool_calls:
                result = execute_student_tool(tool_call)
                self.history.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call["id"],
                })

        self.session.save(self.history)
        raise RuntimeError("Agent 工具呼叫次數超過上限。")
```

這只是計畫中的參考骨架。正式實作時必須補齊：

- `build_system_prompt` 回傳 `{"role": "system", "content": ...}`（對齊 main.py；非空 `host_context` 併入 content）
- `host_context` 併入 system（§1.7）；CLI 的 `host_context=None` 時行為與現在相同
- 未知工具也要產生對應的 error tool 字典（`role=tool`）
- 單輪多個 tool calls 必須全部執行後再呼叫 LLM
- 工具例外轉成可理解的 tool 訊息，不可讓 session 留在缺少 tool result 的非法狀態
- `response.content` 非純字串時的文字擷取
- `image_path`：**Gate A 明確 raise，不實作附圖**（§1.6 P2-1）；不得靜默忽略
- 真正 token streaming 可在第二版完成；第一版允許最終答案一次呼叫 `on_token(answer)`，或暫時忽略 `on_token` 僅回傳字串（若忽略，文件須註明；Shell 仍可呼叫）

上方骨架的 `{"role": "user", ...}` 即 Gate A 文字路徑。附圖邏輯**不要**塞進學生必讀的 `main_shell.py`。

記憶相關接點（`recall`／`remember`）等 §5 定案後再加入參考專案；**不得**為了示範記憶而把實作塞進 runtime。

### 6.2 `create_agent()`

```python
def create_agent(session_path=None, host_context=None):
    llm = build_llm()
    tools = [*get_builtin_tools(), calculator]
    return Agent(
        llm=llm,
        tools=tools,
        session_path=session_path,
        host_context=host_context,
    )
```

### 6.3 CLI 共用同一個 factory

```python
def main():
    agent = create_agent()
    while True:
        question = input("你的問題: ").strip()
        if question.lower() == "quit":
            break
        if question:
            print(agent.chat(question))
```

### 6.4 安全要求

原 `main.py` 含硬編碼 API key。依 §6.0 **不改原檔**；在 **`main_shell.py` 複本**中必須：

- 不複製硬編碼 key 進複本（或改為環境變數／`.env`）
- 不在 commit、測試輸出或文件中重複該 key
- 提醒專案擁有者撤銷／更新已暴露的 key（原檔仍可能含舊 key，由擁有者自行處理）

---

## 7. Dataset Shell 修改計畫

主要專案：

```text
C:\Users\mz038\Desktop\peas-agent\dataset-streamlit-shell-installer
```

### 7.1 新增 factory loader

在 Shell template 新增獨立模組，例如：

```text
dataset_streamlit_shell/agent_loader.py
```

責任：

- 預設載入 `main:create_agent`（一般學生專案）
- **`agentic_ai_vans` 參考專案**：載入 `main_shell:create_agent`（§6.0；原 `main.py` 不動）
- 呼叫 `create_agent(session_path=目前 session 路徑, host_context=dataset_base_context())`（§1.7）
- 驗證回傳物件有 `chat()`
- 將 import error、signature error 與 factory runtime error 分開顯示
- 不在 Streamlit rerun 時無限制建立新 Agent；沿用現有 session-state cache 策略
- `host_context` 變更極少；若文案版本變更需清 Agent cache 後重建

載入目標可用環境變數或 Shell 設定覆寫（例如 `DATASET_SHELL_AGENT_FACTORY=main_shell:create_agent`），避免為了 vans 示範改死所有學生專案的預設。

### 7.2 載入契約：只認 `create_agent`

細節見 **§1.8**。摘要：

- `create_agent`／`main_shell:create_agent` + runtime
- **移除**本地 `agent_core.py:Agent.from_env`；若檔案仍在，不載入，提示改實作 `create_agent`
- 載入順序：指定 factory → `main:create_agent` → 未連接
- **不**載入 `peas-agent-core`

### 7.3 Session 單一寫入者

依 §1.6 P1-2、§1.8：

- `SessionStore`（runtime）為唯一寫入者

Shell 可以：

- 使用 Streamlit `session_state` 暫存本次畫面
- 使用 Runtime read 顯示已保存歷史（JSONL 形狀對齊 core-compatible codec）
- 建立、切換、刪除 session 檔案（含先 `touch` 空檔再交給 Agent）

Shell 不可以：

- 用另一種 schema 追加同一份 Agent session JSONL
- 在 Agent 已保存回答後再次將相同 user/assistant 訊息寫入 JSONL
- 透過本地舊 `agent_core.py` 寫入 session

實作者必須盤點現有 `data_ui.py`：移除 `from_env` 路徑，改為只載入 `create_agent`，並消除 Shell 雙重寫入。路徑規則見 §1.6 P1-3。

### 7.4 Dataset context（對齊 Studio 兩層）

細節與廢止舊拼法見 **§1.7**。摘要：

- Shell 實作 `dataset_base_context()`（對齊 Studio `studio_base_context` 的**分層概念**，非 core 依賴）
  - 經 `create_agent(host_context=...)` 進學生 system
- 每輪用 `format_extra_context` 風格的當頁快照 → 組成 `【目前頁面狀態】` + `使用者問題：` 再呼叫 `chat()`
- 從現有 `dataset_context()` **拆分**：穩定規則進 host；動態快照進 extra
- Runtime **不**理解 Dataset UI；文案仍由 Shell 產生

### 7.5 長期記憶 UI

記憶 UI **依賴 `peas-agent-memory` 是否可用**，且不得寫進 runtime 契約。

第一版 Session 垂直切片：

- 若未安裝／未接上 memory：不顯示記憶資訊，或明確顯示「長期記憶未接上」
- 不得因缺少 memory 而讓 Agent／Session 面板失敗

memory 規格定案後的簡易技術資訊（候選）：

- 目前 session 路徑
- memory 目錄
- 記憶筆數

可選的後續 UI：

- 查看記憶
- 手動新增記憶
- 刪除單筆記憶
- 手動執行整併

定案前與第一版皆不得提供容易誤觸的「清除全部長期記憶」按鈕。

---

## 8. Installer 修改計畫

### 8.1 Dependency

在 Installer 的 dependencies 安裝清單：

- **`peas-agent-runtime`（必裝）**
- **`peas-agent-memory`：選裝或後續里程碑再裝**，待 §5 規格定案
- **不**安裝 `peas-agent-core`

開發階段可使用本機 path；發布前必須改成可重現的 tag。

### 8.2 安裝後契約檢查

Shell 複製與 dependencies 安裝完成後：

- 若找到相容的 `main:create_agent`（或設定的 factory）：顯示成功
- 若沒有：Shell 仍可安裝，清楚顯示未連接，並提示 `create_agent` 最小函式與 runtime 安裝
- 若偵測到本地舊 `agent_core.py`：提示已不支援 `from_env`，請改實作 `create_agent`

契約檢查只驗證 runtime／`create_agent` 契約，**不**因缺少 memory 套件而失敗。

建議增加嚴格模式：

```powershell
add-dataset-streamlit-shell --require-agent-contract
```

嚴格模式下若契約不存在，Installer 以非零狀態結束；一般模式仍允許先安裝 UI。

### 8.3 不自動改寫學生程式

第一版 Installer 不修改 `main.py`。可提供：

- 終端機中的最小範例
- README 遷移章節
- 一份可複製的 scaffold

若未來要支援自動改寫，只能針對有明確版本標記的官方 starter，且必須先備份、提供 undo，另立計畫實作。

### 8.4 Update 保留資料

`--update` 必須保留：

- `dataset_streamlit_shell/workspace/`
- `dataset_streamlit_shell/sessions/`
- `dataset_streamlit_shell/memory/`（若目錄已存在；即使 memory 套件尚未定案，也不可在 update 時刪除學生資料）
- `dataset_streamlit_shell/uploads/`
- `dataset_streamlit_shell/scripts/`

若新增資料目錄名稱，必須同步更新：

- Installer preserve list
- tests
- README
- `.gitignore` 建議

---

## 9. 執行里程碑

### 9.0 Gate A 不依賴 memory（強制｜垂直切片）

M0–M3、M5 的實作與驗收 **只**可依賴 `peas-agent-runtime` 與學生 `create_agent`。下列任一情況視為計畫違規，應立刻改回：

| 檢查 | 要求 |
|---|---|
| Runtime package | 無 `memory.py`、無 LTM API、無對 `peas-agent-memory` 的硬依賴 |
| 參考 Agent（`main_shell`） | 預設只接 Session；不得為通過 Gate A 而必裝 memory |
| Shell | 未安裝 memory 時 Agent／Session 面板仍可用 |
| Installer | 契約檢查不因缺少 memory 失敗；memory 安裝策略等 §5 定案 |
| 驗收清單 | Gate A DoD（§12.1）不含「長期記憶可用」；該項只在 gate B |
| M4 | 阻塞於 [`peas-agent-memory-scope-discussion.md`](./peas-agent-memory-scope-discussion.md) 凍結；**不得**擋住 M0–M3 開工或結案 |

垂直切片定義（唯一）：

```text
create_agent → Shell 載入 → 一次 tool call → JSONL 保存 → 重啟後還原
```

### Milestone 0：契約與 Session 資料格式凍結

工作：

- 確認 factory 名稱為 `main:create_agent`
- 確認參數：`session_path`、`host_context`（對齊 Studio，§1.7）
- 確認 `chat()` 最小 signature
- 凍結 Session JSONL schema：**對齊 peas-agent-core**（metadata 首行 + `role` 訊息列）
- 凍結兩層 context 注入（system=`host_context`，user=`【目前頁面狀態】`）
- 確認 runtime **不含**長期記憶、**不**依賴 `peas-agent-core` 套件

產物：

- Runtime README 的 Contract 章節
- Session JSONL schema 文件（註明 core-compatible）
- contract tests
- 與 core 欄位對照的 serialization tests（可用靜態 fixture）

驗收：

- 不啟動 LLM 即可驗證 factory 與 chat signature
- user / assistant（含 tool_calls）/ tool message round-trip tests 完成
- 讀寫形狀與 core 文件範例一致

### Milestone 1：`peas-agent-runtime` Session MVP

工作：

- 建立 package
- 實作 Session message codec
- 實作 `SessionStore`
- 實作錯誤型別
- 實作 contract checker

驗收：

- 全部 unit tests 通過
- 多 tool calls round trip 不遺失 id 或 args
- 中斷／損壞檔案有明確錯誤
- `session_path=None` 可用
- 套件中無長期記憶模組

### Milestone 2：學生參考 Agent 重構

工作：

- **複製** `agentic_ai_vans/main.py` → `main_shell.py`，只在複本上重構（§6.0）
- **禁止修改**原 `main.py`
- 在 `main_shell.py` 建立符合契約的參考版本（保留 calculator、prompt、tools 與 ReAct 概念）
- 複本 CLI／`if __name__` 改為呼叫 `create_agent()`（`host_context=None`）
- 實作 `host_context` 併入 system（`# Host Environment`）
- 複本改為環境變數／`.env` 讀取 credential（不把 key 寫進複本）
- 加入不需要真實 LLM 的單元測試（針對 `main_shell`；含 host_context 併入／CLI 無 host 行為）
- **預設只接 runtime Session**；不強制加入 memory

驗收：

- `git diff`／檔案比對確認原 `main.py` 無變更
- `uv run main_shell.py`（或同等）可建立 Agent
- 傳入 `host_context` 時出現在 system，且不重複貼進 user
- 一輪無 tool call 可正確保存
- 一輪單 tool call 可正確保存
- 一輪多 tool calls 可正確保存
- 重新建立 Agent 後可載入上一輪歷史

### Milestone 3：Dataset Shell factory 整合

工作：

- 新增 `agent_loader.py`：只載入 `main`／`main_shell` 的 `create_agent`
- 傳入 `host_context=dataset_base_context()`；每輪 user 改為 Studio 風格 `【目前頁面狀態】` + `使用者問題：`
- 拆分現有 `dataset_context()`：穩定規則 → host；動態快照 → extra
- **移除**本地 `agent_core.py:from_env`
- 清除 Session 雙重寫入（Shell 不再寫訊息列）
- 讓 UI 從 session JSONL 顯示歷史

驗收：

- `create_agent` 路徑啟用成功（只需 runtime）
- Streamlit rerun 不會遺失當前 Agent/session
- 新增、切換、刪除 session 正常
- 同一訊息不會在 JSONL 出現兩份
- tool call 與 ToolMessage 重啟後仍可還原
- 環境規則不再整包塞進每則 user（對齊 §1.7）
- 未安裝 memory 時 Shell 仍可用

### Milestone 4：`peas-agent-memory` MVP（blocked on 規格討論）

**狀態：阻塞於 §5 討論定案。定案前不開始實作，也不阻塞 M0–M3、M5 的 Session 垂直切片。**

定案後的候選工作（將依討論結果改寫）：

- 建立 `peas-agent-memory` package
- 實作記憶條目序列化（本套件自管）
- 實作儲存／查詢／刪除等 API
- 提供學生 Agent 可插入的簡單使用範例
- 記憶跨 session 共用（若產品仍要此行為）

定案前勿將下列驗收當作現行 DoD：

- session A 寫入的記憶能由 session B 讀取
- 刪除 session 不刪除長期記憶
- tombstone 後 recall 不回傳已刪記憶
- 不呼叫額外 LLM 也能完成 MVP

### Milestone 5：Installer 與文件整合

工作：

- Installer 安裝 Runtime（必裝）
- 新增 `--require-agent-contract`
- 安裝後執行 contract check
- 更新 README 與學生遷移教材
- 更新 `--update` preserve tests（含保留既有 `memory/` 目錄資料）
- memory 套件的安裝策略：等 §5／M4 定案後補上

驗收：

- 新專案可先安裝 Shell，再完成契約
- 嚴格模式會正確拒絕不相容專案
- 相容專案安裝後可直接啟動 Shell（不需 memory）
- `--update` 不破壞 Session、既有 memory 目錄、Dataset workspace

### Milestone 6：端到端課堂驗證

使用乾淨暫存專案模擬學生流程：

1. 複製官方 starter
2. 完成 `Agent.chat()` 與 `create_agent()`
3. 執行 Dataset Installer
4. 啟動 Streamlit
5. 上傳 CSV
6. 讓 Agent 呼叫工具
7. 重新啟動 Shell
8. 驗證短期歷史
9. 切換 session
10. （選驗）驗證長期記憶共用——**僅在 M4 解阻並實作後納入必驗**
11. 執行 Installer `--update`
12. 再次驗證 Session／Dataset 等資料仍存在

Session 垂直切片驗收完成後可走 **release gate A**（發布 Runtime 與 Installer tag）；不必等待 memory。  
**不得**因此宣稱整體「記憶整合計畫」完成——見 §1.6 P2-3 與 §12。

---

## 10. 建議的多 Agent 分工

可平行啟動工作流，但必須遵守檔案所有權，避免互相覆寫。

### Agent A：Runtime

獨占修改：

```text
peas-agent-runtime/**
```

負責 Milestone 0、1。

交付：

- package
- Session schema
- tests
- 使用範例

**不負責**長期記憶。

### Agent B：Dataset Shell 與 Installer

獨占修改：

```text
dataset-streamlit-shell-installer/**
```

負責 Milestone 3、5。

開始 Milestone 3 前必須取得 Agent A 凍結的 contract 與 session schema；不得自行發明另一套格式。

### Agent C：參考學生專案與教材

獨占修改：

```text
agentic_ai_vans/**
```

負責 Milestone 2 與學生遷移教材草稿。

不得修改原 `main.py`；只重構 `main_shell.py`（§6.0）。不得把 Runtime 的 ReAct 實作黑箱化進複本。記憶示範等 §5／M4 定案後再加。

### Agent D：Memory（規格定案後）

獨占修改：

```text
peas-agent-memory/**
```

負責 Milestone 4（解阻後）。不得把記憶序列化或 API 實作進 `peas-agent-runtime`。

### 整合 Agent

在 A、B、C（以及已解阻的 D）完成後負責 Milestone 6。整合 Agent 不應重寫各工作流的核心設計；發現契約不一致時，先提交具體 incompatibility report，再由對應 owner 修正。

---

## 11. 測試矩陣

| 類別 | 測試案例 | 預期結果 |
|---|---|---|
| Contract | 缺少 `create_agent` | 明確提示，不誤報 import error |
| Contract | factory 不接受 `session_path` 或 `host_context` | 顯示 signature 修正方式 |
| Shell | host 進 system、快照進 user | 與 Studio 兩層一致；舊整包 user 拼法不存在 |
| Contract | 回傳物件沒有 `chat` | 明確拒絕 |
| Contract | 未安裝 memory | 契約檢查仍可通過 |
| Contract | 預設檢查無 API key | 不呼叫 `create_agent()`，不打 LLM |
| Contract | `invoke=True` 深檢 | 文件註明需金鑰；測試用 fake |
| Path | `../escape.jsonl` | 拒絕 |
| Path | 不含 `sessions` | 拒絕（Shell 傳入時） |
| Image | `image_path` 有值（Gate A） | `main_shell` raise 明確錯誤，不靜默當純文字 |
| Session | 空 session | 回傳空 history |
| Session | Human/AI round trip | 內容與型別等價 |
| Session | AI tool calls | name、args、id 完整 |
| Session | ToolMessage | `tool_call_id` 完整 |
| Session | 損壞 JSONL | 明確錯誤，不靜默清空 |
| ReAct | 未知工具 | 產生 error ToolMessage |
| ReAct | 工具拋例外 | 產生 error ToolMessage，迴圈可繼續 |
| ReAct | 多工具同輪 | 全部結果加入後才再次 invoke |
| ReAct | 超過輪數 | 停止並回報，不無限執行 |
| Shell | Streamlit rerun | Agent 與 session 狀態可恢復 |
| Shell | 切換 session | 短期歷史隔離 |
| Shell | 無 memory 套件 | Agent／Session 面板仍可用 |
| Memory | （M4 定案後再填） | （TBD） |
| Installer | 首次安裝 | Shell 與 runtime dependency 正常加入 |
| Installer | `--update` | 保留 workspace/session/memory/uploads |
| Shell | 僅有舊 `agent_core.py` | 不載入 from_env；提示改實作 `create_agent` |
| Shell | 無 `create_agent` | 未連接；不 fallback 到 peas-agent-core |

所有 LLM 相關測試預設使用 fake chat model 與 fake tools，不可依賴真實 API key 或網路。

---

## 12. Definition of Done

### 12.1 Session 垂直切片＝release gate A（可先發布 runtime／installer）

- 學生不強制、Shell 不依賴 `peas-agent-core`（用 runtime 即可）
- Shell **不**支援 `peas-agent-core` `Agent.create`（§1.8）
- 學生能說明 Human → AI tool call → ToolMessage → final AI 的順序
- 學生保留自己的 LLM、prompt、tools 與 `chat()` ReAct 邏輯
- 學生只需以 `create_agent(session_path=None, host_context=None)` 接上 Shell（Shell 會傳 host_context）
- Context 注入對齊 Studio：host→system、頁面快照→user（§1.7）
- Dataset Installer 是唯一必要安裝入口（runtime 必裝；**不**裝 core）
- Shell 能建立、切換、刪除 session
- Session 重啟後能完整還原 tool calls
- Shell 與 Agent 不會雙重寫入 Session；已移除本地 `from_env`；`SessionStore` 為唯一寫入者（§1.6 P1-2、§1.8）
- 預設契約檢查不需要 API key（§1.6 P1-1）
- Session 路徑規則已實作且與 Shell 一致（§1.6 P1-3）
- `image_path` 不靜默忽略（§1.6 P2-1）
- `--update` 不會破壞 Dataset、Session（以及既有 memory 目錄資料）
- Runtime／Shell／參考 Agent 相關單元與整合測試通過
- 文件包含學生版最短流程與教師版除錯流程，並區分 gate A／gate B 用語（§1.6 P2-3）
- **長期記憶不是 gate A 的必達條件**

### 12.2 Memory 切片＝release gate B（§5／M4 定案後另計）

定案後再寫入具體 DoD（跨 session、tombstone、整併等）。  
**Gate A 發布 ≠ 整體計畫完成**；未完成 gate B 前不得宣稱記憶整合全部完成。

---

## 13. 實作順序摘要

```text
凍結契約與 Session JSONL schema（對齊 peas-agent-core）
    ↓
完成 Runtime SessionStore（core-compatible codec，不依賴 core）
    ↓
複製 main.py → main_shell.py 並重構複本（原檔不動）
    ↓
讓 Dataset Shell 載入 create_agent（vans 用 main_shell）
    ↓
消除 Session 雙重寫入
    ↓
整合 Installer 與 update 保護
    ↓
端到端驗證 Session 垂直切片
    ↓
（平行／之後）討論並定案 peas-agent-memory → M4 → 選驗記憶
```

第一個可展示的 vertical slice 應只包含：

```text
create_agent → Shell 載入 → 一次 tool call → JSONL 保存 → 重啟後還原
```

此切片只需要 `peas-agent-runtime`，不需要 `peas-agent-memory`。  
在這條流程穩定以前，不開始 embeddings、自動記憶判斷、進階記憶 UI 或任意程式碼改寫。
