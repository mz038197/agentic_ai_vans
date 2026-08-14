from add_shell_agent.core import extract_role_settings


def test_extract_soul_and_user_from_build_system_prompt() -> None:
    source = """
def build_system_prompt():
    soul = "你是助教"
    user = "我叫小明"
    return {"role": "system", "content": soul + user}
"""
    soul, user = extract_role_settings(source)
    assert soul == "你是助教"
    assert user == "我叫小明"


def test_extract_implicit_concat_user() -> None:
    source = '''
def build_system_prompt():
    soul = "助教"
    user = (
        "我的名字叫Vans。"
        "請簡潔。"
    )
'''
    soul, user = extract_role_settings(source)
    assert soul == "助教"
    assert user == "我的名字叫Vans。請簡潔。"


def test_extract_missing_role_returns_none() -> None:
    source = "def build_system_prompt():\n    return {}\n"
    soul, user = extract_role_settings(source)
    assert soul is None
    assert user is None
