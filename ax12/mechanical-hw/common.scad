
// These are STL models I found on line

module ax12(){
    // sort of center mass
    translate([-70,-210,-180]) import("parts/AX-12A.STL");
}

module rpi3(){
    // sort of center mass
    translate([-3-88.5/2,-2-56/2,0]) import("parts/rpi3.STL");
}

module f2(){
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
}
