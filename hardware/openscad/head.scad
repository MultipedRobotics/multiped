include <pi-zero/files/PiZero_1.2.scad>;

module PCBhole(Xpos,Ypos,depth)   // Cuts a hole through PCB
{
	PiHoleDia = 3.0;
	translate([Xpos,Ypos,depth/2])
	    cylinder(h=2*depth,d=PiHoleDia,center=true);
}

module backboard(){
    union(){
        /* color("Green", 1) */
		thickness = 4;
        difference(){
            hull(){
                translate([-PiHoleX,-PiHoleY,thickness/2])
                    cylinder(r=PiCornerRad,h=thickness,center=true);
                translate([PiHoleX,-PiHoleY,thickness/2])
                    cylinder(r=PiCornerRad,h=thickness,center=true);
                translate([PiHoleX,PiHoleY,thickness/2])
                    cylinder(r=PiCornerRad,h=thickness,center=true);
                translate([-PiHoleX,PiHoleY,thickness/2])
                    cylinder(r=PiCornerRad,h=thickness,center=true);
            }
            PCBhole(-PiHoleX,-PiHoleY,thickness);
            /* PCBhole(PiHoleX,-PiHoleY,thickness); */
            /* PCBhole(PiHoleX,PiHoleY,thickness); */
            PCBhole(-PiHoleX,PiHoleY,thickness);
        }
//        translate([-3,-10,-3]) imu();
//        translate([-25,-10,-3]) amp();
    }
}

module HeadMount(dia=40, h=10){
    translate([0,0,0]) union(){
        // pi zero mounting holes
        rotate([0, 90, 0])  translate([-65/2-20-5,0,1]) backboard();
        // circular base
        difference(){
            cylinder(h,d=dia, center=false); // hub
            cylinder(2*h,d=20,center=false); // wire pass through
            translate([0,0,-1]) cylinder(h/2+1,d=3*20/2,center=false); // inner rim
        }
        // support pilar - left
        translate([0,15,h/2]) rotate([0,0,-90]) difference(){
            cylinder(40,d=10);
            /* translate([-2,1,19]) cube([15,5,25]); */
            /* PCBhole(PiHoleX,PiHoleY,70); */
			/* rotate([90,0,0]) translate([-2.5,12,h/2]) PCBhole(PiHoleX,PiHoleY,70); */
        }
		/* translate([0,15,h/2]) rotate([0,0,-90]) rotate([90,0,0]) translate([-2.5,12,h/2]) PCBhole(PiHoleX,PiHoleY,70); */
        // support pilar - right
        translate([0,-15,h/2]) difference(){
            cylinder(40,d=10);
            /* translate([1,-2,19]) cube([5,15,25]); */
			/* rotate([0,0,90]) rotate([90,0,0]) translate([-2.5,12,h/2]) PCBhole(PiHoleX,PiHoleY,70); */
        }
		/* translate([0,-15,h/2]) rotate([0,0,90]) rotate([90,0,0]) translate([-2.5,12,h/2]) PCBhole(PiHoleX,PiHoleY,70); */
    }
}

HeadMount();
