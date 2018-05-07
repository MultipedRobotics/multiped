nudge = 0.01;

cover();
//lrs350();

//bottom_holes();



module cover() {

    difference() {
        union() {
            translate([-3,-3,-45]) cube([115+6,30+6,50]);
            translate([-3,-3,-45]) cube([115+6,15+6,55+10]);
            translate([-3+56,-3-7,-45]) cube([62,30+6,38]);
            screw_extendys();
            
        }
        
        // psu
        translate([0-.25,0-.25,0-.25]) cube([115+.5,30+.5,50]);
        
        // inside
        translate([3,3,-43]) cube([115-6,30-6,50]);
        
//        translate([4,-6,-34]) cube([115-8,40,34+nudge]);
        
        translate([60,-10-nudge,-12]) rotate([-90,0,0]) iec_cutout();
        bottom_holes();
        
        
        
        
        translate([95,10,-32]) rotate([-90,0,0]) cylinder(d=12,h=100);
//        translate([20,10,-32]) rotate([-90,0,0]) cylinder(d=12,h=100);
        
        
        
    }
    
    


}
module lrs350() {
    
    color("silver")
    difference() {
        cube([115,30,235]);
        translate([-nudge,30-12.5,32.5]) rotate([0,90,0]) cylinder(d=4,h=115+(2*nudge));
    }
}

module screw_extendys() {
    
    difference() {
       hull() {
            translate([-3,30-12.5,32.5]) rotate([0,90,0]) cylinder(d=12,h=115+6);
            translate([-3,30-12.5,4]) rotate([0,90,0]) cylinder(d=25,h=115+6);
       }
        translate([-10,30-12.5,32.5]) rotate([0,90,0]) cylinder(d=4,h=150);

        translate([-3,30-12.5,32.5]) rotate([0,90,0]) cylinder(d1=8.5,d2=4.5,h=2);
        translate([115+3,30-12.5,32.5]) rotate([0,-90,0]) cylinder(d1=8.5,d2=4.5,h=2);
    }    
}




module iec_cutout() {
    
    h = 15;
    
    union() {
        linear_extrude(height=h)
            polygon([[0,0],[42,0],[48,6],[48,22],[42,28],[0,28]]);
        translate([0,0,1.3])
        linear_extrude(height=h)
            union() {
                translate([5,-2]) square([10,2]);
                translate([5,28]) square([10,2]);
                translate([32,-2]) square([8,2]);
                translate([32,28]) square([8,2]);
            }
        
    }
}

module bottom_holes() {
    
    translate([7,7,-50])
        for (x = [0:22:90]) {
            for (y=[0:8:20]) {
            hull() {
                translate([x,y,0]) cylinder(r=2,h=100);
                translate([x+12,y,0]) cylinder(r=2,h=100);
            }
        }
    }
    
    
}