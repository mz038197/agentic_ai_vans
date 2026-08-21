from pathlib import Path

from add_dungeon_starter.cli import main
from add_dungeon_starter.core import STARTER_FILES


def test_cli_writes_then_skips_existing(tmp_path: Path, capsys, monkeypatch) -> None:
    templates = {name: f"t-{name}" for name in STARTER_FILES}
    monkeypatch.setattr("add_dungeon_starter.cli.fetch_template", templates.__getitem__)

    assert main(["-C", str(tmp_path)]) == 0
    first = capsys.readouterr()
    assert "已寫入" in first.out
    assert (tmp_path / "main.py").read_text(encoding="utf-8") == "t-main.py"

    assert main(["-C", str(tmp_path)]) == 0
    second = capsys.readouterr()
    assert "未覆寫" in second.out
