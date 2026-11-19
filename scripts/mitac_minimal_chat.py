"""最小神通 Agent Builder 串接範例：登入 → 建 Session → run_sse 對話。

對照 API 文件 v1.2.2：Ch.3 login、Ch.10/11 列 Space/App、Ch.15 建 Session、Ch.14 run_sse。

設定（環境變數或 .env；缺的會在執行時詢問）：
    MITAC_BASE_URL   例：http://學校server:5011（不要結尾斜線）
    MITAC_EMAIL      Agent Builder 平台的登入 Email
    MITAC_PASSWORD   不設就用隱藏輸入詢問
    MITAC_SPACE_ID   選填；不設就列出可用 Space 讓你選
    MITAC_APP_ID     選填；不設就列出可用 App 讓你選

執行：
    uv run python scripts/mitac_minimal_chat.py
    uv run python scripts/mitac_minimal_chat.py "請用一句話介紹你自己"   # 只問一句就結束

token 只放在記憶體，不寫檔。
"""

from __future__ import annotations

import getpass
import json
import os
import sys
import uuid

import requests
from dotenv import load_dotenv


def ask(env_name: str, prompt: str, secret: bool = False) -> str:
    value = os.getenv(env_name, "").strip()
    if value:
        return value
    return (getpass.getpass(prompt) if secret else input(prompt)).strip()


def pick(items: list[dict], label: str) -> int:
    if not items:
        sys.exit(f"這個帳號看不到任何 {label}，請確認群組授權。")
    for item in items:
        print(f"  [{item['id']}] {item['name']}")
    if len(items) == 1:
        print(f"只有一個 {label}，自動選它。")
        return items[0]["id"]
    return int(input(f"輸入 {label} ID："))


def login(base: str, email: str, password: str) -> tuple[str, str]:
    """Ch.3：POST /api/v1/auth/login，回傳 (access_token, user_id)。"""
    resp = requests.post(
        f"{base}/api/v1/auth/login",
        json={"email": email, "password": password},
        timeout=30,
    )
    if resp.status_code == 401:
        sys.exit("登入失敗：帳號或密碼錯誤。")
    if resp.status_code == 403:
        sys.exit("登入失敗：帳號尚未啟用或已停權。")
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"], data["user_id"]


def create_session(base: str, headers: dict, space_id: int, app_id: int, user_id: str) -> str:
    """Ch.15：建立 Session，run_sse 之前必須先有。"""
    resp = requests.post(
        f"{base}/api/v1/spaces/{space_id}/apps/{app_id}/users/{user_id}/sessions",
        headers=headers,
        json={"session_id": f"py-{uuid.uuid4().hex[:12]}", "session_name": "Python 最小範例"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def chat(base: str, headers: dict, space_id: int, app_id: int, user_id: str, session_id: str, text: str) -> None:
    """Ch.14：run_sse，streaming=true 時只印 partial 增量；沒有增量才印完整事件。"""
    payload = {
        "user_id": user_id,  # 伺服器會以登入者覆寫
        "session_id": session_id,
        "new_message": {"role": "user", "parts": [{"text": text}]},
        "streaming": True,
    }
    printed_partial = False
    display_mode = "display"
    with requests.post(
        f"{base}/api/v1/spaces/{space_id}/apps/{app_id}/run_sse",
        headers=headers,
        json=payload,
        stream=True,
        timeout=(30, 300),
    ) as resp:
        resp.raise_for_status()
        resp.encoding = "utf-8"
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                display_mode = "display"  # 空行 = 一個事件結束
                continue
            if line.startswith("event: "):
                display_mode = line[len("event: "):].strip()  # display / thinking / hide
                continue
            if not line.startswith("data: "):
                continue
            event = json.loads(line[len("data: "):])
            if "error" in event:
                print(f"\n[錯誤] {event['error']} ({event.get('error_type')})")
                return
            if display_mode != "display":
                continue
            is_partial = bool(event.get("partial"))
            if not is_partial and printed_partial:
                continue  # 完整事件會重複整段文字，已印過增量就跳過
            for part in (event.get("content") or {}).get("parts") or []:
                if part.get("thought"):
                    continue
                if "text" in part:
                    print(part["text"], end="", flush=True)
                    printed_partial = printed_partial or is_partial
    print()


def main() -> None:
    load_dotenv()
    base = ask("MITAC_BASE_URL", "Base URL（例 http://host:5011）：").rstrip("/")
    email = ask("MITAC_EMAIL", "Email：")
    password = ask("MITAC_PASSWORD", "密碼：", secret=True)

    token, user_id = login(base, email, password)
    headers = {"Authorization": f"Bearer {token}"}
    print(f"登入成功，user_id = {user_id}")

    space_id = os.getenv("MITAC_SPACE_ID")
    if not space_id:
        spaces = requests.get(f"{base}/api/v1/spaces", headers=headers, timeout=30)
        spaces.raise_for_status()
        space_id = pick(spaces.json().get("spaces", []), "Space")
    space_id = int(space_id)

    app_id = os.getenv("MITAC_APP_ID")
    if not app_id:
        apps = requests.get(f"{base}/api/v1/spaces/{space_id}/apps", headers=headers, timeout=30)
        apps.raise_for_status()
        app_id = pick(apps.json().get("apps", []), "App")
    app_id = int(app_id)

    session_id = create_session(base, headers, space_id, app_id, user_id)
    print(f"Session 建好了：{session_id}\n")

    if len(sys.argv) > 1:
        print("你：", " ".join(sys.argv[1:]))
        print("Agent：", end="")
        chat(base, headers, space_id, app_id, user_id, session_id, " ".join(sys.argv[1:]))
        return

    print("開始對話（空白行或 Ctrl+C 結束）")
    try:
        while True:
            text = input("你：").strip()
            if not text:
                break
            print("Agent：", end="")
            chat(base, headers, space_id, app_id, user_id, session_id, text)
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    main()
