$fn=90;
use <common.scad>;
use <sternum.scad>;


module cam(d,xs,ys){
    thick = 2;
    cam_width = 30;
    difference(){
        translate([0,-cam_width/2,0]) cube([xs*d/2,cam_width,d/2], center=false);
        translate([0,-cam_width/2+thick,0]) cube([xs*d/2-2*thick,cam_width-2*thick,d/2-2*thick], center=false);
        scale([xs,ys,1]) sphere(d=d-thick,center=true);
    }
}

module shell(d,xscale,yscale){
    difference(){
        thick = 2;
        cam_width = 30;
        scale([xscale,yscale,1]) sphere(d=d,center=true);   // outer shell
        scale([xscale,yscale,1]) sphere(d=d-thick,center=true);    // inner shell
        translate([-d,-d,-2*d]) cube(2*d, center=false);  // bottom
        translate([0,-cam_width/2,0]) cube([xscale*d/2,cam_width,d/2], center=false); // camera
    }
}


//translate([0,0,0]) cylinder(10,d=30, center=true);
//translate([0,0,-20]) rotate([0,0,45]) top();

//cam(100,1.25,0.9);

module head(){
    union(){
        xscale = 1.25;
        yscale = 0.9;
        shell(100,xscale,yscale);
        cam(100,xscale,yscale);
    }
}

//translate([0,0,5]) rotate([0,0,180]) rpi3();
//translate([1.25*50,0,25]) rotate([90,0,90]) picamera();
//translate([0,0,-20]) rotate([0,0,45]) top();
////shell(100,1.25,0.9);
//color("Gold", 0.5) head();

head();