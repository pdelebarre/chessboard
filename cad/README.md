# Parametric CAD

The V0.1 mechanical design is based on standard 4040 T-slot extrusion and an 8x8 board.

## Baseline parameters

- Square: 50 mm
- Playing area: 400 x 400 mm
- Board outside: 460 x 460 mm
- Frame: 4040 extrusion
- Frame height: 80 mm
- CoreXY usable travel: 400 x 400 mm
- Carriage: approximately 70 x 70 mm
- Belt: GT2, 6 mm
- Pulleys: 20 tooth
- Motors: 2 x NEMA 17
- Hall sensors: 64 at 50 mm pitch

Keep these values centralized when implementing CAD generators. The board should be scalable by changing square size, with all derived dimensions calculated from it.

## Manufacturing principle

No custom aluminium machining is required for V0.1. Order standard extrusion pre-cut to length, use catalogue brackets/T-nuts, and 3D print the custom brackets, carriage and mounts.