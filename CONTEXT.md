# Agentic AI Vans

凡思課堂學生 Agent 參考專案：學生完成 CLI `main.py`；接 Dataset Shell 時使用 Shell Agent 檔。

## Language

**Shell Agent 模板**:
本專案根目錄、尚未填入個別學生角色設定的 `main_shell.py`；是課堂一鍵寫入學生專案的來源。
_Avoid_: 學生專案裡的同名檔；把此檔複製進 Dataset Shell installer 當第二份原始碼

**Shell Agent 檔**:
學生專案根目錄的 `main_shell.py`；由模板寫入並填入該生角色設定後，供 Shell 以 `main_shell:create_agent` 載入。
_Avoid_: 與模板口頭混稱；為改某一屆學生檔而去改教材專案

**角色設定**:
學生 `main.py` 裡 `build_system_prompt` 的 `soul` 與 `user` 兩個字串。
_Avoid_: calculator、tool loop、API 金鑰
