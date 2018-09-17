
// Simple primatives for generating holes

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

module M3Nut(t){
    dia = 3.5;
    sdia = 9;
    cylinder(3*t, d=dia, center=true);  // M3
    translate([0,0,2]) cylinder(3*t, d=sdia, center=false);  // screw driver
}



module M3(t){
    dia = 3.5;
    sdia = 8.5;  // counter sink dia
    cylinder(3*t, d=dia, center=true);  // M3
    translate([0,0,2]) cylinder(3*t, d=sdia, center=false);  // screw driver
}

module M2(t){
    dia = 2.5;
    sdia = 6;  // counter sink dia
    cylinder(3*t, d=dia, center=true);  // M2
    translate([0,0,2]) cylinder(3*t, d=sdia, center=false);  // screw driver
}


/* module holes(t){
    // M3 3.3 mm
    M3(t);

    // M2 2.3 mm
    // dia = 2.3;
    translate([8,0,0]) M2(t);
    translate([-8,0,0]) M2(t);
    translate([0,8,0]) M2(t);
    translate([0,-8,0]) M2(t);
}

module pulley(dia=24, thick=3, cen=false){
    cylinder(thick,d=dia,center=cen);
} */
