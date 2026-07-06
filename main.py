from langchain_openai import ChatOpenAI
api_key = "vcr_sk_fc0905e9e690890a8592b7913203a10830d626a7da10f9436778883c7c05c8e3"


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
    llm = ChatOpenAI(
        api_key=api_key, 
        model_name="ollama_cloud@minimax-m3:cloud", 
        temperature=0.7,
        base_url="https://ai.vanscoding.com/v1")
    
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

        response = llm.invoke([system_prompt, user_prompt])
        print(response.content)



if __name__ == "__main__":
    main()
