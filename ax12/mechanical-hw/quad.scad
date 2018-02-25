$fn=50;

use <sternum.scad>;
use <tarsus.scad>;
use <head.scad>;
use <common.scad>;

/* module ax12(){
    // sort of center mass
    translate([-70,-210,-180]) import("parts/AX-12A.STL");
}

module femur2(L){
    ;
}

module rpi3(){
    // sort of center mass
    translate([-3-88.5/2,-2-56/2,0]) import("parts/rpi3.STL");
}

module f2(){
    // sort of center mass
    translate([0,0,0]) import("parts/f2.stl");
} */


color("SkyBlue") top();
color("gray") translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,90]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,180]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,270]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();

color("SkyBlue") rotate([0,0,45]) translate([0,0,4]) rpi_base();
color("ForestGreen") rotate([0,0,45]) translate([11,0,20]) rpi3();

color("SkyBlue") bottom();

color("lightgray") translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,90])  translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,180]) translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,270]) translate([0,-67,-16]) f2();
