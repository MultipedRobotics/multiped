$fn = 90;

// library folder
use <lib/robotis_parts.scad>;
use <lib/misc.scad>;
use <lib/pi.scad>;
use <lib/lidar.scad>;

// this folder
use <tibia.scad>;
use <femur.scad>;
use <tarsus.scad>;
use <coxa.scad>;
//use <head.scad>;
use <sternum-2.scad>;
use <power.scad>;

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

module leg60(a1=0, a2=0,COLOR1,COLOR2){
    translate([18,-16.5,15]) {
        length=60;
        // 60 degrees
        color(COLOR2) femur(length, 60);
        translate([0,0,-35]) color(COLOR2) femur(length, 60);

        translate([-3,20-4,-13]) rotate([0,0,90]) ax12();
        translate([51,-13,-13]) rotate([0,0,270-60]) ax12();
//        rotate([90,0,-60]) translate([53+(89/2)*cos(a1)+27*sin(a1),-15, -38-(27+89/2)*sin(a1)+27*cos(a1)]) rotate([0,a1,0]) {
        rotate([90,0,-60]) translate([53+(89/2)*cos(a1)+27*sin(a1),-15, -18-(27+89/2)*sin(a1)+37*cos(a1)]) rotate([0,a1,0]) {
            rotate([180,0,0]) color(COLOR1) tibia();
            translate([43+15*cos(a2),-2.75,-15*sin(a2)]) rotate([0,-90,90]) rotate([0,0,-a2]) {
                ax12();

                rotate([-90,0,0]) translate([0,4,-25]) rotate([90,0,0]) f3();
                rotate([-90,0,0]) translate([0,4,-78]) rotate([0,0,90]) color(COLOR2) tarsus();
            }
        }
    }
}

module leg(femur_angle, tibia_angle, tarsus_angle,COLOR1,COLOR2){
    rotate([-90,0,0]) coxa();  // standard robotis parts
    rotate([-90,-femur_angle,0]) leg60(tibia_angle,tarsus_angle,COLOR1,COLOR2);
}

module piFootPrint(depth=10){
    hole = 2.8; // mm
    dx = 58;
    dy = 49;
    translate([-dx/2,-dy/2,0]){
        /* cylinder(h=depth, d=hole, center=true);
        translate([dx,0,0]) cylinder(h=depth, d=hole, center=true);
        translate([0,dy,0]) cylinder(h=depth, d=hole, center=true);
        translate([dx,dy,0]) cylinder(h=depth, d=hole, center=true); */
        M2(20);
        translate([dx,0,0]) M2(20);
        translate([0,dy,0]) M2(20);
        translate([dx,dy,0]) M2(20);
    }
}

module M2standoff(x,y,z,h){
    dia = 2.5;
    wide = 3;

    translate([x,y,z]) difference(){
        cylinder(h=h, d=dia+wide);
        cylinder(h=4*h, d=dia, center=true);
    }
}

module cameramount(thick){
    offset = 15;
    translate([0,-3,0]){  // move to avoid screw holes
    // connects to base plate
    difference(){
        translate([-49/2,0,0]) cube([49, 15, thick]);
        translate([-25/2,-1,-1]) cube([25, 20, 2*thick]); // screw cutout
    }
    // camera mount back
    difference(){
        translate([-49/2,0,0])cube([49, 3, 30+offset]);
        translate([-49/2+3,-1,3+offset]) cube([4, 10, 4]);
        translate([-49/2+3,-1,3+offset+20]) cube([4, 10, 4]);
        translate([49/2-7,-1,3+offset]) cube([4, 10, 4]);
        translate([49/2-7,-1,3+offset+20]) cube([4, 10, 4]);
        translate([-25/2,-1,-1])cube([25, 10, 25]);  // cable/sd card cutout
    }
    // curved edges
    difference(){
        translate([-49/2,0,4]) cube([49, 8, 5]);
        translate([-49/2-1,5+3,4+5]) rotate([0,90,0]) cylinder(h=55, d=10);
        translate([-25/2,-1,-1]) cube([25, 20, 40]); // screw cutout
    }
}
}

module rpi_base(){
    difference(){
        // main deck
        cylinder(h=4, d=100);

        // cable cutouts
        cube([70,20,20], center=true);
        translate([0,-10,0]) cylinder(h=10, d=50, center=true);
        translate([0,10,0]) cylinder(h=20, d=40, center=true);

        // alt imu mount point
        rotate([0,180,0]) translate([0,0,-4]){
            y = 5;
            translate([38, 23+y, 0]) M2(20);
            translate([38, y, 0]) M2(20);
        }

        // screws to bottom (legs)
        translate([50-5/2-1, 0, 0]) M3(20);
        translate([-50+5/2+1, 0, 0]) M3(20);
        translate([0, 50-5/2-1, 0]) M3(20);
        translate([0, -50+5/2+1, 0]) M3(20);

        // screws to top (lidar)
        rotate([0,180,45]) translate([0,0,-4]){
            rotate([0,0,20]) translate([50-5/2-1, 0, 0]) M3(20);
            translate([-50+5/2+1, 0, 0]) M3(20);
            translate([0, 50-5/2-1, 0]) M3(20);
            rotate([0,0,-20]) translate([0, -50+5/2+1, 0]) M3(20);
        }

        rotate([0,180,90]) translate([10,0,-4]) piFootPrint();
    }

    // imu standoffs
    height = 4;  // height above plate
    y = 5;
    M2standoff(-38,23+y,4,height);
    M2standoff(-38,y,4,height);

    // pi standoffs
    dx = 58;
    dy = 49;
    height = 4;  // height above plate
    rotate([0,0,90]) translate([-dx/2,-dy/2,0]) {
        M2standoff(dx-10,0,4,height);
        M2standoff(-10,0,4,height);
        M2standoff(dx-10,dy,4,height);
        M2standoff(-10,dy,4,height);
    }

    translate([0,-55,0]) cameramount(4);
}

module lidar_base(){
    dia = 100;
    difference(){
        cylinder(h=4, d=100);
        cylinder(h=10, d=40, center=true);

        // screws to rpi deck
        m3d = 6;
        translate([50-5/2-1, 0, 0]) M3Nut(20); //cylinder(h=19,d=m3d, center=true);
        rotate([0,0,-20]) translate([-50+5/2+1, 0, 0]) M3Nut(20);
        translate([0, 50-5/2-1, 0]) M3Nut(20);
        rotate([0,0,20]) translate([0, -50+5/2+1, 0]) M3Nut(20);
//}{
        // ydlidar/lds-01 lidar mount
        rotate([0,180,45]) translate([3,0,-4]){
            translate([22,31,0]) M3(20);
            translate([22,-31,0]) M3(20);
            translate([-35,25,0]) M3(20);
            translate([-35,-25,0]) M3(20);
        }

        // rpylidar - tbd

        // hokuyo urg mount
        rotate([0,180,45]) translate([0,0,-4]){
            translate([20,20,0]) M3(20);
            translate([20,-20,0]) M3(20);
            translate([-20,20,0]) M3(20);
            translate([-20,-20,0]) M3(20);
        }

        // skeletonizing
        translate([dia/3+4, dia/3+4, -2]) rotate([0,0,-45]) scale([1.2,.85,1]) cylinder(h=10, d=50); // back
        translate([-dia/4-5, dia/2.5, -2]) rotate([0,0,35]) scale([.90,.75,1]) cylinder(h=10, d=50); // right
        //translate([dia/3, -dia/3, -2]) rotate([0,0,45]) scale([1,.5,1]) cylinder(h=10, d=50);
        translate([dia/2.5, -dia/4-5, -2]) rotate([0,0,35]) scale([.90,.75,1]) cylinder(h=10, d=50); // left
        translate([-dia/3, -dia/3, -2]) rotate([0,0,-45]) scale([1.75,.70,1]) cylinder(h=10, d=50); // front
    }
}


//leg(10,140,20);  // stand
//leg(100,180,70);  // stow
//leg(100,170,85);
//leg(10,140,20);

/* module upper(){
    translate([0,26,4+4]) power_board();
    translate([0,-26,4+4]) rotate([0,0,180]) power_board();

    color("silver") translate([50-5/2-1, 0, 4]) cylinder(h=19,d=5);
    color("silver") translate([-50+5/2+1, 0, 4]) cylinder(h=19,d=5);
    color("silver") translate([0, 50-5/2-1, 4]) cylinder(h=19,d=5);
    color("silver") translate([0, -50+5/2+1, 4]) cylinder(h=19,d=5);

    translate([0,0,4+19]) {  // top: 4mm  stand off: 19 mm
        rotate([0,0,90]) translate([0,0,4+19]) rpi3();
        color("red") rpi_base();
    }
} */


// stand: 10, 100, 55
// stow: 100 180 70

module fullrobot(femur_angle, tibia_angle, tarsus_angle){
    length = 140;
    width = 100;

    // COLOR1 = "skyblue";
    COLOR1 = "red";
    COLOR2 = "silver";

    color(COLOR1) top2(length, width);
    translate([0,30,10]) power_board();
    translate([0,-30,10]) rotate([0,0,180]) power_board();

    translate([0,0,25]) {
        color(COLOR1) rpi_base();
        translate([0,-60,20]) rotate([90,0,0]) picamera();
        rotate([0,0,90]) translate([2,0,6]) rpi3();
        translate([0,0,30]) rotate([0,0,45]) color(COLOR1) lidar_base();
        translate([0,0,34]) rotate([0,0,-90]) rplidar();
    }

    // Legs
    offset = 31;  // distance from 45 deg mid-line
    shift = length/2 - sqrt(50*50+50*50)*cos(45);
    translate([shift,0,0]) rotate([0,0,45]) translate([offset,0,0]) translate([21,0,-12]) rotate([0,0,-90]){
        ax12();
        rotate([0,0,90]) translate([70,0,-7]) leg(femur_angle,tibia_angle,tarsus_angle,COLOR1,COLOR2);
    }
    translate([-shift,0,0]) rotate([0,0,135]) translate([offset,0,0]) translate([21,0,-12]) rotate([0,0,-90]){
        ax12();
        rotate([0,0,90]) translate([70,0,-7]) leg(femur_angle,tibia_angle,tarsus_angle,COLOR1,COLOR2);
    }
    translate([-shift,0,0]) rotate([0,0,225]) translate([offset,0,0]) translate([21,0,-12]) rotate([0,0,-90]){
        color(COLOR2) ax12();
        rotate([0,0,90]) translate([70,0,-7]) leg(femur_angle,tibia_angle,tarsus_angle,COLOR1,COLOR2);
    }
    translate([shift,0,0]) rotate([0,0,315]) translate([offset,0,0]) translate([21,0,-12]) rotate([0,0,-90]){
        ax12();
        rotate([0,0,90]) translate([70,0,-7]) leg(femur_angle,tibia_angle,tarsus_angle,COLOR1,COLOR2);
    }

    color(COLOR1) bottom2(length,width);
}

//COLOR1 = "lime";

//fullrobot(10,140,20);  // stand
//fullrobot(100,160,90);  // stow
//bottom2(140,100);

//top2(140,100);
//rotate([0,0,90]) translate([2,0,6]) rpi3();
//translate([0,0,0]) color(COLOR1) rpi_base();
//translate([0,0,30]) rotate([0,0,45]) color(COLOR1) lidar_base();
//translate([0,0,34]) rotate([0,0,-90]) rplidar();
//translate([0,0,20]) cylinder(d=80,h=110); // head?

//top2(125, 100);
//upper();
//rpi_base();
lidar_base();
