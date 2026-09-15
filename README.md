# Autonomous Chessboard — Webots MVP

A Webots simulation of an autonomous chessboard where the opponent's pieces move by themselves.

## MVP

- 8×8 physical chessboard
- Passive chess pieces represented as Webots `Solid` nodes
- Under-board CoreXY-style carriage visualization
- Electromagnet visualization beneath the active piece
- Human move simulation: press `1` to play **e2-e4**
- AI response: black pawn automatically moves **e7-e5**
- Robot animation interpolates the opponent piece between squares
- Capture-ready architecture for the next iteration
- Reset with `R`
- Automatic demo with `D`

## Run

Open `webots/worlds/chessboard.wbt` in Webots and start the simulation.

Keyboard controls:

| Key | Action |
|---|---|
| `1` | Simulate human move e2-e4, then trigger AI e7-e5 |
| `D` | Run the autonomous movement demo |
| `R` | Reset the board |
| `ESC` | Stop Webots |

## Architecture

```text
Webots world
    │
    └── chessboard_controller.py
          ├── Game state / move simulation
          ├── Move planner
          ├── Robot motion interpolation
          └── Electromagnet state

Future hardware mapping:

Raspberry Pi / game service
        │
        │ USB / serial
        ▼
      ESP32
        │
        ├── Hall sensors
        ├── Stepper drivers
        ├── CoreXY
        └── Electromagnet
```

This MVP intentionally keeps the chess rules and AI simple. The next stage should replace the scripted AI move with Stockfish/python-chess and replace simulated sensor events with 64 Hall sensors.
