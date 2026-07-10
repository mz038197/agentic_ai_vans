
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from peas_agent_tools import get_builtin_tools

api_key = "vcr_sk_6b741c30e40f1b1bd51c9ee3e434bbb3f8979bc0b07930a31200099b2413859f"

@tool
def calculator(a: float, b: float, operation: str) -> float:
    """Perform a calculation on two numbers."""
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
        return "Error: Unsupported operation"

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
    tools = [*get_builtin_tools(), calculator]
    tool_map = {tool.name: tool for tool in tools}

    llm = ChatOpenAI(
        api_key=api_key, 
        model_name="ollama_cloud@minimax-m3:cloud", 
        temperature=0.7,
        base_url="https://ai.vanscoding.com/v1")
    
    llm = llm.bind_tools(tools)

    message_history = []
    while True:
        question = input("你的問題: ")

        if not question.strip():
            print("請輸入一個問題。")
            continue

        if question.strip().lower() == "quit":
            print("Exiting...")
            break
        
        system_prompt = build_system_prompt()

        user_prompt = {"role": "user", "content": question}
        message_history.append(user_prompt)

        response = llm.invoke([system_prompt, *message_history])
        
        while response.tool_calls:
            # 先記下助理的 tool_calls 訊息，模型才知道是自己呼叫的
            message_history.append(response)
            print(response.tool_calls)

            # 一次把模型要求的所有工具都執行完
            for tool_call in response.tool_calls:
                print(f"Tool call: {tool_call}")
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                if tool_name not in tool_map:
                    print(f"Error: Tool '{tool_name}' not found.")
                    continue

                tool_func = tool_map[tool_name]
                result = tool_func.invoke(tool_args)
                tool_response = {"role": "tool", "content": str(result), "tool_call_id": tool_id}
                print(f"Tool '{tool_name}' called with arguments {tool_args}. Result: {result}")
                message_history.append(tool_response)

            # 所有工具結果都放進歷史後，再讓模型產生下一步回應
            response = llm.invoke([system_prompt, *message_history])

        assistant_message = {"role": "assistant", "content": response.content}
        message_history.append(assistant_message)
        print("AI: ", end="")
        print(response.content)



if __name__ == "__main__":
    main()
