from __future__ import annotations

from pathlib import Path

import main_shell
import pytest
from langchain_core.messages import AIMessage
from peas_agent_runtime.contract import check_agent_factory


class FakeLLM:
    def __init__(self, responses: list):
        self.responses = list(responses)
        self.calls: list = []

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self.calls.append(messages)
        if not self.responses:
            return AIMessage(content="fallback")
        return self.responses.pop(0)


def test_host_context_merged_into_system() -> None:
    msg = main_shell.build_system_prompt("路徑規則")
    assert isinstance(msg, dict)
    assert msg["role"] == "system"
    assert "角色設定" in msg["content"]
    assert "# Host Environment" in msg["content"]
    assert "路徑規則" in msg["content"]


def test_default_session_path(tmp_path: Path) -> None:
    llm = FakeLLM([AIMessage(content="ok")])
    agent = main_shell.Agent(llm=llm, tools=[], base_dir=tmp_path)
    agent.chat("hi")
    path = tmp_path / "sessions" / "session.jsonl"
    assert path.is_file()
    assert agent.session.path == path.resolve()


def test_chat_without_tools_saves_session(tmp_path: Path) -> None:
    session = tmp_path / "sessions" / "s.jsonl"
    session.parent.mkdir()
    session.touch()
    llm = FakeLLM([AIMessage(content="你好")])
    agent = main_shell.Agent(
        llm=llm,
        tools=[],
        session_path=str(session.relative_to(tmp_path)),
        host_context="HOST",
        base_dir=tmp_path,
    )
    answer = agent.chat("嗨")
    assert answer == "你好"
    assert llm.calls[0][0]["role"] == "system"
    assert "# Host Environment" in llm.calls[0][0]["content"]
    assert "HOST" in llm.calls[0][0]["content"]
    assert agent.history[0]["role"] == "user"
    assert agent.history[0]["content"] == "嗨"
    assert agent.history[1]["role"] == "assistant"
    assert agent.history[1]["content"] == "你好"
    reloaded = main_shell.SessionStore(
        str(session.relative_to(tmp_path)), base_dir=tmp_path
    ).load()
    assert reloaded[0]["role"] == "user"
    assert reloaded[0]["content"] == "嗨"
    assert reloaded[1]["content"] == "你好"
    assert "timestamp" in reloaded[0]


def test_chat_tool_call_round_trip(tmp_path: Path) -> None:
    session = tmp_path / "sessions" / "tool.jsonl"
    session.parent.mkdir()
    session.touch()

    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "calculator",
                    "args": {"a": 12, "b": 5, "operation": "multiply"},
                    "id": "call_1",
                }
            ],
        ),
        AIMessage(content="答案是 60。"),
    ]
    llm = FakeLLM(responses)
    agent = main_shell.Agent(
        llm=llm,
        tools=[main_shell.calculator],
        session_path=str(session.relative_to(tmp_path)),
        base_dir=tmp_path,
    )
    answer = agent.chat("12 × 5")
    assert answer == "答案是 60。"
    assert agent.history[1]["role"] == "assistant"
    assert agent.history[1]["tool_calls"][0]["id"] == "call_1"
    assert agent.history[2]["role"] == "tool"
    assert agent.history[2]["tool_call_id"] == "call_1"
    assert agent.history[2]["content"] == "60.0" or agent.history[2]["content"] == "60"
    history = agent.session.load()
    assert len(history) == 4
    assert history[1]["tool_calls"][0]["id"] == "call_1"
    assert history[2]["tool_call_id"] == "call_1"


def test_unknown_tool_writes_error_tool_message(tmp_path: Path) -> None:
    session = tmp_path / "sessions" / "unk.jsonl"
    session.parent.mkdir()
    session.touch()
    llm = FakeLLM(
        [
            AIMessage(
                content="",
                tool_calls=[{"name": "missing", "args": {}, "id": "x"}],
            ),
            AIMessage(content="我無法使用該工具"),
        ]
    )
    agent = main_shell.Agent(
        llm=llm,
        tools=[main_shell.calculator],
        session_path=str(session.relative_to(tmp_path)),
        base_dir=tmp_path,
    )
    agent.chat("go")
    assert agent.history[2]["role"] == "tool"
    assert "not found" in agent.history[2]["content"]


def test_image_path_raises_not_silently_ignored(tmp_path: Path) -> None:
    session = tmp_path / "sessions" / "img.jsonl"
    session.parent.mkdir()
    session.touch()
    llm = FakeLLM([AIMessage(content="看到了")])
    agent = main_shell.Agent(
        llm=llm,
        tools=[],
        session_path=str(session.relative_to(tmp_path)),
        base_dir=tmp_path,
    )
    with pytest.raises(NotImplementedError, match="image_path"):
        agent.chat("看圖", image_path="uploads/chat_images/a.png")
    assert session.read_text(encoding="utf-8") == ""
    assert agent.history == []


def test_contract_main_shell() -> None:
    result = check_agent_factory(
        "main_shell:create_agent",
        project_root=Path(__file__).resolve().parent.parent,
    )
    hard = [m for m in result.messages if not m.startswith("提示：")]
    assert hard == []
    assert result.ok or all("chat" in m or "提示" in m for m in result.messages)
    assert not any("host_context" in m for m in hard)
