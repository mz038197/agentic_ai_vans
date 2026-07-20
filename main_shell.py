"""Shell 用參考 Agent（由 main.py 概念重構；原 main.py 禁止修改）。

相對 main.py 的增量：create_agent、SessionStore、host_context。
Gate A 先不支援附圖。
訊息格式對齊 main.py：用 role 字典，不在學生程式裡組 AIMessage／HumanMessage 等類別。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from peas_agent_runtime import SessionStore
from peas_agent_tools import get_builtin_tools

load_dotenv(Path(__file__).resolve().parent / ".env")

MAX_TOOL_ROUNDS = 8
DEFAULT_SESSION_PATH = "sessions/session.jsonl"


@tool
def calculator(a: float, b: float, operation: str) -> float:
    """Perform a calculation on two numbers."""
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b != 0:
            return a / b
        return "Error: Division by zero"
    return "Error: Unsupported operation"


def build_system_prompt(host_context: str | None = None) -> dict:
    soul = "你是法鬥超人，一位擅長引導學生python問題的助教"
    user = (
        "我的名字叫Vans, 是一位樂於分享AI資訊的講師。"
        "我喜歡你用簡潔扼要的方式引導我解決python問題，並且在回答中加入一些幽默感。"
    )
    system_content = f"""
    # 角色設定
    {soul}
    # 使用者設定
    {user}
    """
    if host_context and str(host_context).strip():
        system_content = (
            f"{system_content.rstrip()}\n\n"
            f"# Host Environment\n{str(host_context).strip()}"
        )
    return {"role": "system", "content": system_content}


class Agent:
    def __init__(
        self,
        *,
        llm,
        tools,
        session_path=None,
        host_context=None,
        base_dir: str | Path | None = None,
    ):
        self.llm = llm.bind_tools(tools)
        self.tool_map = {t.name: t for t in tools}
        self.host_context = host_context
        root = Path(base_dir) if base_dir is not None else Path.cwd()
        path = DEFAULT_SESSION_PATH if session_path is None else session_path
        self.session = SessionStore(path, base_dir=root)
        self.history = self.session.load()

    def chat(self, user_text: str, *, image_path: str | None = None, on_token=None) -> str:
        if image_path is not None:
            raise NotImplementedError("尚未支援 image_path（Gate A 先做文字對話）")

        system_prompt = build_system_prompt(self.host_context)
        self.history.append({"role": "user", "content": user_text})

        for _ in range(MAX_TOOL_ROUNDS):
            response = self.llm.invoke([system_prompt, *self.history])
            tool_calls = getattr(response, "tool_calls", None) or []

            if not tool_calls:
                answer = str(response.content or "")
                self.history.append({"role": "assistant", "content": answer})
                self.session.save(self.history)
                if on_token is not None:
                    on_token(answer)
                return answer

            self.history.append(
                {
                    "role": "assistant",
                    "content": str(response.content or ""),
                    "tool_calls": tool_calls,
                }
            )
            for tool_call in tool_calls:
                name = tool_call.get("name", "")
                tool_id = str(tool_call.get("id", ""))
                if name not in self.tool_map:
                    content = f"Error: Tool '{name}' not found."
                else:
                    try:
                        content = str(self.tool_map[name].invoke(tool_call.get("args") or {}))
                    except Exception as exc:
                        content = f"Error: tool '{name}' raised {type(exc).__name__}: {exc}"
                tool_response = {
                    "role": "tool",
                    "content": content,
                    "tool_call_id": tool_id,
                }
                if name:
                    tool_response["name"] = name
                self.history.append(tool_response)

        self.session.save(self.history)
        raise RuntimeError("Agent 工具呼叫次數超過上限。")


def build_llm() -> ChatOpenAI:
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("請設定環境變數 OPENAI_API_KEY（或 VCR_API_KEY）。")
    return ChatOpenAI(
        api_key=api_key,
        model_name=os.environ.get("MODEL_NAME"),
        temperature=0.7,
        base_url=os.environ.get("BASE_URL"),
    )


def create_agent(session_path=None, host_context=None):
    return Agent(
        llm=build_llm(),
        tools=[*get_builtin_tools(), calculator],
        session_path=session_path,
        host_context=host_context,
    )


def main() -> None:
    agent = create_agent()
    while True:
        question = input("你的問題: ").strip()
        if not question:
            print("請輸入一個問題。")
            continue
        if question.lower() == "quit":
            print("Exiting...")
            break
        print("AI:", agent.chat(question))


if __name__ == "__main__":
    main()
