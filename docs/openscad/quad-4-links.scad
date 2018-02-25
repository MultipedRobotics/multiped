$fn=45;

module joint(l, c="gray"){
    color(c) cylinder(5,1,center=true);
    rotate([0,90,0]) color(c) cylinder(l,1);
}

module leg(l1, l2, l3,l4, a1, a2, a3,a4){
    rotate([0,0,a1]) joint(l1, "red");
    rotate([0,0,a1]) translate([l1,0,0]) rotate([90,-a2,0]) joint(l2,"blue");
    rotate([0,0,a1]) translate([l1,0,0]) rotate([90,-a2,0]) translate([l2,0,0]) rotate([0,0,a3]) joint(l3,"yellow");
    rotate([0,0,a1]) translate([l1,0,0]) rotate([90,-a2,0]) translate([l2,0,0]) rotate([0,0,a3]) translate([l3,0,0]) rotate([0,0,a4]) joint(l4,"green");
}

module quad(dia,l1,l2,l3,l4,a1,a2,a3,a4){
    offset = sqrt((dia/2)*dia/2/2);
    color("gray") cylinder(4,d=dia,center=true);
    translate([offset,offset,0]) rotate([0,0,45]) leg(l1,l2,l3,l4,a1,a2,a3,a4);
    translate([offset,-offset,0]) rotate([0,0,-45]) leg(l1,l2,l3,l4,a1,a2,a3,a4);
    translate([-offset,-offset,0]) rotate([0,0,-135]) leg(l1,l2,l3,l4,a1,a2,a3,a4);
    translate([-offset,offset,0]) rotate([0,0,135]) leg(l1,l2,l3,l4,a1,a2,a3,a4);
    cylinder(6,d=2);
    translate([0,0,6]) cylinder(6,d=4);
}

quad(8,4,7,10,4,0,60,-90,-60);
//quad(8,4,7,10,0,90,-160);
//quad(8,4,7,10,0,-45,-45);


//quad(100,40,70,100,0,20,-110);