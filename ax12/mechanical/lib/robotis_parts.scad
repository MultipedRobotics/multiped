use <misc.scad>;

///////////////////////
// These are STL models I found on line
///////////////////////

module ax12(){
    // sort of center mass
    color("dimgray") translate([-70,-210,-180]) import("parts/AX-12A.STL");
}


module f2(){
    // U bracket
    // sort of center mass
    color("lightgray") translate([0,0,0]) import("parts/F2.stl");
}

module f3(){
    // End cap bracket
    // sort of center mass
    color("lightgray") translate([0,0,0]) import("parts/F3.stl");
}

/////////////////////
// These are some interfaces I made for the parts
////////////////////

module pulleyHole(){
    cylinder(20, d=8.5, center=true);  // hub
    translate([0,0,3]) cylinder(20, d=11);  // 3mm?
}

module holes(t){
    // M3 3.3 mm
    M3(t);

    // M2 2.3 mm
    /* dia = 2.3; */
    translate([8,0,0]) M2(t);
    translate([-8,0,0]) M2(t);
    translate([0,8,0]) M2(t);
    translate([0,-8,0]) M2(t);
}

// does anything use this?????
/* module pulley(dia=24, thick=3, cen=false){
    cylinder(thick,d=dia,center=cen);
} */

module servo_mnt(){
    d = 2.5;
    w = 22; // center servo
    l = 35; // center servo
    s = 38.5-2.5;
    h=20;

    translate([32,-20,-1]) cube([20,40,h],center=false);
    translate([2.5,-w/2,-1])cube([l,w,h],center=false);

    // bottom holes
    translate([0,8,-1]) cylinder(h,d=d);
    translate([0,-8,-1]) cylinder(h,d=d);

    // right holes
    translate([5.5,-27/2,-1]) cylinder(h,d=d);
    translate([5.5+8,-27/2,-1]) cylinder(h,d=d);
    translate([5.5+16,-27/2,-1]) cylinder(h,d=d);
    translate([5.5+24,-27/2,-1]) cylinder(h,d=d);

    // left holes
    translate([5.5,27/2,-1]) cylinder(h,d=d);
    translate([5.5+8,27/2,-1]) cylinder(h,d=d);
    translate([5.5+16,27/2,-1]) cylinder(h,d=d);
    translate([5.5+24,27/2,-1]) cylinder(h,d=d);
}
