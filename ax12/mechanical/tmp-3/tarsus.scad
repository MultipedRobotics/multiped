use <../robotis_parts.scad>;

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

tarsus();
