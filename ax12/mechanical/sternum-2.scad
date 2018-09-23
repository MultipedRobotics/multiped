//use <lib/robotis_parts.scad>;
use <power.scad>;
use <lib/misc.scad>;
use <base.scad>;

//$fn=100;

module spar(L){
    linear_extrude(4){
        hull(){
            circle(d=1.25*40);
//            translate([2.25*40/3-3,0,0]) square(35, center=true);
            translate([2.25*40/3-3,0,0]) square(35, center=true);
        }
    }
}

module servo_mnt(){
    d = 2.5;
    w = 22; // center servo
    l = 35; // center servo
    s = 38.5-2.5;
    h=20;

    translate([32,-20,-1]) cube([20,40,h],center=false);
    translate([2.5,-w/2,-1]) cube([l,w,h],center=false);

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

    // make layer thinner so M2x6 screws work
    translate([-2.5,-32/2,2]) cube([40,32,5], center=false);

    // make shorter - x: 25 mm should give 3 holes
    translate([25,-60/2,-10]) cube([40,60,20], center=false);
}

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

module spar2(){
    // make an unnecessarily fancy shape that mostly gets removed ... replace with simplier solution?
    linear_extrude(4){
        hull(){
            circle(d=1.25*40);
            translate([27,0,0]) square(35, center=true);
        }
    }
}


module base_wide2(L, W){
    servo = 35/2+2.25*40/2;
    h=4;
    angle = atan2(W/2,L/2);
    echo("angle",angle);
    difference()
    {
//        spar_len = 50;  // 50
        spar_len = 30;
        offset = 31;  // distance from 45 deg mid-line
        shift = L/2 - sqrt(50*50+50*50)*cos(45);
        echo("shift", shift);
//        shift = 0;
        union(){
            translate([-L/2,-W/2,0]) cube([L,W,h], center=false);
            translate([shift,0,0]) rotate([0,0,45]) translate([spar_len,0,0]) spar2();
            translate([-shift,0,0]) rotate([0,0,135]) translate([spar_len,0,0]) spar2();
            translate([-shift,0,0]) rotate([0,0,225]) translate([spar_len,0,0]) spar2();
            translate([shift,0,0]) rotate([0,0,315]) translate([spar_len,0,0]) spar2();

            // push button
            // translate([32,0,0]) cylinder(10,d=19, center=false);
        }
        // translate([0,0,-1]) cylinder(20,d=20);  // cable hole
        cube([40,20,60], center=true);  // cable hole

        // push button
        // translate([32,0,0]) cylinder(40,d=16.5, center=true);

        translate([shift,0,0]) rotate([0,0,45]) translate([offset,0,0]) servo_mnt();
        translate([-shift,0,0]) rotate([0,0,135]) translate([offset,0,0]) servo_mnt();
        translate([-shift,0,0]) rotate([0,0,225]) translate([offset,0,0]) servo_mnt();
        translate([shift,0,0]) rotate([0,0,315]) translate([offset,0,0]) servo_mnt();

    }
}

/* module M2standoff(x,y,z,h){
    dia = 2.5;
    wide = 3;

    translate([x,y,z]) difference(){
        cylinder(h=h, d=dia+wide);
        cylinder(h=4*h, d=dia, center=true);
    }
} */

module top2(l,w){
    difference(){
        union(){
            base_wide2(l, w);
            translate([0,26,0]) powerStandoff(8);
            translate([0,-26,0]) rotate([0,0,180]) powerStandoff(8);
        }

        // stand-offs
        m3 = 3.1;
        translate([50-5/2-1, 0, 4]) cylinder(h=19,d=m3, center=true);
        translate([-50+5/2+1, 0, 4]) cylinder(h=19,d=m3, center=true);
        translate([0, 50-5/2-1, 4]) cylinder(h=19,d=m3, center=true);
        translate([0, -50+5/2+1, 4]) cylinder(h=19,d=m3, center=true);

        // pan head counter sinks
        m3d = 6;
        m3h = 2.5;
        translate([50-5/2-1, 0, -0.5]) cylinder(h=m3h,d=m3d, center=false);
        translate([-50+5/2+1, 0, -0.5]) cylinder(h=m3h,d=m3d, center=false);
        translate([0, 50-5/2-1, -0.5]) cylinder(h=m3h,d=m3d, center=false);
        translate([0, -50+5/2+1, -0.5]) cylinder(h=m3h,d=m3d, center=false);

        translate([0,26,0]) powerFootPrint();
        translate([0,-26,0]) rotate([0,0,180]) powerFootPrint();
    }

//    thick = 4;
//    neck = 15;
//    difference(){
//        translate([0,0,neck/2+thick/2]) cylinder(neck, d2=30, d1=2*w/3, center=true);
//        translate([0,0,neck/2+thick/2]) cylinder(2*neck,d=20, center=true);
//    }
}

/* module interface(h, dia){
    difference(){
        cylinder(h=h,d=dia);
        translate([0,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
    }
} */

module bottom2(l,w){

    difference(){
        rotate([180,0,0])  translate([0,0,32]) base_wide2(l, w);

        // cable holes
        translate([20,w/2-10,-32]) cube([15,8,10], center=true);
        translate([-20,w/2-10,-32]) cube([15,8,10], center=true);
        translate([20,-w/2+10,-32]) cube([15,8,10], center=true);
        translate([-20,-w/2+10,-32]) cube([15,8,10], center=true);

        hbolt = 100;
        translate([22,22,-32])   M3(hbolt);
        translate([-22,22,-32])  M3(hbolt);
        translate([22,-22,-32])  M3(hbolt);
        translate([-22,-22,-32]) M3(hbolt);
    }

    // center grab point
    dia = 18;
    h = 15;
//    translate([0,0,-32-h]) difference(){
//        cylinder(h, d=dia);
//        rotate([0,0,90]) translate([dia/2+15,0,0]) cube([dia,dia, 2*h], center=true);
//        rotate([0,0,90]) translate([-dia/2-15,0,0]) cube([dia,dia, 2*h], center=true);
//    }
    translate([0,0,-32-h-4]) {
        difference()
        {
            union(){
                translate([l/2-dia,0,0]) cylinder(h=h,d=dia); //interface(h,dia);
                translate([-l/2+dia,0,0]) cylinder(h=h,d=dia); //interface(h,dia);
                translate([0,w/2-dia,0]) cylinder(h=h,d=dia); //interface(h,dia);
                translate([0,-w/2+dia,0]) cylinder(h=h,d=dia); //interface(h,dia);

                cylinder(h=h, d=40);

                translate([-dia/4, -w/2+dia,0]) cube([dia/2,w-2*dia,h]);
                translate([-l/2+dia,-dia/4,0]) cube([l-2*dia,dia/2,h]);
            }
            translate([l/2-dia,0,0]) translate([0,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([-l/2+dia,0,0]) translate([0,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([0,w/2-dia,0]) translate([0,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([0,-w/2+dia,0]) translate([0,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([0,0,-1]) cylinder(h=h, d2=0, d1=40-1);

        }
    }
    // corner stablizers
//    sdia = 10;
//    rotate([0,0,0]) translate([l/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
//    rotate([0,0,90]) translate([w/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
//    rotate([0,0,180]) translate([l/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
//    rotate([0,0,270]) translate([w/2-sdia/2,0,-32-h]) cylinder(h, d=sdia);
}

/* module robot_stand(height){
    union(){
        l = 140;
        w = 100;
        dia = 18-1;
        h = 15-0.5;
        thick = 4;

        // spikes
        translate([0,0,thick+height]){
            translate([l/2-dia,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([-l/2+dia,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([0,w/2-dia,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([0,-w/2+dia,-1]) cylinder(h=h,d2=0, d1=dia-1);
            translate([0,0,-1]) cylinder(h=h, d2=0, d1=40-1);
        }

        // pillar supports
        translate([0,0,thick]){
            translate([l/2-dia,0,-1]) cylinder(h=height,d=dia-1);
            translate([-l/2+dia,0,-1]) cylinder(h=height,d=dia-1);
            translate([0,w/2-dia,-1]) cylinder(h=height,d=dia-1);
            translate([0,-w/2+dia,-1]) cylinder(h=height,d=dia-1);
            translate([0,0,-1]) cylinder(h=height, d=40-1);


            translate([-dia/8, -w/2+dia,0]) cube([dia/4,w-2*dia,height-10]);
            translate([-l/2+dia,-dia/8,0]) cube([l-2*dia,dia/4,height-10]);
        }
        translate([-l/2,-w/2,0]) cube([l,w,thick]);
    }
} */

/* robot_stand(70); */

//translate([150,0,0]) rotate([0,0,45]) top();
//translate([0,0,40]) rotate([0,0,45]) top();

//base_wide(135, .75*135);
//rotate([0,0,90]) translate([0,0,30]) rpi3();
//base_wide2(140, 100);
//translate([0,30,10]) power_board();
//translate([0,-30,10]) rotate([0,0,180]) power_board();

//bottom2(150,100);

//$fn=90;
//top2(140,100);
//bottom2(140,100);
