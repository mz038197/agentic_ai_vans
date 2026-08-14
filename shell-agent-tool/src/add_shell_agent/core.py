from __future__ import annotations

import ast
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TEMPLATE_URL = (
    "https://raw.githubusercontent.com/mz038197/agentic_ai_vans/master/main_shell.py"
)


@dataclass(frozen=True)
class MaterializeResult:
    status: str
    message: str
    used_template_role: bool = False


def extract_role_settings(source: str) -> tuple[str | None, str | None]:
    tree = ast.parse(source)
    soul: str | None = None
    user: str | None = None
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name != "build_system_prompt":
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                continue
            target = stmt.targets[0]
            if not isinstance(target, ast.Name) or target.id not in ("soul", "user"):
                continue
            value = _string_value(stmt.value)
            if value is None:
                continue
            if target.id == "soul":
                soul = value
            else:
                user = value
    return soul, user


def _string_value(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for part in node.values:
            if isinstance(part, ast.Constant) and isinstance(part.value, str):
                parts.append(part.value)
            else:
                return None
        return "".join(parts)
    return None


def stamp_template(template: str, *, soul: str | None, user: str | None) -> str:
    if soul is None and user is None:
        return template
    tree = ast.parse(template)
    edits: list[tuple[int, int, str]] = []
    wanted = {"soul": soul, "user": user}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name != "build_system_prompt":
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                continue
            target = stmt.targets[0]
            if not isinstance(target, ast.Name) or target.id not in wanted:
                continue
            replacement = wanted[target.id]
            if replacement is None:
                continue
            start = _offset(template, stmt.value.lineno, stmt.value.col_offset)
            end_lineno = stmt.value.end_lineno
            end_col = stmt.value.end_col_offset
            if end_lineno is None or end_col is None:
                continue
            end = _offset(template, end_lineno, end_col)
            edits.append((start, end, repr(replacement)))
    edits.sort(key=lambda item: item[0], reverse=True)
    raw = template.encode("utf-8")
    for start, end, text in edits:
        raw = raw[:start] + text.encode("utf-8") + raw[end:]
    return raw.decode("utf-8")


def _offset(source: str, lineno: int, col: int) -> int:
    lines = source.splitlines(keepends=True)
    prefix = "".join(lines[: lineno - 1])
    return len(prefix.encode("utf-8")) + col


def fetch_template(url: str = DEFAULT_TEMPLATE_URL) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "add-shell-agent"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def materialize(
    project_root: Path,
    *,
    fetch_template: Callable[[], str],
) -> MaterializeResult:
    root = project_root.resolve()
    dest = root / "main_shell.py"
    if dest.exists():
        return MaterializeResult("skipped", "已有 Shell Agent 檔，未覆寫。")
    main_py = root / "main.py"
    if not main_py.is_file():
        return MaterializeResult("failed", "找不到 main.py。")
    try:
        template = fetch_template()
    except OSError as exc:
        return MaterializeResult("failed", f"無法下載 Shell Agent 模板：{exc}")
    if not template.strip():
        return MaterializeResult("failed", "無法下載 Shell Agent 模板：內容為空。")
    soul, user = extract_role_settings(main_py.read_text(encoding="utf-8"))
    used_template_role = soul is None or user is None
    dest.write_text(stamp_template(template, soul=soul, user=user), encoding="utf-8")
    message = "已寫入 Shell Agent 檔。"
    if used_template_role:
        message += " 未在 main.py 找到 soul／user，已用模板預設人格。"
    return MaterializeResult("written", message, used_template_role=used_template_role)
