use <common.scad>

module edgeHoles(x=0, y=0, z=0, angle=0){
    height = 15;
    hole = 2.15; // 4.1 mm diameter
    dist = 6; // 6 mm center to center distance
    rotate([0,0,angle]){
        center = true;
        translate([x-6,y,z]){
            cylinder(height, 2, 2, center);
            translate([dist,0,0]){
                cylinder(height, 2, 2, center);
                translate([dist,0,0]){
                    cylinder(height, 2, 2, center);
                }
            }
//            translate([dist, dist, 0]) {
//                cylinder(height, 2, 2, center);
//            }
//            translate([dist, -dist, 0]) {
//                cylinder(height, 2, 2, center);
//            }
        }
    }
}

module main_plate(dia=65, hole=20){
    /*
    makes the base plate that the legs are mounted to
    */
    bar_th = 4;
    offset = 5;
    difference(){
        // build base plate
        union(){
            cylinder(2, d=dia, center=false);
            l = dia/2;
            w = 4;
            //rotate([0,0,45]) translate([-w/2,-l,0]) strut(l,w,10);
            //translate([0,0,bar_th/2]) rotate([0,0,45]) cube([dia,bar_th,bar_th], center=true);
            //translate([0,0,bar_th/2]) rotate([0,0,45]) cube([bar_th,dia,bar_th], center=true);
            // mount point or feet
            //mw = 10;
            //ml = 30;
            //dist = 20;
            //translate([-ml/2,-mw/4+dist,2]) cube([ml,mw/2,mw], center=false);
            //translate([-ml/2,-mw/4-dist,2]) cube([ml,mw/2,mw], center=false);
        }
        // cut out mount points
        translate([dia/2-offset,0,0]) edgeHoles(angle=90);
        translate([-dia/2+offset,0,0]) edgeHoles(angle=90);
        translate([0, dia/2-offset,0]) edgeHoles();
        translate([0, -dia/2+offset,0]) edgeHoles();
        // cut out center hole for wires
        cylinder(20, d=hole, center=true);
        // 4-40 holes
        rotate([0,0,45]) translate([dia/2-offset,0,0]) 4_40_hole();
        rotate([0,0,135]) translate([dia/2-offset,0,0]) 4_40_hole();
        rotate([0,0,225]) translate([dia/2-offset,0,0]) 4_40_hole();
        rotate([0,0,315]) translate([dia/2-offset,0,0]) 4_40_hole();
    }
}

main_plate();
