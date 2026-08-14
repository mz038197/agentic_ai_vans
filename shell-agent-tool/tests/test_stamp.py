from pathlib import Path

from add_shell_agent.core import extract_role_settings, stamp_template


def test_stamp_replaces_soul_and_user_in_template() -> None:
    template = """
def build_system_prompt(host_context=None):
    soul = "模板助教"
    user = "模板使用者"
    return soul
"""
    stamped = stamp_template(template, soul="學生助教", user="學生使用者")
    soul, user = extract_role_settings(stamped)
    assert soul == "學生助教"
    assert user == "學生使用者"


def test_stamp_keeps_template_role_when_missing() -> None:
    template = """
def build_system_prompt():
    soul = "模板助教"
    user = "模板使用者"
"""
    stamped = stamp_template(template, soul=None, user=None)
    soul, user = extract_role_settings(stamped)
    assert soul == "模板助教"
    assert user == "模板使用者"


def test_stamp_real_vans_template() -> None:
    template_path = Path(__file__).resolve().parents[2] / "main_shell.py"
    template = template_path.read_text(encoding="utf-8")
    stamped = stamp_template(template, soul="課堂助教", user="課堂學生")
    soul, user = extract_role_settings(stamped)
    assert soul == "課堂助教"
    assert user == "課堂學生"
    assert "vcr_sk_" not in stamped
