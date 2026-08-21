def new_messages():
    # 完成挑戰：建立 messages 串列（Lv5 Memory）
    return []


def make_system_message(content: str):
    # 完成挑戰：建立系統提示詞（Lv5 Memory）
    return {}


def remember_user(messages, text):
    # 完成挑戰：記錄 user & assistant 訊息（Lv5 Memory）
    pass


def remember_assistant(messages, text):
    # 完成挑戰：記錄 user & assistant 訊息（Lv5 Memory）
    pass


def send_context(system, history, question):
    # 完成挑戰：發送 Context 訊息（Lv5 Memory）
    return [{"role": "user", "content": question}]
