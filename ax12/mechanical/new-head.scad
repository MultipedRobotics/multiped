//$fn=150;
use <common.scad>;

translate([65,0,0]) cylinder(10,d=30, center=true);
rotate([90,0,0]){
    translate([70,50,5]) rotate([0,0,180]) rpi3();
    
    translate([120,55,18]) rotate([0,90,0]) picamera();
    
    difference(){
    cube([120,81,4]);
    scale([1,1.1]) cylinder(h=10,r=10+41,center=true);
    translate([120,0,0]) scale([2,1.1]) cylinder(h=10,r=20,center=true);
    }
}