from pathlib import Path

from add_dungeon_starter.core import STARTER_FILES, fetch_template, materialize



def test_skips_when_all_starter_files_exist(tmp_path: Path) -> None:
    for name in STARTER_FILES:
        (tmp_path / name).write_text("keep-me", encoding="utf-8")
    called: list[str] = []

    def read_template(name: str) -> str:
        called.append(name)
        return "NEW"

    result = materialize(tmp_path, read_template=read_template)
    assert result.status == "skipped"
    assert "未覆寫" in result.message
    assert called == []
    for name in STARTER_FILES:
        assert (tmp_path / name).read_text(encoding="utf-8") == "keep-me"


def test_writes_missing_starter_files(tmp_path: Path) -> None:
    templates = {name: f"content-{name}" for name in STARTER_FILES}
    result = materialize(tmp_path, read_template=templates.__getitem__)
    assert result.status == "written"
    assert "已寫入" in result.message
    for name in STARTER_FILES:
        assert (tmp_path / name).read_text(encoding="utf-8") == f"content-{name}"


def test_writes_only_missing_files_and_leaves_existing(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("keep-main", encoding="utf-8")
    templates = {name: f"content-{name}" for name in STARTER_FILES}
    result = materialize(tmp_path, read_template=templates.__getitem__)
    assert result.status == "written"
    assert (tmp_path / "main.py").read_text(encoding="utf-8") == "keep-main"
    assert (tmp_path / "level5_memory.py").read_text(encoding="utf-8") == "content-level5_memory.py"


def test_fails_when_read_template_raises_and_writes_nothing(tmp_path: Path) -> None:
    def boom(name: str) -> str:
        raise OSError("network")

    result = materialize(tmp_path, read_template=boom)
    assert result.status == "failed"
    assert "無法" in result.message
    for name in STARTER_FILES:
        assert not (tmp_path / name).exists()


def test_repo_starter_templates_match_file_list() -> None:
    root = Path(__file__).resolve().parents[2] / "dungeon-starter"
    for name in STARTER_FILES:
        assert (root / name).is_file(), name


def test_fetch_template_reads_local_dungeon_starter() -> None:
    text = fetch_template("main.py")
    assert "完成挑戰：用 print 輸出" in text



