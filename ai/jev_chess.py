"""Jev decision layer for the autonomous chessboard."""
from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Iterable
import chess
from typesafe_sdk import Choice, TypeSafeClient

@dataclass(frozen=True)
class MoveDecision:
    move: chess.Move
    confidence: float
    probabilities: dict[str, float]

class JevChessPolicy:
    """Select one move from a small, already-legal candidate set using Jev."""
    def __init__(self, client: TypeSafeClient | None = None):
        if client is not None:
            self.client = client
        else:
            if not os.getenv("TYPESAFE_API_KEY"):
                raise RuntimeError("TYPESAFE_API_KEY is required for Jev")
            self.client = TypeSafeClient()

    def choose(self, board: chess.Board, candidates: Iterable[chess.Move], *, personality: str = "strong, calm and positional") -> MoveDecision:
        moves = list(candidates)
        legal = {m.uci(): m for m in board.legal_moves}
        moves = [m for m in moves if m.uci() in legal]
        if not moves:
            raise ValueError("No legal candidate moves supplied")
        labels = {m.uci(): self._describe_move(board, m) for m in moves}
        state = {"fen": board.fen(), "turn": "white" if board.turn else "black", "material": self._material(board), "check": board.is_check(), "legal_candidates": labels, "personality": personality}
        with self.client:
            response = self.client.system_one(state=state, questions={"move": Choice(instructions="Choose the chess move that best fits the position. Prefer a sound move that improves the position, addresses immediate threats, and matches the stated playing style. Never invent a move.", criteria=labels)})
        answer = response.answers["move"]
        selected = legal[answer.choice]
        probabilities = dict(answer.probabilities)
        confidence = float(getattr(answer, "confidence", max(probabilities.values())))
        return MoveDecision(selected, confidence, probabilities)

    @staticmethod
    def _describe_move(board: chess.Board, move: chess.Move) -> str:
        flags = []
        if board.is_capture(move): flags.append("capture")
        if move.promotion is not None: flags.append("promotion")
        if board.gives_check(move): flags.append("check")
        suffix = " (" + ", ".join(flags) + ")" if flags else ""
        return f"Play {board.san(move)}{suffix}. UCI={move.uci()}"

    @staticmethod
    def _material(board: chess.Board) -> dict[str, int]:
        values = {chess.PAWN:1, chess.KNIGHT:3, chess.BISHOP:3, chess.ROOK:5, chess.QUEEN:9, chess.KING:0}
        return {side: sum(len(board.pieces(pt, colour))*value for pt,value in values.items()) for side,colour in (("white",chess.WHITE),("black",chess.BLACK))}

def stockfish_candidates(board: chess.Board, *, engine, count: int = 8) -> list[chess.Move]:
    """Return top Stockfish candidates for Jev to rerank."""
    infos = engine.analyse(board, chess.engine.Limit(depth=16), multipv=count)
    if isinstance(infos, dict): infos = [infos]
    return [info["pv"][0] for info in infos if info.get("pv")]
