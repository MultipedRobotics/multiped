use <common.scad>
use <pulley.scad>

$fn=45;

module bodyHoles(x=0,y=0,z=0){
    center = true;
    height = 15;
    hole = 2.15; // 4.1 mm diameter
    hdist = 6; // 6 mm center to center distance
    vdist = 6; // 18 mm center to center distance
    translate([x,y-3.5,z]){
//        translate([0,9,0]) cube([height,10,14], center);
        bottomHoles(0, vdist+18, 0);
        bottomHoles(0, vdist+12, 0);
        bottomHoles(0, vdist+6, 0);
        bottomHoles(0, vdist, 0);
        bottomHoles(0, 0, 0);
    }
}

module u_frame(length=18){
    /*
    Makes a u frame connected to the horn. The bottom of the horn can mount the back or
    side of a servo motor with a hole to pass the cable through.

    length - measured from the bottom of the u to the center horn hole (piviot point) in mm
    */
    fillets = true;
    difference() {
            union(){
                cube([20,34,2], true);
                translate([0,32/2,length/2]){
                    cube([20,2,length+2], true);
                    translate([0,0,length/2]) rotate([90,0,0]) cylinder(2,10,10, true);
                }
                translate([0,-32/2,length/2]){
                    cube([20,2,length+2], true);
                    translate([0,0,length/2]) rotate([90,0,0]) cylinder(2,10,10, true);
                }
                rr=2;
                translate([0,32/2-2,length]) rotate([90,0,0]) pulley();
                if(fillets){
                    render(convexity=2) difference(){
                        translate([0,32/2-1,1]) rotate([0,90,0]) cylinder(20,rr,rr, true);
                        translate([0,32/2-3,3]) rotate([0,90,0]) cylinder(20,rr,rr, true);
                    }
                    render(convexity=2) difference(){
                        translate([0,-32/2+1,1]) rotate([0,90,0]) cylinder(20,rr,rr, true);
                        translate([0,-32/2+3,3]) rotate([0,90,0]) cylinder(20,rr,rr, true);
                    }
                }
            }
        translate([0,34/2,length]) rotate([90,0,0]) hornHoles();
        translate([0,-34/2,length]) rotate([90,0,0]) hornHoles();
        translate([0,-34/4,0]) bodyHoles();
    }
}

u_frame();
