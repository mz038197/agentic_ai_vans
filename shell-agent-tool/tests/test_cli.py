from pathlib import Path

from add_shell_agent.cli import main


def test_cli_writes_then_skips_existing(tmp_path: Path, capsys, monkeypatch) -> None:
    (tmp_path / "main.py").write_text(
        "def build_system_prompt():\n"
        '    soul = "助教"\n'
        '    user = "學生"\n',
        encoding="utf-8",
    )
    template = (
        "def build_system_prompt(host_context=None):\n"
        '    soul = "模板助教"\n'
        '    user = "模板使用者"\n'
    )
    monkeypatch.setattr("add_shell_agent.cli.fetch_template", lambda: template)

    assert main(["-C", str(tmp_path)]) == 0
    first = capsys.readouterr()
    assert "已寫入" in first.out
    assert (tmp_path / "main_shell.py").is_file()

    assert main(["-C", str(tmp_path)]) == 0
    second = capsys.readouterr()
    assert "未覆寫" in second.out


def test_cli_fails_without_main_py(tmp_path: Path, capsys) -> None:
    assert main(["-C", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "main.py" in err
