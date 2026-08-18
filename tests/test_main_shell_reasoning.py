from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from langchain_core.messages import AIMessage, AIMessageChunk

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main_shell import Agent, extract_answer_text, iter_chunk_deltas


class FakeStreamLLM:
    def __init__(self, rounds: list[list[AIMessageChunk]]) -> None:
        self._rounds = list(rounds)
        self._i = 0

    def bind_tools(self, tools):
        return self

    def stream(self, _messages):
        chunks = self._rounds[self._i]
        self._i += 1
        yield from chunks


class TestChunkDeltas(unittest.TestCase):
    def test_iter_chunk_deltas_routes_reasoning_and_text(self) -> None:
        reasoning_chunk = AIMessageChunk(
            content=[{"type": "reasoning", "reasoning": "先想"}]
        )
        text_chunk = AIMessageChunk(content=[{"type": "text", "text": "答案"}])

        self.assertEqual(list(iter_chunk_deltas(reasoning_chunk)), [("reasoning", "先想")])
        self.assertEqual(list(iter_chunk_deltas(text_chunk)), [("text", "答案")])

    def test_extract_answer_text_skips_reasoning_blocks(self) -> None:
        message = AIMessage(
            content=[
                {"type": "reasoning", "reasoning": "不要這段"},
                {"type": "text", "text": "只要這段"},
            ]
        )
        self.assertEqual(extract_answer_text(message), "只要這段")


class TestAgentReasoningStream(unittest.TestCase):
    def test_chat_streams_reasoning_then_text(self) -> None:
        llm = FakeStreamLLM(
            [
                [
                    AIMessageChunk(content=[{"type": "reasoning", "reasoning": "想一步"}]),
                    AIMessageChunk(content=[{"type": "text", "text": "你好"}]),
                ]
            ]
        )
        agent = Agent(llm, [], session_path=None, host_context="")
        reasoning: list[str] = []
        tokens: list[str] = []

        answer = agent.chat(
            "嗨",
            on_token=tokens.append,
            on_reasoning=reasoning.append,
        )

        self.assertEqual(reasoning, ["想一步"])
        self.assertEqual(tokens, ["你好"])
        self.assertEqual(answer, "你好")

    def test_chat_calls_on_stream_reset_between_tool_rounds(self) -> None:
        tool_chunk = AIMessageChunk(
            content=[{"type": "reasoning", "reasoning": "呼叫工具"}],
            tool_call_chunks=[
                {
                    "name": "calculator",
                    "args": '{"a": 1, "b": 2, "operation": "add"}',
                    "id": "call-1",
                    "index": 0,
                    "type": "tool_call_chunk",
                }
            ],
        )
        final_chunks = [
            AIMessageChunk(content=[{"type": "reasoning", "reasoning": "加完了"}]),
            AIMessageChunk(content=[{"type": "text", "text": "3"}]),
        ]
        llm = FakeStreamLLM([[tool_chunk], final_chunks])
        calculator = MagicMock()
        calculator.name = "calculator"
        calculator.invoke.return_value = 3
        agent = Agent(llm, [calculator], session_path=None, host_context="")
        resets: list[str] = []

        answer = agent.chat("1+2", on_stream_reset=lambda: resets.append("reset"))

        self.assertEqual(resets, ["reset"])
        self.assertEqual(answer, "3")
        calculator.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
