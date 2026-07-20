# `peas-agent-memory` 規格討論（另開｜尚未凍結實作）

> **狀態（2026-07-19）**：討論區已開。下列「已定邊界」可直接約束 runtime／Gate A；「待凍結」與「草案」**不是**現行契約。  
> **規則**：未凍結前 **不開始 Milestone 4**；**不阻塞** M0–M3／M5 Session 垂直切片（見升級計畫 gate A）。  
> **主計畫**：[`dataset-shell-student-agent-upgrade-plan.md`](./dataset-shell-student-agent-upgrade-plan.md) §5、§12.2。

---

## 1. 已定邊界（可立刻遵守，無需再討論）

| 決策 | 說明 |
|---|---|
| 獨立套件 | 暫名 `peas-agent-memory`；package 暫名 `peas_agent_memory` |
| 建議路徑 | `C:\Users\mz038\Desktop\peas-agent\peas-agent-memory` |
| 與 runtime 邊界 | 記憶條目序列化／schema **只在 memory**；`peas-agent-runtime` **不得**含 LTM／`memory.py` |
| 與 Session 分開 | 長期記憶資料與 Session JSONL **必須**分目錄／分檔 |
| Gate A | Session ↔ Shell 垂直切片 **不依賴**本套件 |
| 契約檢查 | `create_agent`／runtime 契約 **不**因缺少 memory 而失敗 |
| Shell UI | 未接 memory 時 Agent／Session 面板仍可用；不得誤觸「清全部記憶」 |
| 第一版禁區 | 不定案前不做 embeddings／向量庫／複雜評分；不每輪自動多打一輪 LLM |

---

## 2. 待凍結題目（定案後回填升級計畫 §5 與 M4）

逐項勾選後，才解阻 M4。

### 2.1 要記什麼

- [ ] facts（事實）
- [ ] preference（偏好）
- [ ] summary（摘要）
- [ ] 其他：________

**草案**：先支援 `preference` + 自由文字 `fact`；summary 留給 consolidator 之後。

### 2.2 公開 API

- [ ] 是否採 `remember` / `recall` / `list` / `delete`？
- [ ] 類別名是否固定為 `LongTermMemory`？
- [ ] `recall` 第一版要不要關鍵字搜尋，還是只 list＋簡單過濾？

**草案（非正式契約）**：

```python
memory = LongTermMemory(memory_dir)
memory.remember(text, category="preference")  # → id
items = memory.recall(query, limit=5)         # 簡單包含比對即可
memory.list()
memory.delete(memory_id)                      # tombstone，非物理刪
```

### 2.3 觸發方式

- [ ] 僅學生程式明確呼叫 API
- [ ] 另提供 remember tool 給 ReAct
- [ ] 之後才考慮自動寫入

**草案**：第一版只做明確 API；tool／自動寫入另里程碑。

### 2.4 儲存路徑與格式

- [ ] 是否沿用 `dataset_streamlit_shell/memory/`？
- [ ] on-disk 格式（JSONL？單檔？）
- [ ] schema 欄位（id、text、category、created_at、tombstone…）

**草案**：目錄沿用 `dataset_streamlit_shell/memory/`；單檔或每日 JSONL 二選一，定案時寫死；**不**與 Session codec 共用。

### 2.5 整併（consolidator）

- [ ] Gate B 要不要做？
- [ ] 「滿了才整併」門檻？
- [ ] 是否允許打 LLM 做摘要？

**草案**：自動整併偏後；Gate B MVP 可不含 consolidator。

### 2.6 教材與 Installer

- [ ] 學生教材最小接點幾個（例：只示範 `remember`＋`recall`）？
- [ ] Installer：預設必裝／選裝／完全手動？

**草案**：Installer **選裝或不預設安裝**；教材等 API 凍結後再加一頁。

---

## 3. 與 Gate A 的關係（強制）

```text
M0–M3、M5、gate A  ← 只依賴 peas-agent-runtime
M4、gate B         ← 依賴本文件「待凍結」全部勾選後才開工
```

驗收時若有人把「長期記憶可用」寫進 gate A DoD → **退回**，改寫進 §12.2。

---

## 4. 定案紀錄（凍結時填）

| 日期 | 決策摘要 | 回填位置 |
|---|---|---|
| （尚未） | — | 升級計畫 §5、M4、§12.2 |
