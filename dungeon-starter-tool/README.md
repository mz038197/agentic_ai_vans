# 寫入課堂起點

課堂一鍵用的小工具：把 vans 的 `dungeon-starter/` 起點模板寫進學生課程專案根目錄（起點主程式 `main.py` 與 Lv5～Lv8 關卡檔）。

已有同名檔則跳過、不覆寫。無執行期依賴。

```powershell
uvx --from git+https://github.com/mz038197/agentic_ai_vans.git@master#subdirectory=dungeon-starter-tool add-dungeon-starter
```

本機（在 vans 的 `dungeon-starter-tool/` 目錄）：

```powershell
uvx --from . add-dungeon-starter -C <學生課程專案根目錄>
```

本機執行時若找得到上一層的 `dungeon-starter/`，會直接讀那些檔，不必先 push 到 GitHub。
