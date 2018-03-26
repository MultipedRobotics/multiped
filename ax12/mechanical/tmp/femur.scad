$fn = 50;

use <common.scad>;
/* use <tarsus.scad>; */
use <misc.scad>;
use <sternum.scad>;

//////////////////////////////////////////////////////
// Femur
//////////////////////////////////////////////////////
//module femur_supt(){
//    color("SkyBlue") translate([10,70,-286]) import("other/femur.stl");
//}

module femur_supt(){
    difference(){
        w = 35;
        l = 80-16;
        translate([-l/2, -w/2,0]) cube([l, w, 4]);
        cube([8,12,10], center=true);
        translate([-14,0,0]) rotate([0,0,180]) servo_mnt();
        translate([14,0,0]) rotate([0,0,0]) servo_mnt();
        translate([14-2.5,-32/2,2]) cube([40,32,5], center=false);
        translate([-14+2.5,32/2,2]) rotate([0,0,180]) cube([40,32,5], center=false);
    }
}

module femur(L){
    rotate([0,90,90]) {
        ax12();
        rotate([0,0,180]) translate([0,-50/2+10,-3]) f2();
    }
    translate([70,0,0]) rotate([180,-90,90]) {
        ax12();
        /* rotate([0,0,180]) translate([0,-50/2+10,-3]) f2(); */
    }
    translate([35,15,-1]) rotate([90,0,180]) femur_supt();
    translate([35,-20,-1]) rotate([90,0,0]) femur_supt();
}

femur();
