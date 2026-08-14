# 接上 Shell Agent

課堂一鍵用的小工具：從 GitHub `master` 下載 vans 根目錄的 Shell Agent 模板，填入學生 `main.py` 的 `soul`／`user`，寫成專案根目錄的 `main_shell.py`。

不改 `main.py`。已有 `main_shell.py` 則不覆寫。無執行期依賴。

```powershell
uvx --from git+https://github.com/mz038197/agentic_ai_vans.git@master#subdirectory=shell-agent-tool add-shell-agent
```

本機：

```powershell
uvx --from . add-shell-agent -C <學生專案根目錄>
```
