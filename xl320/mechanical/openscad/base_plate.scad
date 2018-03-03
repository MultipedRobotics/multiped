use <main_plate.scad>
use <common.scad>

module base_plate(dia=65){
    union(){
        main_plate(dia);
        union(){
            difference(){
                cylinder(10, d=dia/2, center=false);
                mw = 10;
                ml = 30;
                dist = 15;
                translate([-ml/2,-mw/2+dist,2]) cube([ml,mw,mw], center=false);
                translate([-ml/2,-mw/2-dist,2]) cube([ml,mw,mw], center=false);
            }
            offset = dia/2-5;
            rotate([0,0,45]) translate([offset,0,0]) cylinder(10, d=10, center=false);
            rotate([0,0,45]) translate([-offset,0,0]) cylinder(10, d=10, center=false);
            rotate([0,0,45]) translate([0,offset,0]) cylinder(10, d=10, center=false);
            rotate([0,0,45]) translate([0,-offset,0]) cylinder(10, d=10, center=false);
        }
    }
}

base_plate();
