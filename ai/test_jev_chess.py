import chess
from jev_chess import JevChessPolicy

class FakeChoice:
    choice = "e2e4"
    probabilities = {"e2e4": 0.9}
    confidence = 0.9

class FakeResponse:
    answers = {"move": FakeChoice()}

class FakeClient:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def system_one(self, *, state, questions):
        assert state["fen"]
        assert "e2e4" in questions["move"].criteria
        return FakeResponse()

def test_jev_filters_to_legal_candidates():
    board = chess.Board()
    decision = JevChessPolicy(FakeClient()).choose(board, [chess.Move.from_uci("e2e4")])
    assert decision.move == chess.Move.from_uci("e2e4")
    assert decision.confidence == 0.9

def test_illegal_candidate_is_rejected():
    board = chess.Board()
    try:
        JevChessPolicy(FakeClient()).choose(board, [chess.Move.from_uci("e2e5")])
    except ValueError as exc:
        assert "legal candidate" in str(exc)
    else:
        raise AssertionError("Expected illegal candidate to be rejected")
