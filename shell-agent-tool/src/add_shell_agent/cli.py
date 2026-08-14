from __future__ import annotations

import argparse
import sys
from pathlib import Path

from add_shell_agent.core import fetch_template, materialize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="從 vans 模板寫入 Shell Agent 檔，並填入 main.py 的角色設定。"
    )
    parser.add_argument(
        "-C",
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="學生專案根目錄（預設為目前目錄）",
    )
    args = parser.parse_args(argv)
    result = materialize(args.project_root, fetch_template=fetch_template)
    stream = sys.stderr if result.status == "failed" else sys.stdout
    print(result.message, file=stream)
    return 1 if result.status == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
