
//module bar(length){
//    width = 20;
//    height = 2;
//    translate([0, width/2,0]) {
//        cylinder(height, width/2, width/2, false);
//    }
//    //translate([width/2,0,0]){
//        cube([length-width,width,height], false);
//        translate([length-width, width/2, 0]){
//            cylinder(height, width/2, width/2, false);
//        }
//}


//module bar2(length){
//    /*
//    This creates a bar that looks like a popsicle stick.
//    */
//    hull(){
//        translate([0,length,0]) cylinder(2,10,10,false);
//        cylinder(2,10,10,false);
//    }
//}


//module femur_horn2horn(length){
//    difference(){
//        bar2(length);
//        hornHoles(0,0,0, 0);
//        hornHoles(0,length,0, 0);
//    }
//}
//
//module femur_side2side(length){
//    union(){
//        difference(){
//            bar2(length);
//            hornHoles(0,0,0, 0);
//            hornHoles(0,length,0, 0);
//        }
//        translate([0,0,3.5]) pulley();
//        translate([0,length,3.5]) pulley();
//    }
//}
//
//module sidePlate(length=18){
//    difference(){
//        bar2(length);
//        bodyHoles(0,0,0);
//    }
//}

//module foot(length){
//    base = 7.5;
//    end = 2.5;
//    color("CornflowerBlue", 1) {
//        cylinder(length, 7.5, 2.5, false);
//        translate([0,0,length]) sphere(end);
//    }
//}
//
//module foot2(length){
//    translate([0,6,0]) rib(-1, length);
//    translate([0,-6,0]) rib(1, length);
//    translate([length-2,0,0]) cylinder(5,2,2);
//}

//module foot3(length){
//    difference(){
//        union(){
//    translate([0,-34/2,0]) cube([20, 34, 2], false);
//    linear_extrude(height=4, center=false)
//        polygon([[0,-6],[length,-2],[length,2],[0,6]]);
//    translate([length,0,2]) sphere(2);
//        }
////    translate([9,-9,0]) bodyHoles();
//        translate([10,-12,0]){
//            bottomHoles();
//            bottomHoles(0,24,0);
//        }
//    }
//}

module coxa(){
    cube([1,1,1], true);
}

module rib(side, length){
    angle = side*atan2(4,length);
    echo(angle);
    rotate([90,0,angle]){
        linear_extrude(height=2, center=true) polygon([[0,0],[length,0],[length,4],[0,4]]);
    }
}

//module lplate(){
//    // facing the wrong way!
//    sidePlate(33-9);
//    translate([0,33-9,5]) {
//        difference(){
//            cube([20,2,10], true);
//            rotate([90,0,0]) bottomHoles();
//        }
//    }
//}


module tibia(length=50){
    lplate();
}
