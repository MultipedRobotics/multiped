// linear_extrude(height = 10, center = true, convexity = 10, scale=2)
// translate([2, 0, 0])
// circle(r = 1, $fn=100);

$fn = 45;
 // d1 = bottom
 // d2 = top radius
 module seg(d1,d2,l){
     scale([.5,1,1]) cylinder(h=l,d1=d1,d2=d2,center=false);
 }

union(){
    scale([2,2,2]) import("tibiaLong_SLA.STL");
//    cube([20,20,20], center=true);
}
//translate([-70,-300,-179]) rotate([0,0,0]) import("AX-12A.STL");
 

//min = 0.1;
//max = 1;
// for(i=[0:max/min:max]){
//     h = 1;
//     th = h*i;
//     angle = i*10;
//     d1 = min*(i+1);
//     d2 = min*(i+2);
//     rotate([0,angle,0]) translate([0,0,th]) seg(d1,d2,h);
// }

// translate([0,0,h]) seg(d1,d2,h)
//seg(0.1,0.4,1);
//translate([0,0,1]) seg(0.4,0.7,1);

//union(){
//	difference(){
//		rotate_extrude(angle=120) translate ([50,0,0]) circle(10);
//		difference(){
//			cube([120,120,40], center = true);
//			translate([30,30,0]) cube([60,60,40], center = true);	
//			}
////		rotate_extrude(angle=120) translate([50,0,0]) circle(8);
////		difference(){
////			cube([120,120,40], center = true);
////			translate([30,30,0]) cube([60,60,40], center = true);	
////		}
//	}
//	difference(){
//		translate([50,0,0]) rotate([90,0,0]) cylinder(r=10,h=20);
//		translate([50,0,0]) rotate([90,0,0]) cylinder(r=8,h=22);
//	}
//	difference(){
//		translate([0,50,0]) rotate([0,270,0]) cylinder(r=10,h=20);
//		translate([0,50,0]) rotate([0,270,0]) cylinder(r=8,h=22);
//	}	
//}