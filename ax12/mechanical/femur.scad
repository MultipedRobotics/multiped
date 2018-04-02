//$fn = 50;

use <lib/robotis_parts.scad>;

//////////////////////////////////////////////////////
// Femur
//////////////////////////////////////////////////////
// arc - arclength in mm, this is the distance between motors
// angle - angular curve in degrees, this will be the angluar
//         offset between the motors
module femur(arc=60, angle=60){
//    servo_depth = mirror ? 2 : -3;
    servo_depth = 2;

    //w = 35;
    thick = 4; // servo_depth dependant on this!
    w = 36;
    ar = arc*360/(angle*2*PI);
    r = ar+w/2;
    dia = 2*r;
    translate([0,w-r,0])  // center
    difference()
    {
    difference()
    {
        cylinder(h=thick, d=dia);
        cylinder(h=15, d=dia-2*w,center=true);  // center hole
        rotate([0,0,-angle]) translate([0,0,-r/2]) cube([r,r,r]); // quadrant 2
        translate([0,-2*r,-r/2]) rotate([0,0,1]) cube([2*r,2*r,r]); // quadrant 1
        translate([-2*r,-2*r,-r/2]) cube([2*r,4*r,r]); // q 3 & 4

        // servos
//        translate([10,w/2,0]) rotate([0,0,0]) servo_mnt();
//        translate([25,w/2,0]) rotate([0,0,180]) servo_mnt();
    }
    rotate([0,0,-angle]) translate([-17,ar-1,0]) {
        servo_mnt(); // top mount
        translate([-2.5,-32/2,servo_depth]) cube([40,32,5], center=false);
    }
    translate([17,ar-1,0]) rotate([0,0,180]) {
        servo_mnt();  // bottom mount
        translate([-2.50,-32/2,servo_depth]) cube([40,32,5], center=false);
    }
    rotate([0,0,-angle/2]) translate([0,ar,0]) cube([8,12,10], center=true);
    }
}

//femur();
