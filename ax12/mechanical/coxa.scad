
use <lib/robotis_parts.scad>;

///////////////////////
// Coxa
///////////////////////
// This is just 2 standard robotis parts
//

module coxa(){
    color("lightgray") rotate([0,0,-90]) f2();
    color("lightgray") translate([-53,-5,0]) rotate([90,-90,0]) f2();
}
