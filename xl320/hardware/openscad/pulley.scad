use <common.scad>

module pulley(height=3){
    /*
    This creates a pulley to offset a side w/o a horn.
    */
    difference(){
        cylinder(height,9,9, true);
        hornHoles(0,0,0,0);
    }
}

pulley();
