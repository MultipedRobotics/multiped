use <lib/robotis_parts.scad>;

//$fn=100;

module tarsus(L=50){
    // if too small, it doesn't work right
    L = L <= 40 ? 40 : L;
    color("SkyBlue") difference(){

        union(){
            translate([0,0,L+3/2]) cube([35,25,3], center=true);
            translate([0,0,5]) cylinder(h=L-5,d=12);  // shaft
            translate([0,0,L-20]) cylinder(h=20,d1=0,d2=24); // base
            cylinder(h=5,d1=0,d2=12);  // point
        }
        translate([0,0,L+3/2]) rotate([180,0,0]) holes(10);
    }
}

//tarsus(10);
