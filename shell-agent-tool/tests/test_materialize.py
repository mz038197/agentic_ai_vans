from pathlib import Path

from add_shell_agent.core import extract_role_settings, materialize

TEMPLATE = """
def build_system_prompt(host_context=None):
    soul = "模板助教"
    user = "模板使用者"
"""

MAIN_WITH_ROLE = """
def build_system_prompt():
    soul = "你是助教"
    user = "我叫小明"
"""


def test_skips_when_shell_agent_file_exists(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(MAIN_WITH_ROLE, encoding="utf-8")
    existing = tmp_path / "main_shell.py"
    existing.write_text("keep-me", encoding="utf-8")
    result = materialize(tmp_path, fetch_template=lambda: TEMPLATE)
    assert result.status == "skipped"
    assert existing.read_text(encoding="utf-8") == "keep-me"


def test_writes_stamped_shell_agent_file(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(MAIN_WITH_ROLE, encoding="utf-8")
    result = materialize(tmp_path, fetch_template=lambda: TEMPLATE)
    assert result.status == "written"
    soul, user = extract_role_settings(
        (tmp_path / "main_shell.py").read_text(encoding="utf-8")
    )
    assert soul == "你是助教"
    assert user == "我叫小明"


def test_fails_without_main_py(tmp_path: Path) -> None:
    result = materialize(tmp_path, fetch_template=lambda: TEMPLATE)
    assert result.status == "failed"
    assert "main.py" in result.message
    assert not (tmp_path / "main_shell.py").exists()


def test_fails_when_fetch_raises(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(MAIN_WITH_ROLE, encoding="utf-8")

    def boom() -> str:
        raise OSError("network")

    result = materialize(tmp_path, fetch_template=boom)
    assert result.status == "failed"
    assert not (tmp_path / "main_shell.py").exists()


def test_fails_when_template_empty(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(MAIN_WITH_ROLE, encoding="utf-8")
    result = materialize(tmp_path, fetch_template=lambda: "  \n")
    assert result.status == "failed"
    assert not (tmp_path / "main_shell.py").exists()


def test_writes_template_role_when_soul_user_missing(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        "def build_system_prompt():\n    return {}\n", encoding="utf-8"
    )
    result = materialize(tmp_path, fetch_template=lambda: TEMPLATE)
    assert result.status == "written"
    assert result.used_template_role is True
    soul, user = extract_role_settings(
        (tmp_path / "main_shell.py").read_text(encoding="utf-8")
    )
    assert soul == "模板助教"
    assert user == "模板使用者"


def test_does_not_copy_api_key(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        'api_key = "secret-key"\n'
        "def build_system_prompt():\n"
        '    soul = "助教"\n'
        '    user = "學生"\n',
        encoding="utf-8",
    )
    result = materialize(tmp_path, fetch_template=lambda: TEMPLATE)
    assert result.status == "written"
    written = (tmp_path / "main_shell.py").read_text(encoding="utf-8")
    assert "secret-key" not in written
