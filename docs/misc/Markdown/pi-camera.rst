Pi Camera
==========

The `Pi Camera <https://www.raspberrypi.org/documentation/hardware/camera/README.md>`_

Power: 3.3v @ 250 mA  `ref ... look in the text <https://www.raspberrypi.org/help/faqs/#power>`_

=================== =================================== ==============================
Param               Camera v1                           Camera v2
=================== =================================== ==============================
Size                around 25 x 24 x 9 mm
Weight	            3g
Still resolution    5 Megapixels                        8 Megapixels
Video modes         1080p30, 720p60 and 640 × 480p60/90 1080p30, 720p60 and 640 × 480p60/90
Linux integration   V4L2 driver available               V4L2 driver available
C programming API   OpenMAX IL and others available     OpenMAX IL and others available
Sensor              OmniVision OV5647                   Sony IMX219
Sensor resolution	2592 × 1944 pixels                  3280 × 2464 pixels
Sensor image area   3.76 x 2.74 mm
Pixel size	        1.4 µm x 1.4 µm
Optical size        1/4"
SLR lens equivalent 35 mm
S/N ratio           36 dB
Dynamic range       67 dB @ 8x gain
Sensitivity         680 mV/lux-sec
Dark current        16 mV/sec @ 60 C
Well capacity       4.3 Ke-
Fixed focus         1 m to infinity
=================== =================================== ==============================

Grab a still image::

	raspistill -o cam.jpg

Grab video::

	raspivid -o vid.h264
