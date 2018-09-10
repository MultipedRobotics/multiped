//$fn = 50;

// library folder
use <lib/robotis_parts.scad>;
use <lib/misc.scad>;
use <lib/pi.scad>;

// this folder
//use <tibia.scad>;
//use <femur.scad>;
//use <tarsus.scad>;
//use <coxa.scad>;
//use <head.scad>;
//use <sternum.scad>;

/* module piFootPrint(depth=10){
    hole = 2.8; // mm
    dx = 58;
    dy = 49;
    translate([-dx/2,-dy/2,0]){
        cylinder(h=depth, d=hole, center=true);
        translate([dx,0,0]) cylinder(h=depth, d=hole, center=true);
        translate([0,dy,0]) cylinder(h=depth, d=hole, center=true);
        translate([dx,dy,0]) cylinder(h=depth, d=hole, center=true);
    }
} */

module powerFootPrint(){
    // board dimensions
    x = 42.2;
    y = 31.8;
    height = 10;

    translate([x/2-2.2, y/2-2.2, 0]) cylinder(d=2.2, h=height, center=true);
    translate([x/2-2.2, -y/2+4.2, 0]) cylinder(d=2.2, h=height, center=true);
    translate([-x/2+2.2, -y/2+4.2, 0]) cylinder(d=2.2, h=height, center=true);
    translate([-x/2+2.2, y/2-2.2, 0]) cylinder(d=2.2, h=height, center=true);

    // counter sink
    m2h = 2.5;
    m2d = 5;
    // hex(3.5, m2h);
    translate([x/2-2.2, y/2-2.2, -0.5]) cylinder(d=m2d, h=m2h, center=false);
    translate([x/2-2.2, -y/2+4.2, -0.5]) cylinder(d=m2d, h=m2h, center=false);
    translate([-x/2+2.2, -y/2+4.2, -0.5]) cylinder(d=m2d, h=m2h, center=false);
    translate([-x/2+2.2, y/2-2.2, -0.5]) cylinder(d=m2d, h=m2h, center=false);
}


module M2standoff(x,y,z,h){
    dia = 2.5;
    wide = 3;

    translate([x,y,z]) difference(){
        cylinder(h=h, d=dia+wide);
        cylinder(h=4*h, d=dia, center=true);
    }
}


module powerStandoff(height){
    // board dimensions
    x = 42.2;
    y = 31.8;

    M2standoff(x/2-2.2, y/2-2.2, 0, height);
    M2standoff(x/2-2.2, -y/2+4.2, 0, height);
    M2standoff(-x/2+2.2, -y/2+4.2, 0, height);
    M2standoff(-x/2+2.2, y/2-2.2, 0, height);
}

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
    // light blue - Vin
    // dark blue - Vout
    translate([-x/2+7.62,-y/2,board/2]) color("blue") cube([7, 6, 9]);
    translate([x/2-7-7.62,-y/2,board/2]) color("lightblue") cube([7, 6, 9]);

    // SMT
    translate([-x/2+5,-y/2+6,board/2]) color("silver") cube([x-10, y-7, 8]);
    translate([-x/2+5,-y/2+6,-board/2-2]) color("silver") cube([x-10, y-7, 2]);
}

//difference(){
//    cylinder(h=4, d=101.25);
//    translate([0,0,-1]) cylinder(20,d=20);  // cable hole
//}
//base(135);
//rotate([0,0,45]){
//translate([0, 27,10]) power_board();
//translate([0,-27,10]) rotate([0,0,180]) power_board();
//}



//module HeadMount(dia=40, h=10){
//    translate([0,0,0]) union(){
//        // pi zero mounting holes
////        rotate([0, 90, 0])  translate([-65/2-20-5,0,1]) backboard();
//        // circular base
//        difference(){
//            cylinder(h,d=dia, center=false); // hub
//            cylinder(2*h,d=20,center=false); // wire pass through
//            translate([0,0,-1]) cylinder(h/2+1,d=3*20/2,center=false); // inner rim
//        }
//        plen = 25;
//        // support pilar - left
//        translate([0,15,h/2]) rotate([0,0,-90]) difference(){
//            cylinder(plen,d=10);
//        }
//        // support pilar - right
//        translate([0,-15,h/2]) difference(){
//            cylinder(plen,d=10);
//        }
//    }
//}

//module head(){
//    h = 110;
//    d = 75;
//    translate([0,0,-20]) rotate([0,0,90]) HeadMount();
//
//    difference()
//    {
//        translate([-d/2,-1.5,0]) cube([d,3,h]);  // base plate
//        rotate([90,90,0]) translate([-70,0,0]) piFootPrint();
//        translate([5,0,35]) rotate([90,90,0]) powerFootPrint();
//        translate([5,0,80]) rotate([90,90,0]) powerFootPrint();
//    }
//    rotate([0,90,90]) translate([-60,0,5]) rpi3();
//    //rotate([0,90,0]) translate([0,0,0]) picamera();
//    translate([5,-10,35]) rotate([90,90,0]) power_board();
//    translate([5,-10,80]) rotate([90,90,0]) power_board();
//    color("red", 0.25) cylinder(h=h, d=d);
//}


//module neck(outer=40, inner=25, len=70){
//    difference(){
//        union(){
//            ch = outer/3;
//            cylinder(ch,r1=outer/2, r2=inner/2, center=false);
//            translate([0,0,len-ch]) cylinder(ch,r1=inner/2, r2=outer/2, center=false);
//            translate([0,0,len]) cylinder(4,d=29, center=false);
//            cylinder(len, d=inner, center=false);
//        }
//        cylinder(len*5, d=20, center=true);
//    }
//}

//module top2(){
//	thick = 4;
//    base(135);
//    neck = 15;
//    difference(){
//        translate([0,0,neck/2+thick/2]) cylinder(neck, d2=20, d1=55, center=true);
//        translate([0,0,neck/2+thick/2]) cylinder(2*neck,d=20, center=true);
//    }
//    neck(len=40);
//}

//top2();
//neck(len=40);
//translate([0,0,40]) rotate([0,0,90]) HeadMount();
//translate([0,0,40+20]) head();
