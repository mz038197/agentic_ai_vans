
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


api_key = "vcr_sk_96725ddabe06bfb610b7e2c625459d69e603f81b5da35ba6c723735c0ed85b78"

@tool
def calculator(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b != 0:
            return a / b
        else:
            return "Error: Division by zero"
    else:
        return "Error: Invalid operation"


def build_system_prompt():
    soul = "你是法鬥超人，一位擅長引導學生python問題的助教"
    user = "我的名字叫Vans, 是一位樂於分享AI資訊的講師。我喜歡你用簡潔扼要的方式引導我解決python問題，並且在回答中加入一些幽默感。"
    system_content = f"""
    # 角色設定
    {soul}
    # 使用者設定
    {user}
    """
    return {"role": "system", "content": system_content}


def main():
    message_history = []
    llm = ChatOpenAI(
        api_key=api_key, 
        model_name="ollama_cloud@minimax-m3:cloud", 
        temperature=0.7,
        base_url="https://ai.vanscoding.com/v1")
    
    while True:
        question = input("你的問題: ")

        if question.strip() == "":
            print("請輸入一個問題。")
            continue

        if question.strip().lower() == "quit":
            print("Exiting...")
            break
        
        system_prompt = build_system_prompt()
        user_prompt = {"role": "user", "content": question}
        message_history.append(user_prompt)

        response = llm.invoke(
            [system_prompt, *message_history]
        )
        assistant_content = response.content
        message_history.append(
            {"role": "assistant", "content": assistant_content}
        )
        print(assistant_content)



if __name__ == "__main__":
    main()
