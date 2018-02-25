

module rpi_holes(){
    x = 58/2;
    y = 49/2;
    d = 3.5;
    h=20;
    translate([x,y,-1]) cylinder(h,d=d);
    translate([-x,-y,-1]) cylinder(h,d=d);
    translate([x,-y,-1]) cylinder(h,d=d);
    translate([-x,y,-1]) cylinder(h,d=d);
}

module rpi_base(){
    x = 58/2;
    y = 49/2;
    d = 3.5;
    h=20;
    thick = 3;
    translate([0,0,11.5]) union(){
        difference(){
//            translate([0,0,0]) cube([2*x+10+30,2*y+10,thick], center=true);
            translate([0,0,0]) cylinder(thick, d=85, center=true);
            // mounting holes
            translate([x,y,-10]) cylinder(h,d=d);
            translate([-x,-y,-10]) cylinder(h,d=d);
            translate([x,-y,-10]) cylinder(h,d=d);
            translate([-x,y,-10]) cylinder(h,d=d);
            cylinder(10, d=20, center=true);
        }
        neck = 10;
        difference(){
            translate([0,0,-neck/2-thick/2]) cylinder(neck, d1=30, d2=50, center=true);
            translate([0,0,-neck/2-thick/2]) cylinder(2*neck,d=20, center=true);
        }
    }
}
