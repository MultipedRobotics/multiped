$fn=100;

use <sternum.scad>;
/* use <tarsus.scad>; */
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
module picamera(){
    // sort of center mass
    color("ForestGreen") translate([-25/2,0,0]) import("parts/pi-camera.stl");
}

rotate([0,0,-45]) rotate([90,0,0]) translate([-15,20,85/2-3]){
	cube([30,20,2]);
	translate([0,5,0]) rotate([90,0,0]) cylinder(25,d=6);
	translate([30,5,0]) rotate([90,0,0]) cylinder(25,d=6);
}

//rotate([0,0,-45]) rotate([90,0,0]) translate([0,20,85/2]) picamera();
//
//color("SkyBlue") rotate([0,0,45]) head();

/* rotate([0,0,45]) rotate([0,90,0]) rotate_extrude($fn=200) translate([65/2,0,0]) square([10,3]); // circle(d=10); */
h = 30;
/* rotate([0,0,45]) translate([0,85/2-2.5,0]) scale([2,.5,1]) cylinder(h,d=10);
rotate([0,0,45]) translate([0,85/2-2.5-10,h]) cube([20,30,5], center=true); */

//color("ForestGreen") rotate([0,0,45]) translate([11,0,10]) rpi3();


color("SkyBlue") top();
/* color("gray") translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,90]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,180]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,270]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12(); */

/* color("SkyBlue") rotate([0,0,45]) translate([0,0,4]) rpi_base(); */
/* color("ForestGreen") rotate([0,0,45]) translate([11,0,10]) rpi3(); */

/* color("SkyBlue") bottom(); */

/* color("lightgray") translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,90])  translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,180]) translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,270]) translate([0,-67,-16]) f2(); */
