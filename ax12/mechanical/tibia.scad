$fn = 90;

use <lib/robotis_parts.scad>;
use <lib/misc.scad>;


module tibiaSupt(L, thick, rev=false){
    // makes the bar on the left/right of the tibbia
    // everything is drawn in 2D and then extruded into 3D
    angle = 0;
    dia = 22;
    difference(){
    translate([-L/2,0,0]) linear_extrude(thick){
        hull(){
            circle(d=dia);  // servo head
            translate([L/3,0,0]) circle(d=10);
        }
        if (rev){
            rotate([0,0,angle]) {
                translate([0,-(dia+5)/2,0]) square([dia,dia+5], center=true);
                translate([0,-dia-5,0]) circle(d=dia);
            }
        }
        else {
            rotate([0,0,angle]) {
                translate([0,(dia+5)/2,0]) square([dia,dia+5], center=true);
                translate([0,dia+5,0]) circle(d=dia);
            }
        }
        translate([L/3,-5,0]) square([L/3,10]);
        translate([2*L/3,0,0]) hull(){
            circle(d=10);
            translate([L/3,0,0]) circle(d=dia); // servo head
        }
    }
    if (rev){
        translate([-L/2-(dia+5)*sin(angle),-(dia+5)*cos(angle),0]) holes(2);  // hub
        translate([L/2,0,0]) pulleyHole();  // pulley head
    }
    else {
        translate([-L/2-(dia+5)*sin(angle),(dia+5)*cos(angle),0]) pulleyHole();  // hub
        translate([L/2,0,0]) holes(2);  // servo head
    }
}
}

module tibia(L=85){
    // hub outter: 10 mm
    // hub inner: 8 mm
    // hub thickness inner ring: 2 mm
    thick = 4;

    // middle support bar and wiring channel
    difference(){
        union(){
            translate([0,21,0]) rotate([-90,0,0]) tibiaSupt(L, thick, true);
            translate([0,-21,0]) rotate([90,0,0]) tibiaSupt(L, thick);

            difference(){
                cube([L/3,42,10], center=true);
                translate([-L/3/2,0,0]) scale([.5,1,1]) sphere(d=45);
                translate([L/3/2,0,0]) scale([.5,1,1]) sphere(d=45);
            }

            rotate([0,90,0]) scale([1,2.5,1]) cylinder(h=10,d=15, center=true);
        }
        cube([20,12,8], center=true);
        translate([-40,-25,0]) rotate([0,0,90]) cube([20,11,6], center=true);
        translate([28,25,0]) rotate([0,0,90]) cube([20,11,6], center=true);
    }
}

tibia();
//tibiaSupt(85, 4, true);
