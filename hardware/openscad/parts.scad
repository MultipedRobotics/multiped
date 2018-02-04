use <common.scad>
use <pulley.scad>
use <u_frame.scad>
use <base_plate.scad>
use <top_plate.scad>
$fn=45;

//use <pi-zero/files/PiZero_1.2.scad>;

color("SkyBlue", 1) {
    //pulley();
	//u_frame(25);
    //main_plate();
    //base_plate();
    top_plate();
    //neck();
    //translate([0,0,10]) PiZeroBody();
}
