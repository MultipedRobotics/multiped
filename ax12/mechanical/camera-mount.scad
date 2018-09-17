$fn = 90;
use <lib/misc.scad>;
use <lib/pi.scad>;

module cameramount(){
    offset = 3;
    difference(){
        translate([-49/2,0,0])cube([49, 15, offset]);
        translate([20,10,0]) M3(20);
        translate([-20,10,0]) M3(20);
        translate([0,10,0]) M3(20);
    }
    difference(){
        translate([-49/2,0,offset])cube([49, 3, 30]);
        translate([-49/2+3,-1,3+offset])cube([4, 10, 24]);
        translate([49/2-7,-1,3+offset])cube([4, 10, 24]);
    }
}

cameramount();
