from __future__ import annotations

import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

STARTER_FILES = (
    "main.py",
    "level5_memory.py",
    "level6_tools.py",
    "level7_react.py",
    "level8_coding.py",
)

DEFAULT_BASE_URL = (
    "https://raw.githubusercontent.com/mz038197/agentic_ai_vans/master/dungeon-starter"
)


@dataclass(frozen=True)
class MaterializeResult:
    status: str
    message: str


def _local_template_dir() -> Path | None:
    candidate = Path(__file__).resolve().parents[3] / "dungeon-starter"
    if candidate.is_dir() and (candidate / "main.py").is_file():
        return candidate
    return None


def fetch_template(name: str) -> str:
    local = _local_template_dir()
    if local is not None:
        return (local / name).read_text(encoding="utf-8")
    url = f"{DEFAULT_BASE_URL}/{name}"
    request = urllib.request.Request(url, headers={"User-Agent": "add-dungeon-starter"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def materialize(
    project_root: Path,
    *,
    read_template: Callable[[str], str],
) -> MaterializeResult:
    root = project_root.resolve()
    missing = [name for name in STARTER_FILES if not (root / name).exists()]
    if not missing:
        return MaterializeResult("skipped", "已有課堂起點檔，未覆寫。")
    contents: dict[str, str] = {}
    try:
        for name in missing:
            contents[name] = read_template(name)
    except OSError as exc:
        return MaterializeResult("failed", f"無法下載起點模板：{exc}")
    for name, text in contents.items():
        (root / name).write_text(text, encoding="utf-8")
    return MaterializeResult("written", f"已寫入課堂起點檔：{', '.join(contents)}。")
