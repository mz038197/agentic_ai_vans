from __future__ import annotations

import argparse
import sys
from pathlib import Path

from add_dungeon_starter.core import fetch_template, materialize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="從 vans 起點模板寫入課程專案的課堂起點檔。"
    )
    parser.add_argument(
        "-C",
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="學生課程專案根目錄（預設為目前目錄）",
    )
    args = parser.parse_args(argv)
    result = materialize(args.project_root, read_template=fetch_template)
    stream = sys.stderr if result.status == "failed" else sys.stdout
    print(result.message, file=stream)
    return 1 if result.status == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
