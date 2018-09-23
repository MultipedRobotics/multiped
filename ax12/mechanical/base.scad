
module interface(h, dia){
    difference(){
        cylinder(h=h,d=dia);
        translate([0,0,-1]) cylinder(h=h,d2=0, d1=dia-1);
    }
}


module robot_stand(height){
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
}
