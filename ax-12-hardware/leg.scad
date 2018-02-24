$fn=50;


module foot(L, W){
    union(){
        cylinder(L,d=W, center=true);
        translate([0,0,L/2]) sphere(d=W);  // end cap
        translate([0,0,-L/2]) sphere(d=W);  // end cap
    }
}
    
module tibia(){
    L = 100;
    union(){
        rotate([0,-10,0]) scale([1,1.2,1.5]) difference(){
            scale([2, .9, .55]) sphere(d=L); //d=5
            translate([0,1/5*L,-2/5*L]) scale([2.5, .5, .8]) sphere(d=8/5*L);  // d=8
            translate([0,-1/5*L,-2/5*L]) scale([2.5, .5, .8]) sphere(d=8/5*L);
        }
        translate([-1*L,0,-5]) rotate([0,-120,0]) foot(3/5*L,10);
        translate([35,0,33]) cube([25,35,15], center=true);  // mount
    }
}

module M3(t){
    dia = 3.5;
    sdia = 6;
    cylinder(3*t, d=dia, center=true);  // M2
    translate([0,0,2]) cylinder(3*t, d=sdia, center=false);  // screw driver
}

module M2(t){
    dia = 2.5;
    sdia = 4;
    cylinder(3*t, d=dia, center=true);  // M2
    translate([0,0,2]) cylinder(3*t, d=sdia, center=false);  // screw driver
}


module holes(t){
    // M3 3.3 mm
    M3(t);
    
    // M2 2.3 mm
    dia = 2.3;
    translate([8,0,0]) M2(t);
    translate([-8,0,0]) M2(t);
    translate([0,8,0]) M2(t);
    translate([0,-8,0]) M2(t);
}

module pulley(dia=24, thick=3, cen=false){
    cylinder(thick,d=dia,center=cen);
}

module ax12(){
    // sort of center mass
    translate([-70,-210,-180]) import("AX-12A.STL");
}

module femur(L){
    thick = 4;
    difference(){
        union(){
            translate([L/2,0,0]) pulley(thick=thick);
            translate([-L/2,0,0]) pulley(thick=thick);
            linear_extrude(height=thick){
                difference(){
                    resize([1.2*L,L/2]) circle(d=L/3);
                    translate([0,-5,0]) resize([.75*L,L/7]) circle(d=L/3);
                    translate([-L/2,-L/2-5,0]) square([L,L/2]);
                }
            }
        }
        translate([L/2,0,0]) holes(thick);
        translate([-L/2,0,0]) holes(thick);
    }
}

module femur2(L){
    thick = 40;
//    difference(){
//        union(){
//            translate([L/2,0,0]) pulley(thick=thick);
//            translate([-L/2,0,0]) pulley(thick=thick);
            linear_extrude(height=thick)
//                rotate_extrude(angle=30, convexity = 20)
    {
                    rotate([0,0,90]) difference(){
                        resize([L,L/2]) circle(d=L/3);
                        translate([0,0,0]) resize([1.2*L,L/3]) circle(d=L/3);
                        translate([-L/2,0,0]) square([2*L,L/2]);
                    }
                }
//            }
//        }
//        translate([L/2,0,0]) holes(thick);
//        translate([-L/2,0,0]) holes(thick);
//    }
//    hull(){
//        translate([0,0,0]) circle(d=40);
//        translate([L,0,0]) circle(d=10);
//    }
    
    
}





//femur2(90);
//rotate([0,0,0]) tibia();
//translate([40,-5,0]) rotate([0,90,-90]) ax12();

module hex(side,t){
    s = side/2;
    h = sqrt(side*side-s*s);
    pts = [
        [2*s,0],
        [s,h],
        [-s,h],
        [-2*s,0],
        [-s,-h],
        [s,-h]
    ];
    linear_extrude(height=t){
        polygon(pts);
    }
}

//hex(5,3);

//module spar(L){
//    hull(){
//        circle(d=1.25*40);
//        translate([2.25*40/3-3,0,0]) square(35, center=true);
//    }
//}

module spar(L){
    linear_extrude(4){
    hull(){
        circle(d=1.25*40);
        translate([2.25*40/3-3,0,0]) square(35, center=true);
    }
}
}

module rpi3(){
    // sort of center mass
    translate([-3-88.5/2,-2-56/2,0]) import("rpi3.STL");
}


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

//module servo_mnt(){
//    d = 2.5;
//    w = 22; // center servo
//    l = 35; // center servo
//    s = 38.5-2.5;
//    
//    translate([32,-20,0]) square([20,40],center=false);
//    translate([2.5,-w/2,0])square([l,w],center=false);
//    // bottom holes
//    translate([0,8,0]) circle(d=d);
//    translate([0,-8,0]) circle(d=d);
//    
//    // right holes
//    translate([5.5,-27/2,0]) circle(d=d);
//    translate([5.5+8,-27/2,0]) circle(d=d);
//    translate([5.5+16,-27/2,0]) circle(d=d);
//    translate([5.5+24,-27/2,0]) circle(d=d);
//    
//    // left holes
//    translate([5.5,27/2,0]) circle(d=d);
//    translate([5.5+8,27/2,0]) circle(d=d);
//    translate([5.5+16,27/2,0]) circle(d=d);
//    translate([5.5+24,27/2,0]) circle(d=d);
//}

module servo_mnt(){
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
}

module base(D){
    servo = 35/2+2.25*40/2;
    difference(){
    linear_extrude(4){
        spar_len = 30;
        difference(){
            union(){
                circle(d=.75*D);
                rotate([0,0,0]) translate([spar_len,0,0])  spar(D);
                rotate([0,0,90]) translate([spar_len,0,0]) spar(D);
                rotate([0,0,180]) translate([spar_len,0,0]) spar(D);
                rotate([0,0,270]) translate([spar_len,0,0]) spar(D);
            }
            circle(d=20);  // cable hole
            rotate([0,0,0])  translate([servo/2,0,0]) servo_mnt();
            rotate([0,0,90])  translate([servo/2,0,0]) servo_mnt();
            rotate([0,0,180])  translate([servo/2,0,0]) servo_mnt();
            rotate([0,0,270])  translate([servo/2,0,0]) servo_mnt();
            
            rpi_holes();
        }
    }
    rotate([0,0,0])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    rotate([0,0,90])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    rotate([0,0,180])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    rotate([0,0,270])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    }
}

module base2(D){
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
            
            rpi_holes();
        }
    rotate([0,0,0])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    rotate([0,0,90])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    rotate([0,0,180])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    rotate([0,0,270])  translate([servo/2-2.5,-32/2,2]) cube([40,32,5], center=false);
    }
}

module bottom(){
    rotate([180,0,0])  translate([0,0,32]) base2(135);
    translate([0,0,-32-20]) difference(){
        dia = 50;
        h = 20;
        cylinder(h, d=dia);
//        translate([15,-20,-1]) cube([40,40,30]);
        translate([dia/1.75,0,0]) cube([dia/2,dia, 2*h], center=true);
        translate([-dia/1.75,0,0]) cube([dia/2,dia, 2*h], center=true);
    }
}


module f2(){
    // sort of center mass
    translate([0,0,0]) import("f2.stl");
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


//color("SkyBlue") base2(135);
//color("gray") translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
//color("gray") rotate([0,0,90]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
//color("gray") rotate([0,0,180]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();
//color("gray") rotate([0,0,270]) translate([2.25*40/4+30,0.5,-12]) rotate([0,0,-90]) ax12();

//color("SkyBlue") rotate([0,0,45]) translate([0,0,4]) rpi_base();
//color("ForestGreen") rotate([0,0,45]) translate([11,0,20]) rpi3();

//color("SkyBlue") bottom();

//color("lightgray") translate([0,-67,-16]) f2();
//color("lightgray") rotate([0,0,90])  translate([0,-67,-16]) f2();
//color("lightgray") rotate([0,0,180]) translate([0,-67,-16]) f2();
//color("lightgray") rotate([0,0,270]) translate([0,-67,-16]) f2();

rotate_extrude($fn=200) polygon( points=[[0,0],[2,0],[2,1],[1,2],[1,8],[3,10],[0,10]] );

