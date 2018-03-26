$fn=90;
use <common.scad>;
use <sternum.scad>;


/* module cam(d,xs,ys,zs){
    thick = 2;
    cam_width = 30;
    difference(){
        translate([-50,-cam_width/2,10]) cube([2*xs*d,cam_width,60], center=false);
        translate([0,-cam_width/2+thick,0]) cube([xs*d/2-2*thick,cam_width-2*thick,d/2-2*thick], center=false);
        scale([xs,ys,1]) sphere(d=d-thick,center=true);
    }
} */

module shell(d,xscale,yscale,zscale){
    difference(){
        thick = 2;
        cam_width = 30;
        scale([xscale,yscale,zscale]) sphere(d=d,center=true);   // outer shell
        scale([xscale,yscale,zscale]) sphere(d=d-thick,center=true);    // inner shell
        translate([-d,-d,-2*d]) cube(2*d, center=false);  // bottom
        translate([0,-cam_width/2,0]) cube([xscale*d/2,cam_width,d/2], center=false); // camera
    }
}


//translate([0,0,0]) cylinder(10,d=30, center=true);
//translate([0,0,-20]) rotate([0,0,45]) top();

//cam(100,1.25,0.9);

// Calculate the cap of a sphere
// r = raduis mm
// h = height of cap mm
// http://www.ambrsoft.com/TrigoCalc/Sphere/Cap/SphereCap.htm#cap
module cap(r,h){
    d = 2*r;
    difference()
    {
        translate([0,0,-(r-h)]) sphere(d=d);
        translate([0,0,-d/2]) cube([d,d,d], center=true);
    }

}

// Adafruit mini 8x8 led matrix w/i2c backpack
// item: 1080
module miniled(){
    h = 4;
    m = 20;
    b = 28;
    thick = 2;

    translate([0,0,2]) cube([m,m,3], center=true);
    translate([0,0,0.5]) cube([b,m,1], center=true);
}

module head(){
    union(){
        xscale = 1;
        yscale = 1;
		zscale = 1;
        cylinder(h=3, r=50);
        //shell(50,xscale,yscale,zscale);
        //cam(50,xscale,yscale,zscale);
    }
}

/* translate([0,0,40]) rotate([0,0,0]) rpi3();
translate([-1.2*50,0,30]) rotate([0,0,180]) rotate([90,0,90]) picamera();
translate([0,0,-20]) rotate([0,0,45]) top();
translate([0,0,40]) head(); */
////shell(100,1.25,0.9);
/* color("Gold", 0.5) head(); */

//head();

translate([0,40,12]) rotate([-25,0,0]) miniled();
translate([12,0,0])  rpi3();
translate([-20-12/2,-30-35, 0]) cube([12,35,15], center=false);
translate([-45,0,-10]) rotate([0,0,180]) rotate([90,0,90]) picamera();
color("Gold", 0.5) translate([0,0,10]) scale([1,1,1.5]) cap(150, 10);
translate([0,0,-3]) cylinder(h=13, r=53.852);
/* color("Gold", 0.5) rotate([180,0,0]) scale([1,1,1.5]) cap(350, 20); */
