# Jev chess AI

This package adds TypeSafe Jev as the decision layer for the autonomous chessboard.

Architecture:

human/remote move -> python-chess legality/state -> optional Stockfish candidate generation -> Jev semantic reranking -> deterministic safety validation -> ESP32/Webots motion

Jev is deliberately not the chess rules engine. python-chess remains authoritative for legality. If Stockfish is available, it supplies a shortlist and Jev chooses among those already-legal candidates. The robot receives only a structured UCI move such as e7e5; free-form model output is never sent to the motion controller.

Setup:

    cd ai
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    export TYPESAFE_API_KEY="..."

The official TypeSafe Python SDK reads TYPESAFE_API_KEY and exposes typed Choice/Score/Noul decisions. See https://github.com/typesafe-ai/typesafe-sdk-python.

Production flow:

1. Hall-sensor layer reports the human move.
2. python-chess validates it.
3. Stockfish generates candidate moves.
4. Jev reranks the candidates using the board state and playing style.
5. A deterministic safety layer validates Jev's selected UCI move again.
6. ESP32 receives the structured command.
7. Motion executes and sensor feedback confirms the physical move.
