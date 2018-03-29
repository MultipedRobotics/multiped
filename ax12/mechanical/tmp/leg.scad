$fn = 50;

use <../common.scad>;
/* use <tarsus.scad>; */
use <../misc.scad>;
use <../leg.scad>;
use <../head.scad>;

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
    color("SkyBlue") translate([10,70,-286]) import("../other/femur.stl");
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

use <../sternum.scad>;

//translate([0,60,0]) femur_supt();

//// old coxa
//module coxa(){
//    difference(){
//        w = 35;
//        l = 80-16;
//        translate([-l/2, -w/2,0]) cube([l, w, 4]);
//        cube([8,12,10], center=true);
//        translate([-14,0,0]) rotate([0,0,180]) servo_mnt();
//        translate([14,0,0]) rotate([0,0,0]) servo_mnt();
//        translate([14-2.5,-32/2,2]) cube([40,32,5], center=false);
//        translate([-14+2.5,32/2,2]) rotate([0,0,180]) cube([40,32,5], center=false);
//    }
//}

// arc - arclength in mm, this is the distance between motors
// angle - angular curve in degrees, this will be the angluar
//         offset between the motors
module coxa(arc, angle, mirror=false){
    servo_depth = mirror ? 2 : -3;
            
    //w = 35;
    thick = 4; // servo_depth dependant on this!
    w = 36;
    ar = arc*360/(angle*2*PI);
    r = ar+w/2;
    dia = 2*r;
    translate([0,w-r,0])  // center
    difference()
    {
    difference()
    {
        cylinder(h=thick, d=dia);
        cylinder(h=15, d=dia-2*w,center=true);  // center hole
        rotate([0,0,-angle]) translate([0,0,-r/2]) cube([r,r,r]); // quadrant 2
        translate([0,-2*r,-r/2]) rotate([0,0,1]) cube([2*r,2*r,r]); // quadrant 1
        translate([-2*r,-2*r,-r/2]) cube([2*r,4*r,r]); // q 3 & 4
        
        // servos
//        translate([10,w/2,0]) rotate([0,0,0]) servo_mnt();
//        translate([25,w/2,0]) rotate([0,0,180]) servo_mnt();
    }
    rotate([0,0,-angle]) translate([-17,ar-1,0]) {
        servo_mnt(); // top mount
        translate([-2.5,-32/2,servo_depth]) cube([40,32,5], center=false);
    }
    translate([17,ar-1,0]) rotate([0,0,180]) {
        servo_mnt();  // bottom mount
        translate([-2.50,-32/2,servo_depth]) cube([40,32,5], center=false);
    }
    rotate([0,0,-angle/2]) translate([0,ar,0]) cube([8,12,10], center=true);
    }
}


$fn=90;


module draw60(a0=0, a1=0, a2=0){
    translate([20,-15,15]) rotate([0,0,a0]){
        length=60;
        // 60 degrees
        coxa(length, 60, mirror=true);
        translate([0,0,-35]) coxa(length, 60);
        translate([-3,20-4,-13]) rotate([0,0,90]) ax12();
        translate([51,-13,-13]) rotate([0,0,270-60]) ax12();
        rotate([90,0,-60]) translate([53+85/2*cos(a1),-15, -38-85/2*sin(a1)]) rotate([0,a1,0]) {
            tibia();
            translate([43+15*cos(a2),-2.75,-15*sin(a2)]) rotate([0,-90,90]) rotate([0,0,-a2]) {
                ax12();
            
                rotate([-90,0,0]) translate([0,4,-25]) rotate([90,0,0]) f3();
                rotate([-90,0,0]) translate([0,4,-78]) rotate([0,0,90]) tarsus();
            }
        }
    }
}

module draw45(a0=0, a1=0, a2=0){
    translate([20,-15,15]) rotate([0,0,a0]){
        length=60;
        coxa(length, 45, mirror=true);
        translate([0,0,-35]) coxa(length, 45);
        translate([-3,20-4,-13]) rotate([0,0,90]) ax12();
        translate([56,-7,-13]) rotate([0,0,270-45]) ax12();
        rotate([90,0,-45]) translate([60+85/2*cos(a1),-15, -35-85/2*sin(a1)]) rotate([0,a1,0]){
            tibia();
            translate([43+15*cos(a2),-2.75,-15*sin(a2)]) rotate([0,-90,90]) rotate([0,0,-a2]) {
                ax12();
            
                rotate([-90,0,0]) translate([0,4,-25]) rotate([90,0,0]) f3();
                rotate([-90,0,0]) translate([0,4,-78]) rotate([0,0,90]) tarsus();
            }
        }
    }
}

// stand: 10, 100, 55
// stow:

module fullrobot(){
femur_angle = 100;
tibia_angle = 140;
tarsus_angle = 115;

//color("SkyBlue") top();
//draw45(-20,110,45);
translate([120,0,-20])
    rotate([-90,-femur_angle,0]) draw60(0,tibia_angle,tarsus_angle);
rotate([0,0,90])
    translate([120,0,-20])
        rotate([-90,-femur_angle,0]) draw60(0,tibia_angle,tarsus_angle);
rotate([0,0,180])
    translate([120,0,-20])
        rotate([-90,-femur_angle,0]) draw60(0,tibia_angle,tarsus_angle);
rotate([0,0,270])
    translate([120,0,-20])
        rotate([-90,-femur_angle,0]) draw60(0,tibia_angle,tarsus_angle);

color("SkyBlue") top();
color("gray") translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,90]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,180]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
color("gray") rotate([0,0,270]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12(); 

translate([0,0,20]){
color("SkyBlue") rotate([0,0,45]) translate([0,0,4]) rpi_base(); 
color("ForestGreen") rotate([0,0,45]) translate([11,0,10]) rpi3();
}

color("SkyBlue") bottom();

color("lightgray") translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,90])  translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,180]) translate([0,-67,-16]) f2();
color("lightgray") rotate([0,0,270]) translate([0,-67,-16]) f2();
}

//fullrobot();

coxa(60,60, mirror=false);