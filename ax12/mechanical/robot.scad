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

//module leg45(a1=0, a2=0){
//    translate([20,-15,15]) rotate([0,0,0]){
//        length=60;
//        femur(length, 45);
//        translate([0,0,-35]) coxa(length, 45);
//        translate([-3,20-4,-13]) rotate([0,0,90]) ax12();
//        translate([56,-7,-13]) rotate([0,0,270-45]) ax12();
//        rotate([90,0,-45]) translate([60+85/2*cos(a1),-15, -35-85/2*sin(a1)]) rotate([0,a1,0]){
//            tibia();
//            translate([43+15*cos(a2),-2.75,-15*sin(a2)]) rotate([0,-90,90]) rotate([0,0,-a2]) {
//                ax12();
//            
//                rotate([-90,0,0]) translate([0,4,-25]) rotate([90,0,0]) f3();
//                rotate([-90,0,0]) translate([0,4,-78]) rotate([0,0,90]) tarsus();
//            }
//        }
//    }
//}

module leg60(a1=0, a2=0){
    translate([18,-16.5,15]) {
        length=60;
        // 60 degrees
        femur(length, 60);
        translate([0,0,-35]) femur(length, 60);
        translate([-3,20-4,-13]) rotate([0,0,90]) ax12();
        translate([51,-13,-13]) rotate([0,0,270-60]) ax12();
//        rotate([90,0,-60]) translate([53+(89/2)*cos(a1)+27*sin(a1),-15, -38-(27+89/2)*sin(a1)+27*cos(a1)]) rotate([0,a1,0]) {
        rotate([90,0,-60]) translate([53+(89/2)*cos(a1)+27*sin(a1),-15, -18-(27+89/2)*sin(a1)+37*cos(a1)]) rotate([0,a1,0]) {
            rotate([180,0,0]) tibia();
            translate([43+15*cos(a2),-2.75,-15*sin(a2)]) rotate([0,-90,90]) rotate([0,0,-a2]) {
                ax12();
            
                rotate([-90,0,0]) translate([0,4,-25]) rotate([90,0,0]) f3();
                rotate([-90,0,0]) translate([0,4,-78]) rotate([0,0,90]) tarsus();
            }
        }
    }
}

module leg(femur_angle, tibia_angle, tarsus_angle){
    rotate([-90,0,0]) coxa();
    rotate([-90,-femur_angle,0]) leg60(tibia_angle,tarsus_angle);
}


//leg(10,140,20);  // stand
//leg(100,180,70);  // stow
//leg(100,170,85);
//leg(10,140,20);


// stand: 10, 100, 55
// stow: 100 180 70

module fullrobot(femur_angle, tibia_angle, tarsus_angle){
    translate([120,0,-20]) leg(femur_angle,tibia_angle,tarsus_angle);
    
    rotate([0,0,90])translate([120,0,-20])leg(femur_angle,tibia_angle,tarsus_angle);
        
    rotate([0,0,180])translate([120,0,-20])leg(femur_angle,tibia_angle,tarsus_angle);
        
    rotate([0,0,270])translate([120,0,-20])leg(femur_angle,tibia_angle,tarsus_angle);
    
    color("SkyBlue") top();
    color("gray") translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
    color("gray") rotate([0,0,90]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
    color("gray") rotate([0,0,180]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
    color("gray") rotate([0,0,270]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12(); 
    
//    translate([0,0,20]){
//        color("SkyBlue") rotate([0,0,45]) translate([0,0,4]) rpi_base(); 
//        color("ForestGreen") rotate([0,0,45]) translate([11,0,10]) rpi3();
//    }
    
    color("SkyBlue") bottom();
}

//fullrobot(10,140,20);  // stand
fullrobot(100,180,70);  // stow

//translate([0,0,20]) cylinder(d=80,h=110); // head?
