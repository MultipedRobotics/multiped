use <common.scad>
//$fn=45;

include <pi-zero/files/PiZero_1.2.scad>;


module face(){
    // PiSizeZ = 1.5;
    PiSizeZ = 1;
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
        // Corner screw holes
        PiPCBhole(-PiHoleX,-PiHoleY);
        PiPCBhole(PiHoleX,-PiHoleY);
        PiPCBhole(PiHoleX,PiHoleY);
        PiPCBhole(-PiHoleX,PiHoleY);
    }
}

face();