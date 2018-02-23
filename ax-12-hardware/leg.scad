$fn=45;


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

module spar(L){
//    difference(){
//        linear_extrude(5){
            hull(){
                circle(d=1.25*40);
                translate([2.25*40/4,0,0]) square(35, center=true);
            }
//        }
//        translate([2.25*40/4+6,0,0]) cube([26,21,12], center=true);
//    }
//    color("gray") translate([2.25*40/4+15,0,-12]) rotate([0,0,-90]) ax12();
}

module base(D){
    difference(){
        union(){
            circle(d=.75*D);
            L=D/8;
            rotate([0,0,0]) translate([L,0,0])  spar(D);
            rotate([0,0,90]) translate([L,0,0]) spar(D);
            rotate([0,0,180]) translate([L,0,0]) spar(D);
            rotate([0,0,270]) translate([L,0,0]) spar(D);
        }
        circle(d=20);  // cable hole
        rotate([0,0,0])  translate([35/2+2.25*40/4,0,0]) square([26,21],center=true);
        rotate([0,0,90])  translate([35/2+2.25*40/4,0,0]) square([26,21],center=true);
        rotate([0,0,180])  translate([35/2+2.25*40/4,0,0]) square([26,21],center=true);
        rotate([0,0,270])  translate([35/2+2.25*40/4,0,0]) square([26,21],center=true);
    }
}

base(100);





