# Agentic AI Vans

凡思課堂學生 Agent 參考專案。根目錄 `main.py` 是通關成品，給學生當參考。學生在自己的課程專案從零寫。接 Dataset Shell 時使用 Shell Agent 檔。

## Language

**Shell Agent 模板**:
本專案根目錄、尚未填入個別學生角色設定的 `main_shell.py`；是課堂一鍵寫入學生專案的來源。
_Avoid_: 學生專案裡的同名檔；把此檔複製進 Dataset Shell installer 當第二份原始碼

**Shell Agent 檔**:
學生專案根目錄的 `main_shell.py`；由模板寫入並填入該生角色設定後，供 Shell 以 `main_shell:create_agent` 載入。
_Avoid_: 與模板口頭混稱；為改某一屆學生檔而去改教材專案

**角色設定**:
學生 `main.py` 裡 `build_system_prompt` 的 `soul` 與 `user` 兩個字串常數。只有這兩個必須留在該檔，課程專案其餘檔可自拆。
_Avoid_: calculator、tool loop、API 金鑰；從別的檔 import 再賦值給 soul／user（Shell 安裝器抽不到）

**通關成品**:
本專案根目錄的 `main.py`：八關都做完後的完整 CLI Agent，單檔、行為對齊 Agent Dungeon 教材。只給學生當參考，不複製進課程專案當起點。
_Avoid_: example.py、答案卷、起點模板、起點主程式、課堂起點

**課程專案**:
學生自己的課堂作業目錄；從零實作關卡與完成挑戰，並以 `uv run main.py` 執行，不是 vans 教材 repo。
_Avoid_: 本專案根目錄、把 vans clone 下來當作業目錄（除非另有約定）；把通關成品複製進來當第一份檔

**關卡**:
Agent Dungeon 的八個能力層：Lv1 Voice、Lv2 Brain、Lv3 Loop、Lv4 Identity、Lv5 Memory、Lv6 Tools、Lv7 Decision、Lv8 Coding。
_Avoid_: 把一關裡的單一步驟也叫關卡；關卡檔

**完成挑戰**:
一關裡面的實作步驟，對應教材「完成挑戰」原句。
_Avoid_: 關卡（那是能力層）
