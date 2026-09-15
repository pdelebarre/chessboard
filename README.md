# Autonomous Chessboard — Webots MVP + V0.1 Hardware Design

A Webots simulation and manufacturable prototype design for an autonomous chessboard where the opponent's pieces move by themselves.

## Current status

- Webots MVP implemented.
- Parametric V0.1 mechanical CAD added under `cad/`.
- V0.1 BOM, aluminium cut list, PCB specification and assembly plan added under `docs/`.
- Recommended manufacturing workflow: cut-to-size 4040 extrusion + purchased linear rails + Bambu 3D-printed custom parts + Dutch PCB assembly.

## V0.1 hardware baseline

| Parameter | Value |
|---|---:|
| Chess square | 50 mm |
| Playing surface | 400 × 400 mm |
| Nominal outer frame | 480 × 480 mm |
| Frame profile | 4040 T-slot, slot 8 |
| Hall sensing | 64 positions |
| XY mechanism | CoreXY-style |
| Carriage | 70 × 70 mm |
| Piece magnet | 12 × 4 mm target |
| Controller | ESP32-S3 |
| Host | Raspberry Pi |

See:

- `cad/chessboard_v01.scad`
- `docs/v0.1-bom.md`
- `docs/v0.1-cut-list.md`
- `docs/v0.1-pcb-spec.md`
- `docs/v0.1-assembly.md`

## Recommended suppliers

### Aluminium

Motedis is the preferred supplier for the V0.1 frame because it offers standard aluminium profiles, cut-to-size ordering and single-piece orders. The design uses standard 4040 slot-8 profiles so no custom extrusion tooling is required.

### PCB

SST Hardware in the Netherlands is the preferred prototype PCB partner. They support single prototypes and small series, SMT/THT assembly, component sourcing and functional testing.

## Webots MVP

- 8×8 physical chessboard
- Passive chess pieces represented as Webots `Solid` nodes
- Under-board CoreXY-style carriage visualization
- Electromagnet visualization beneath the active piece
- Human move simulation: press `1` to play **e2-e4**
- AI response: black pawn automatically moves **e7-e5**
- Robot animation interpolates the opponent piece between squares
- Reset with `R`
- Automatic demo with `D`

## Run

Open `webots/worlds/chessboard.wbt` in Webots and start the simulation.

## Architecture

```text
                        Raspberry Pi 5
                              │
                    Stockfish + python-chess
                              │
                        USB / serial
                              │
                           ESP32-S3
                   ┌──────────┼──────────┐
                   │          │          │
               64 Hall     TMC2209    TMC2209
                sensors       │          │
                   │          └────┬─────┘
                   │               CoreXY
                   │                  │
                   └──────────── Electromagnet
```

The next software stage should replace the scripted Webots moves with Stockfish/python-chess and map the same interfaces to real ESP32 firmware.
