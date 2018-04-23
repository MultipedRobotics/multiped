$fn = 50;

// library folder
use <lib/robotis_parts.scad>;
use <lib/misc.scad>;
use <lib/pi.scad>;

// this folder
use <tibia.scad>;
use <femur.scad>;
use <tarsus.scad>;
use <coxa.scad>;
//use <head.scad>;
use <sternum.scad>;

module power_board(){
    // board dimensions
    x = 42.2;
    y = 31.8;
    board = 1.8;
    
    difference(){
        color("green") cube([x, y, board], center=true);
        translate([x/2-2.2, y/2-2.2, 0]) cylinder(d=2.2, h=5, center=true);
        translate([x/2-2.2, -y/2+4.2, 0]) cylinder(d=2.2, h=5, center=true);
        translate([-x/2+2.2, -y/2+4.2, 0]) cylinder(d=2.2, h=5, center=true);
        translate([-x/2+2.2, y/2-2.2, 0]) cylinder(d=2.2, h=5, center=true);
    }
    
    // terminal blocks
    translate([-x/2+7.62,-y/2,board/2]) color("blue") cube([7, 6, 9]); // power out
    translate([x/2-7-7.62,-y/2,board/2]) color("lightblue") cube([7, 6, 9]); // power in
    
    // SMT
    translate([-x/2+5,-y/2+6,board/2]) color("silver") cube([x-10, y-7, 8]);
    translate([-x/2+5,-y/2+6,-board/2-2]) color("silver") cube([x-10, y-7, 2]);
}

//difference(){
//    cylinder(h=4, d=101.25);
//    translate([0,0,-1]) cylinder(20,d=20);  // cable hole
//}
base(135);
rotate([0,0,45]){
translate([0, 27,10]) power_board();
translate([0,-27,10]) rotate([0,0,180]) power_board();
}