# Autonomous Chessboard — Parametric Mechanical Design v0.1

## Design target

Build a 450–500 mm square autonomous chessboard using standard 40-series T-slot aluminium extrusion, with no user machining required.

The design is deliberately split into four layers:

1. **Chess surface** — 8×8 squares, nominally 50 mm each.
2. **Sensor layer** — 64 Hall-effect sensors, one per square.
3. **Motion layer** — CoreXY-style XY carriage below the sensor layer.
4. **Electronics/service layer** — ESP32, stepper drivers, electromagnet driver and Raspberry Pi.

## Baseline dimensions

| Parameter | V0.1 value |
|---|---:|
| Square size | 50 mm |
| Playing area | 400 × 400 mm |
| Board outer size | 460 × 460 mm |
| Frame profile | 4040 T-slot |
| Frame outside height | 80 mm |
| Approx. overall height | 110–130 mm |
| Moving carriage | ~70 × 70 mm |
| Magnet position | centred under active square |
| Sensor pitch | 50 mm |
| Design tolerance | ±0.2 mm printed parts; ±0.5 mm frame assembly |

The parameters are centralized in `cad/parameters.yaml`. Do not hard-code the 50 mm square size in generated parts.

## Mechanical architecture

```text
TOP
┌────────────────────────────────────────────┐
│             8 × 8 PLAYING AREA             │
│                 400 × 400                  │
├────────────────────────────────────────────┤
│       64 × Hall sensor PCB / matrix        │
├────────────────────────────────────────────┤
│                                            │
│          CoreXY XY motion plane            │
│               ┌────────┐                   │
│               │carriage│                   │
│               │  MAG   │                   │
│               └────────┘                   │
│                                            │
├────────────────────────────────────────────┤
│ ESP32 + drivers + Raspberry Pi service area│
└────────────────────────────────────────────┘
BOTTOM
```

## Why 4040 extrusion

4040 gives a rigid, square reference structure without requiring woodworking or custom metal fabrication. The first prototype should use commercially available profile, cut to length by the supplier. Brackets and T-nuts are standard catalogue items.

Use a single extrusion family wherever possible. Avoid mixing profile standards unless a component forces it.

## Manufacturing strategy

### Aluminium

Order **pre-cut standard profiles** from a supplier such as Motedis. No sawing, drilling or tapping should be required for V0.1.

### 3D printing

Print the carriage, motor mounts, belt clamps, sensor spacers, PCB supports and cable-management parts on the Bambu printer. Prefer PETG for structural parts and PLA for cosmetic prototypes.

### PCB

Use a PCB manufacturer/assembler such as SST Hardware or AISLER. The PCB should be designed around the 50 mm sensor pitch and mechanically constrained by the frame rather than screwed to every square.

## Motion concept

The carriage uses two fixed XY axes with GT2 belts. The two motors remain stationary at the frame. The carriage carries only the electromagnet and its driver wiring. This minimizes moving mass.

For V0.1, target:

- 400 mm usable travel
- 2× NEMA 17 motors
- GT2 6 mm belt
- 20-tooth pulleys
- linear rail or V-wheel guidance
- homing switches on both axes
- conservative acceleration to avoid pieces jumping or rotating

## Piece interface

Each piece gets a standardized magnetic puck:

- NdFeB disc: approximately Ø10–12 × 3–5 mm
- steel ballast washer
- smooth PTFE/UHMW contact surface
- magnet concentric with the piece

The robot does **not** need to identify the piece mechanically. Identity comes from the software chess state plus Hall occupancy.

## Electrical architecture

```text
                 Raspberry Pi
              game + Stockfish
                     │
                USB / serial
                     │
                   ESP32
       ┌─────────────┼─────────────┐
       │             │             │
  Hall sensors   stepper       electromagnet
    64 inputs     drivers          MOSFET
       │             │             │
   board state     CoreXY          coil
```

The ESP32 owns real-time motion and sensor acquisition. The Raspberry Pi owns chess rules, Stockfish, remote play and higher-level orchestration.

## V0.1 acceptance criteria

- All structural parts can be bought or printed; no manual metal machining.
- 8×8 board is mechanically square within 1 mm corner-to-corner.
- Carriage can reach all 64 square centres.
- Magnet can move a test piece from any square to any other square without leaving the board.
- Hall sensor layer can detect occupancy changes reliably.
- Homing is repeatable to better than 0.5 mm.
- Board can be assembled with common hex keys and a screwdriver.

## Next CAD step

Generate the frame, carriage and mounting parts from the parameters file, then validate the complete kinematic envelope in Webots before ordering the aluminium and PCB.