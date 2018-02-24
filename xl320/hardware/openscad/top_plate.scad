use <common.scad>
use <main_plate.scad>

module neck(outer=40, inner=25, len=70){
    difference(){
        union(){
            ch = outer/3;
            cylinder(ch,r1=outer/2, r2=inner/2, center=false);
            translate([0,0,len-ch]) cylinder(ch,r1=inner/2, r2=outer/2, center=false);
            translate([0,0,len]) cylinder(4,d=29, center=false);
            cylinder(len, d=inner, center=false);
        }
        cylinder(len*5, d=20, center=true);
    }
}

module top_plate(dia=65){
    union(){
        main_plate(dia);
        neck();
        /*
        difference(){
            cylinder(10, d=dia/2, center=false);
            cylinder(200, d=dia/4, center=true);
        }
        */
    }

}

top_plate();
