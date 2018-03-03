use <common.scad>
use <pulley.scad>
use <u_frame.scad>
use <base_plate.scad>
use <top_plate.scad>
use <head.scad>
use <face_plate.scad>
$fn=45;

include <pi-zero/files/PiZero_1.2.scad>;

module amp(){
    color("Gray")
    cube([19.4,17.8, 3]);
}

module imu(){
    color("Gray")
    cube([28.3, 20.5, 3]);
}

module board(){
    union(){
        color("Green", 1)
        difference(){
            hull(){
                translate([-PiHoleX,-PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
                translate([PiHoleX,-PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
                translate([PiHoleX,PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
                translate([-PiHoleX,PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
            }
            PiPCBhole(-PiHoleX,-PiHoleY);
            PiPCBhole(PiHoleX,-PiHoleY);
            PiPCBhole(PiHoleX,PiHoleY);
            PiPCBhole(-PiHoleX,PiHoleY);
        }
//        translate([-3,-10,-3]) imu();
//        translate([-25,-10,-3]) amp();
    }
}


module lcd(){
    union(){
        //color("DarkGreen", 1)
        color("DarkSlateGray")
        difference(){
            hull(){
                translate([-PiHoleX,-PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
                translate([PiHoleX,-PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
                translate([PiHoleX,PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
                translate([-PiHoleX,PiHoleY,PiSizeZ/2])
                    cylinder(r=PiCornerRad,h=PiSizeZ,center=true);
            }
            PiPCBhole(PiHoleX,PiHoleY);
            PiPCBhole(-PiHoleX,PiHoleY);
        }
        wleds = 22;
        lleds = 55;
        hleds = 0.5;
        color("White")
        translate([-lleds/2,-wleds/2-7/2,1.5]) cube([lleds,wleds,hleds], center=false);
    }
}
    

module head(){
    // washer offset
    translate([0,0,3]) PiZeroBody();
    // header height + board thickness
    translate([0,0,9+2]) lcd();
}

/*
color("SkyBlue", 1) {
    //pulley();
	//u_frame(25);
    //main_plate();
    //base_plate();
    //top_plate();
    //neck();
    translate([0,0,10]) PiZeroBody();
}*/

//PiZeroBody();

//module hindge(dia){
//    difference(){
//        cylinder(dia,d=6,center=true);
//        translate([0,0,0]) cylinder(5,d=7,center=true);
//        translate([0,0,12]) cylinder(5,d=7,center=true);
//        translate([0,0,-12]) cylinder(5,d=7,center=true);
//        cylinder(dia+2,d=3,center=true);
//    }
//}

//module Base(dia=40){
//    union(){
//        difference(){
//            cube([dia,dia,10], center=true);
//            cylinder(20,d=20,center=true);
//            translate([0,dia/2-3,5])
//            rotate([0,90,0])
//            cylinder(dia+2,d=3,center=true);
//            
//            translate([0,-(dia/2-3),5])
//            rotate([0,90,0])
//            cylinder(dia+2,d=3,center=true);
//        }
//        translate([0,(dia/2-3),5]) rotate([0,90,0]) hindge(dia);
//        translate([0,-(dia/2-3),5]) rotate([0,90,0]) hindge(dia);
//    }
//}

//module Base(dia=40, h=10){
//    translate([0,0,0]) union(){
//        // pi zero mounting holes
//        rotate([0, 90, 0]) translate([-65/2-20-5,0,0]) board();
//        // circular base
//        difference(){
//            cylinder(h,d=dia, center=false); // hub
//            cylinder(2*h,d=20,center=false); // wire pass through
//            translate([0,0,-1]) cylinder(h/2+1,d=3*20/2,center=false); // inner rim
//        }
//        // support pilar - left
//        translate([0,15,h/2]) rotate([0,0,-90]) difference(){
//            cylinder(40,d=10);
//            translate([-2,1,19]) cube([15,5,25]);
//        }
//        // support pilar - right
//        translate([0,-15,h/2]) difference(){
//            cylinder(40,d=10);
//            translate([1,-2,19]) cube([5,15,25]);
//        }
//    }
//}
//rotate([0, 90, 0]) translate([-65/2-20-5,0,3]) rotate([0, 0, 180]) head();
//HeadMount();
//top_plate();
