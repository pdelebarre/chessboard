// Autonomous Chessboard V0.1 - parametric mechanical envelope
// Units: millimetres
// Open with OpenSCAD. Set PART to "assembly", "frame", "board",
// "rails", "carriage", "piece_base", or "sensor_plate".
//
// Manufacturing intent:
// - 4040 T-slot frame, cut-to-length by supplier
// - 400 x 400 mm playing surface (50 mm squares)
// - 3D printed carriage and magnetic piece base
// - This is an envelope/prototype model; precision rail/belt mounting
//   holes are deliberately kept as purchased-component interfaces.

$fn = 64;

square = 50;
board_n = 8;
play = square * board_n;                 // 400
frame_outer = 480;
profile = 40;
frame_inner = frame_outer - 2*profile;  // 400
frame_h = 40;
board_t = 8;

base_z = 40;
board_z = base_z + frame_h + 2;
carriage_size = 70;
carriage_h = 14;

magnet_d = 12;
magnet_h = 4;
piece_base_d = 24;
piece_base_h = 5;

rail_margin = 20;
rail_length = play + 2*rail_margin;     // 440

PART = "assembly";

module profile4040(len) {
    // Simplified solid representation of 40x40 extrusion.
    cube([len, profile, profile]);
}

module frame() {
    color("silver") {
        translate([0,0,base_z]) profile4040(frame_outer);
        translate([0,frame_outer-profile,base_z]) profile4040(frame_outer);
        translate([0,profile,base_z]) rotate([0,0,90]) profile4040(frame_outer-2*profile);
        translate([frame_outer-profile,profile,base_z]) rotate([0,0,90]) profile4040(frame_outer-2*profile);
    }
}

module chessboard() {
    translate([profile,profile,board_z]) {
        for (x=[0:7])
            for (y=[0:7])
                color(((x+y)%2==0) ? "ivory" : "black")
                    translate([x*square,y*square,0])
                        cube([square,square,board_t]);
    }
}

module xy_rails() {
    // Visual envelope only. Actual purchased linear rails are mounted
    // beneath the board, parallel to X/Y.
    color("dimgray") {
        translate([profile, profile+rail_margin, base_z+frame_h+board_t+10])
            cube([rail_length, 12, 8]);
        translate([profile, frame_outer-profile-rail_margin-12, base_z+frame_h+board_t+10])
            cube([rail_length, 12, 8]);
        translate([profile+rail_margin, profile, base_z+frame_h+board_t+18])
            cube([12, rail_length, 8]);
        translate([frame_outer-profile-rail_margin-12, profile, base_z+frame_h+board_t+18])
            cube([12, rail_length, 8]);
    }
}

module carriage() {
    translate([frame_outer/2-carriage_size/2,
               frame_outer/2-carriage_size/2,
               board_z-30]) {
        color("orange") cube([carriage_size,carriage_size,carriage_h]);
        translate([carriage_size/2,carriage_size/2,-magnet_h])
            color("gray") cylinder(d=magnet_d,h=magnet_h);
        translate([carriage_size/2-6,carriage_size-3,carriage_h/2])
            cube([12,8,5]);
    }
}

module sensor_plate() {
    color("green") translate([profile,profile,base_z+5]) cube([play,play,2]);
    for (x=[0:7])
        for (y=[0:7])
            translate([profile+x*square+square/2,
                       profile+y*square+square/2,
                       base_z+7])
                color("black") cylinder(d=6,h=2);
}

module piece_base() {
    difference() {
        cylinder(d=piece_base_d,h=piece_base_h);
        translate([0,0,piece_base_h-magnet_h])
            cylinder(d=magnet_d+0.25,h=magnet_h+0.2);
    }
}

module assembly() {
    frame();
    chessboard();
    xy_rails();
    carriage();
    sensor_plate();
}

if (PART == "assembly") assembly();
if (PART == "frame") frame();
if (PART == "board") chessboard();
if (PART == "rails") xy_rails();
if (PART == "carriage") carriage();
if (PART == "sensor_plate") sensor_plate();
if (PART == "piece_base") piece_base();
