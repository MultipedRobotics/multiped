use <robotis_parts.scad>;

module spar(L){
    linear_extrude(4){
        hull(){
            circle(d=1.25*40);
//            translate([2.25*40/3-3,0,0]) square(35, center=true);
            translate([2.25*40/3-3,0,0]) square(35, center=true);
        }
    }
}

/* module servo_mnt(){
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
} */

module base(D){
    servo = 35/2+2.25*40/2;
    h=4;
    difference(){
        spar_len = 30;
        difference(){
            union(){
                cylinder(h,d=.75*D);
                rotate([0,0,0]) translate([spar_len,0,0])  spar(D);
                rotate([0,0,90]) translate([spar_len,0,0]) spar(D);
                rotate([0,0,180]) translate([spar_len,0,0]) spar(D);
                rotate([0,0,270]) translate([spar_len,0,0]) spar(D);
            }
            translate([0,0,-1]) cylinder(20,d=20);  // cable hole
            rotate([0,0,0])  translate([servo/2,0,0]) servo_mnt();
            rotate([0,0,90])  translate([servo/2,0,0]) servo_mnt();
            rotate([0,0,180])  translate([servo/2,0,0]) servo_mnt();
            rotate([0,0,270])  translate([servo/2,0,0]) servo_mnt();
        }
		// shorten the spars
		rotate([0,0,0])  translate([servo-6,-60/2,-10]) cube([40,60,20], center=false);
		rotate([0,0,90])  translate([servo-6,-60/2,-10]) cube([40,60,20], center=false);
		rotate([0,0,180])  translate([servo-6,-60/2,-10]) cube([40,60,20], center=false);
		rotate([0,0,270])  translate([servo-6,-60/2,-10]) cube([40,60,20], center=false);
        // make layer thinner so M2x6 screws work
        rotate([0,0,0])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
        rotate([0,0,90])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
        rotate([0,0,180])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
        rotate([0,0,270])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    }
}

module top(){
	thick = 4;
    base(135);
    neck = 15;
    difference(){
        translate([0,0,neck/2+thick/2]) cylinder(neck, d2=30, d1=55, center=true);
        translate([0,0,neck/2+thick/2]) cylinder(2*neck,d=20, center=true);
    }
}

module bottom(){
    rotate([180,0,0])  translate([0,0,32]) base(135);

    // center grab point
    dia = 50;
    h = 15;
    translate([0,0,-32-h]) difference(){
        cylinder(h, d=dia);
        translate([dia/1.75,0,0]) cube([dia/2,dia, 2*h], center=true);
        translate([-dia/1.75,0,0]) cube([dia/2,dia, 2*h], center=true);
    }

    // corner stablizers
    sdia = 10;
    rotate([0,0,45]) translate([.75*135/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
    rotate([0,0,135]) translate([.75*135/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
    rotate([0,0,225]) translate([.75*135/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
    rotate([0,0,315]) translate([.75*135/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
}
