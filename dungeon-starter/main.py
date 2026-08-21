from langchain_openai import ChatOpenAI

from level5_memory import (
    make_system_message,
    new_messages,
    remember_assistant,
    remember_user,
    send_context,
)
from level6_tools import student_tools
from level7_react import prepare_llm, run_react
from level8_coding import extra_tools

API_KEY = "vcr_sk_6b741c30e40f1b1bd51c9ee3e434bbb3f8979bc0b07930a31200099b2413859f"
MODEL_NAME = "ollama_cloud@minimax-m3:cloud"
BASE_URL = "https://ai.vanscoding.com/v1"


def build_system_prompt():
    # 完成挑戰：建立系統提示詞字串（Lv4 Identity）
    soul = ""
    user = ""
    return f"""
    # 角色設定
    {soul}
    # 使用者設定
    {user}
    """


def main():
    # 完成挑戰：用 print 輸出 "Hello"（Lv1 Voice）
    print("")
    # 完成挑戰：讓 Agent 說話（Lv1 Voice）
    print("")

    # 完成挑戰：建立大腦（Lv2 Brain）
    llm = ChatOpenAI(
        api_key=API_KEY,
        model_name=MODEL_NAME,
        temperature=0.7,
        base_url=BASE_URL,
    )

    tools, tool_map = student_tools()
    tools = [*extra_tools(), *tools]
    if tools:
        tool_map = {tool.name: tool for tool in tools}
    llm = prepare_llm(llm, tools)

    history = new_messages()

    # 完成挑戰：建立對話迴圈（Lv3 Loop）
    while True:
        # 完成挑戰：讀取使用者輸入（Lv2 Brain）
        question = input("\n你的問題: ")

        # 完成挑戰：說 bye bye 離開 & 空字串就繼續（Lv3 Loop）
        if question.strip() == "":
            print("請輸入一個問題。")
            continue
        if question.strip().lower() == "bye bye":
            pass

        system = make_system_message(build_system_prompt())
        remember_user(history, question)
        # 完成挑戰：完成 Agent 大腦安裝（Lv2 Brain）
        response = llm.invoke(send_context(system, history, question))
        response = run_react(response, llm, system, history, tool_map)
        remember_assistant(history, response.content)
        print("\nAI: ", end="")
        print(response.content)


if __name__ == "__main__":
    main()
