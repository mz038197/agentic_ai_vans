
from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from peas_agent_runtime import SessionStore
from peas_agent_tools import get_builtin_tools

load_dotenv()

DEFAULT_SESSION_PATH = "sessions/session.jsonl"


@tool
def calculator(a: float, b: float, operation: str) -> float:
    """對兩個數字做加減乘除運算。需要計算時請呼叫此工具。"""
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
    # Host Environment
    {host_context or ""}
    """
    return {"role": "system", "content": system_content}


class Agent:
    def __init__(self, llm, tools, session_path=None, host_context=None):
        self.llm = llm.bind_tools(tools)
        self.tool_map = {t.name: t for t in tools}
        self.host_context = host_context
        self.session = SessionStore(session_path)
        self.history = self.session.load()

    def chat(self, user_text: str, image_path=None, on_token=None) -> str:
        # image_path：本教學版忽略；簽名保留以相容呼叫端
        system_prompt = build_system_prompt(self.host_context)
        user_prompt = {"role": "user", "content": user_text}
        self.history.append(user_prompt)

        response = self.llm.invoke([system_prompt, *self.history])

        while response.tool_calls:
            
            self.history.append(
                {
                    "role": "assistant",
                    "content": str(response.content or ""),
                    "tool_calls": response.tool_calls,
                }
            )

            for tool_call in response.tool_calls:
                print(tool_call)
                name = tool_call["name"]
                if name not in self.tool_map:
                    content = f"Error: Tool '{name}' not found."
                else:
                    content = str(self.tool_map[name].invoke(tool_call["args"]))
                self.history.append(
                    {
                        "role": "tool",
                        "content": content,
                        "tool_call_id": tool_call["id"],
                    }
                )

            response = self.llm.invoke([system_prompt, *self.history])

        answer = str(response.content or "")
        
        self.history.append({"role": "assistant", "content": answer})
        self.session.save(self.history)
        if on_token is not None:
            on_token(answer)
        return answer


def create_agent(session_path=None, host_context=None):
    llm = ChatOpenAI(
        api_key=os.environ.get("API_KEY"),
        model_name=os.environ.get("MODEL_NAME"),
        temperature=0.7,
        base_url=os.environ.get("BASE_URL"),
    )
    return Agent(
        llm,
        [*get_builtin_tools(), calculator],
        session_path or DEFAULT_SESSION_PATH,
        host_context,
    )


def main() -> None:
    agent = create_agent()
    while True:
        question = input("\n你的問題: ").strip()
        if not question:
            print("請輸入一個問題。")
            continue
        if question.lower() == "quit":
            print("Exiting...")
            break
        print("\nAI:", agent.chat(question))


if __name__ == "__main__":
    main()
