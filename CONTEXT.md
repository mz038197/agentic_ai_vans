# Agentic AI Vans

凡思課堂學生 Agent 參考專案。根目錄 `main.py` 是通關成品。課堂填空以安裝器寫入學生的課程專案，不在本 repo 裡跑。接 Dataset Shell 時使用 Shell Agent 檔。

## Language

**Shell Agent 模板**:
本專案根目錄、尚未填入個別學生角色設定的 `main_shell.py`；是課堂一鍵寫入學生專案的來源。
_Avoid_: 學生專案裡的同名檔；把此檔複製進 Dataset Shell installer 當第二份原始碼

**Shell Agent 檔**:
學生專案根目錄的 `main_shell.py`；由模板寫入並填入該生角色設定後，供 Shell 以 `main_shell:create_agent` 載入。
_Avoid_: 與模板口頭混稱；為改某一屆學生檔而去改教材專案

**角色設定**:
學生 `main.py` 裡 `build_system_prompt` 的 `soul` 與 `user` 兩個字串常數。Lv4 Identity 的洞也在這裡，不抽成關卡檔。
_Avoid_: calculator、tool loop、API 金鑰；從別的檔 import 再賦值給 soul／user（安裝器抽不到）

**通關成品**:
本專案根目錄的 `main.py`：八關都做完後的完整 CLI Agent，單檔、行為對齊 Agent Dungeon 教材，不當填空用。不拆成關卡檔。
_Avoid_: example.py、起點主程式、答案卷；把通關成品也拆成跟課堂起點一樣的多檔結構

**課程專案**:
學生自己的課堂作業目錄；填空與 `uv run main.py` 都在這裡進行，不是 vans 教材 repo。
_Avoid_: 本專案根目錄、把 vans clone 下來當作業目錄（除非另有約定）

**起點模板**:
本專案 `dungeon-starter/` 裡尚未填過的課堂起點來源，供安裝器寫入課程專案。對齊 Shell Agent 模板：來源在 vans，實例在學生那邊。
_Avoid_: 在 vans 根目錄直接改通關成品來當填空；叫學生 cd 進 vans 子目錄跑；把模板打進安裝器套件、repo 裡看不到空洞檔

**起點主程式**:
安裝後位於課程專案根目錄的 `main.py`：帶 Lv1～Lv4 的洞，組裝關卡檔。學生執行的是這份，不是通關成品。
_Avoid_: 膠水檔、vans 根目錄的 `main.py`

**課堂起點**:
安裝器寫進課程專案的那組檔：起點主程式加上各關卡檔。課程專案裡已有同名檔則跳過、不覆寫。
_Avoid_: 填空卷、考卷、零件包、在 vans 裡開一個給學生 cd 進去的 starter 專案；默默覆寫學生既有的 `main.py`

**關卡**:
Agent Dungeon 的八個能力層：Lv1 Voice、Lv2 Brain、Lv3 Loop、Lv4 Identity、Lv5 Memory、Lv6 Tools、Lv7 Decision、Lv8 Coding。
_Avoid_: 把一關裡的單一步驟也叫關卡

**完成挑戰**:
一關裡面的實作步驟，對應教材「完成挑戰」原句。
_Avoid_: 關卡（那是能力層）、把完成挑戰再拆成獨立安裝檔

**關卡檔**:
課程專案裡對應單一關卡、給學生填的獨立 `.py`。Lv1～Lv4 沒有關卡檔，洞在起點主程式。四個檔名：`level5_memory.py`、`level6_tools.py`、`level7_react.py`、`level8_coding.py`。洞旁註解用教材完成挑戰原句，不寫答案。
_Avoid_: 零件、模組、TODO 檔；`memory.py` 這類不帶關卡編號的泛名；放到 `levels/` 子目錄
