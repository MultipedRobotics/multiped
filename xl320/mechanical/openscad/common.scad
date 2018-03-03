
// create a 4-40 hole for mounting
module 4_40_hole(len=20, cen=true){
    // should be like 2.8448 mm
    cylinder(len,d=3,center=cen);
}


module bottomHoles(x=0,y=0,z=0){
    center = true;
    height = 15;
    hole = 2.15; // 4.1 mm diameter
    hdist = 6; // 6 mm center to center distance
    vdist = 18; // 18 mm center to center distance
    translate([x-6,y,z]){
        cylinder(height,hole,hole, center);
        translate([hdist,0,0]) cylinder(height,hole,hole, center);
        translate([2*hdist,0,0]) cylinder(height,hole,hole, center);
    }
}

// the 5 hold cross for a servo horn
module hornHoles(x=0, y=0, z=0, angle=0){
    height = 15;
    hole = 2.15; // 4.1 mm diameter
    dist = 6; // 6 mm center to center distance
    rotate([0,0,angle]){
        center = true;
        translate([x-6,y,z]){
            cylinder(height, 2, 2, center);
            translate([dist,0,0]){
                cylinder(height, 2, 2, center);
                translate([dist,0,0]){
                    cylinder(height, 2, 2, center);
                }
            }
            translate([dist, dist, 0]) {
                cylinder(height, 2, 2, center);
            }
            translate([dist, -dist, 0]) {
                cylinder(height, 2, 2, center);
            }
        }
    }
}

// a 3D triangular shape, point is at 0,0,0
module strut(length, width, height){
    points2 = [ [10,10,0],[10,-10,0],[-10,-10,0],[-10,10,0], // the four points at base
           [0,0,10]  ];
    points = [
        [0,0,0],
        [width,0,0],
        [width,length,0],
        [0,length,0],
        [0,length,height],
        [width,length,height]
    ];
    faces=[[0,1,2,3],[5,4,3,2],[0,4,5,1],[0,3,4],[5,2,1]];
    polyhedron(points, faces);
}
