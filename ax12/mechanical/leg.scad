$fn = 50;

use <common.scad>;
/* use <tarsus.scad>; */
use <misc.scad>;

/* module f2(){
    // sort of center mass
    color("lightgray") translate([0,0,0]) import("parts/F2.stl");
}

module f3(){
    // sort of center mass
    color("lightgray") translate([0,0,0]) import("parts/F3.stl");
}

module ax12(){
    // sort of center mass
    color("gray") translate([-70,-210,-180]) import("parts/AX-12A.STL");
} */

//////////////////////////////////////////////////////
// Tarsus
//////////////////////////////////////////////////////
module tarsus(){
    color("SkyBlue") difference(){
        union(){
            translate([0,0,50+3/2]) cube([35,25,3], center=true);
            // [x,y]
            // x = width
            // y = height
            /* points=[[0,0],[4,0],[4,1],[2,2],[2,8],[4,10],[0,10]]; // flat head */
            points=[[0,0],[1,1],[1,8],[2,10],[0,10]]; // thumb tack / screw
            rotate([0,0,0]) translate([0,0,0]) scale([6,6,5]) rotate_extrude($fn=200) polygon(points);
        }
        translate([0,0,50+3/2]) rotate([180,0,0]) holes(10);
    }
}



//////////////////////////////////////////////////////
// Femur
//////////////////////////////////////////////////////
module femur_supt(){
    color("SkyBlue") translate([10,70,-286]) import("other/femur.stl");
}

/* module tibia(){
    rotate([90,0,0]) translate([-6+8,145,-378+22]) import("other/tibia.stl");
    rotate([90,180,0]) translate([-6-8,145,-378-19]) import("other/tibia.stl");
    translate([-50,0,0]) rotate([0,-90,-90]) ax12();
} */

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


//////////////////////////////////////////////////////
// Tibia
//////////////////////////////////////////////////////
module pulleyHole(){
    cylinder(20, d=8.5, center=true);  // hub
    translate([0,0,3]) cylinder(20, d=11);  // 3mm?
}

module tibiaSupt(L, thick){
    difference(){
    translate([-L/2,0,0]) linear_extrude(thick){
        hull(){
            circle(d=22);  // servo head
            translate([L/3,0,0]) circle(d=10);
        }
        translate([L/3,-5,0]) square([L/3,10]);
        translate([2*L/3,0,0]) hull(){
            circle(d=10);
            translate([L/3,0,0]) circle(d=22); // servo head
        }
    }
    translate([-L/2,0,0]) pulleyHole();  // hub
    translate([L/2,0,0]) holes(2);  // servo head
    }
}

module tibia(L=85){
    // hub outter: 10 mm
    // hub inner: 8 mm
    // hub thickness inner ring: 2 mm
    thick = 4;
    color("SkyBlue") union(){
        translate([0,21,0]) rotate([-90,180,0]) tibiaSupt(L, thick);
        translate([0,-21,0]) rotate([90,0,0]) tibiaSupt(L, thick);

        difference(){
            cube([L/3,42,10], center=true);
            translate([-L/3/2,0,0]) scale([.5,1,1]) sphere(d=45);
            translate([L/3/2,0,0]) scale([.5,1,1]) sphere(d=45);
        }
    }
}

module fullLeg(){
    translate([42,30,0]){
        rotate([0,0,0])  femur();

        translate([127,-3,0]){
        tibia();
        translate([57,-2.75,-.5]) rotate([0,-90,90]) ax12();
        }
        rotate([0,-90,0]) translate([0,-2,-212]) rotate([90,0,0]) f3();
        rotate([0,-90,0]) translate([0,-2,-265]) rotate([0,0,90]) tarsus();
    }
}

//fullLeg();

use <sternum.scad>;

//translate([0,60,0]) femur_supt();

// square femur
//difference(){
//    w = 35;
//    l = 80-16;
//    translate([-l/2, -w/2,0]) cube([l, w, 4]);
//	cube([8,12,10], center=true);
//    translate([-14,0,0]) rotate([0,0,180]) servo_mnt();
//    translate([14,0,0]) rotate([0,0,0]) servo_mnt();
//    translate([14-2.5,-32/2,2]) cube([40,32,5], center=false);
//    translate([-14+2.5,32/2,2]) rotate([0,0,180]) cube([40,32,5], center=false);
//}
//translate([57,-2.75,-.5]) rotate([0,-90,90]) ax12();

module tarsus2(L=50){
    color("SkyBlue") difference(){
        union(){
            translate([0,0,L+3/2]) cube([35,25,3], center=true);
            // [x,y]
            // x = width
            // y = height
            /* points=[[0,0],[4,0],[4,1],[2,2],[2,8],[4,10],[0,10]]; // flat head */
//            points=[[0,0],[1,1],[1,8],[2,10],[0,10]]; // thumb tack / screw
//            rotate([0,0,0]) translate([0,0,0]) scale([6,6,5]) rotate_extrude($fn=200) polygon(points);
            translate([0,0,5]) cylinder(h=L-5,d=10);
            translate([0,0,L-10]) cylinder(h=10,d1=0,d2=20);
            cylinder(h=5,d1=0,d2=10);
        }
        translate([0,0,L+3/2]) rotate([180,0,0]) holes(10);
    }
}
tarsus2(100);