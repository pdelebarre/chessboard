# CAD / fabrication

The V0.1 mechanical design is based on standard 4040 T-slot extrusion and an 8×8 board.

## Baseline parameters

- Square: 50 mm
- Playing area: 400 × 400 mm
- Nominal frame outside: 480 × 480 mm
- Frame profile: 4040 I-type slot 8
- Frame profile height: 40 mm
- Nominal rail envelope: 440 mm
- CoreXY usable travel target: ~400 mm
- Carriage: 70 × 70 mm
- Belt: GT2, 6 mm
- Pulleys: 20 tooth target
- Motors: 2 × NEMA 17
- Hall sensors: 64 at 50 mm pitch

The design should remain scalable by changing `square`; derived dimensions should be calculated from it.

## Parametric model

Open `chessboard_v01.scad` in OpenSCAD and set:

```scad
PART = "assembly";
```

to one of:

- `assembly` — complete design envelope
- `frame` — 4040 frame envelope
- `board` — 400×400 mm board surface
- `rails` — purchased linear-rail envelope
- `carriage` — printable carriage envelope
- `sensor_plate` — 400×400 mm Hall sensor PCB envelope
- `piece_base` — printable magnetic piece base

## Print workflow

For the Bambu printer:

1. Set `PART = "carriage"`.
2. Render with F6.
3. Export STL.
4. Open the STL in Bambu Studio.
5. Print functional mechanical parts in PETG.
6. Print the magnetic piece base in PETG or PLA for the first fit test.

The carriage is deliberately smaller than 256 mm in every dimension so it fits a desktop printer with a 256 mm class build volume.

## Manufacturing principle

No custom aluminium machining is required for V0.1. Order standard extrusion pre-cut to length, use catalogue brackets/T-nuts, and 3D-print the custom brackets, carriage and mounts.

## Important V0.1 limitation

`chessboard_v01.scad` is currently an **interface/envelope CAD**, not the final precision mechanical drawing. The exact linear rail family, bearing block geometry, belt routing and motor mounting-hole pattern must be frozen before manufacturing final mounts.

Correct sequence:

```text
select rail + bearing family
        ↓
freeze mounting dimensions
        ↓
update CAD parameters
        ↓
print mounts
        ↓
assemble
```

Do not manufacture precision mounts from guessed rail dimensions.
