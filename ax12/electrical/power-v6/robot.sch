EESchema Schematic File Version 4
LIBS:robot-cache
EELAYER 26 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L robot-rescue:Conn_01x03 J1
U 1 1 5A7A565B
P 7400 2500
F 0 "J1" H 7400 2700 50  0000 C CNN
F 1 "C1-2" H 7400 2300 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 7400 2500 50  0001 C CNN
F 3 "" H 7400 2500 50  0001 C CNN
	1    7400 2500
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5A7F9C06
P 2150 7050
F 0 "#FLG01" H 2150 7125 50  0001 C CNN
F 1 "PWR_FLAG" H 2150 7200 50  0000 C CNN
F 2 "" H 2150 7050 50  0001 C CNN
F 3 "" H 2150 7050 50  0001 C CNN
	1    2150 7050
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5A935890
P 1500 7150
F 0 "#FLG02" H 1500 7225 50  0001 C CNN
F 1 "PWR_FLAG" H 1500 7300 50  0000 C CNN
F 2 "" H 1500 7150 50  0001 C CNN
F 3 "" H 1500 7150 50  0001 C CNN
	1    1500 7150
	-1   0    0    1   
$EndComp
$Comp
L power:+12V #PWR03
U 1 1 5AA56F03
P 1500 7050
F 0 "#PWR03" H 1500 6900 50  0001 C CNN
F 1 "+12V" H 1500 7190 50  0000 C CNN
F 2 "" H 1500 7050 50  0001 C CNN
F 3 "" H 1500 7050 50  0001 C CNN
	1    1500 7050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 5AA58E71
P 2150 7150
F 0 "#PWR04" H 2150 6900 50  0001 C CNN
F 1 "GND" H 2150 7000 50  0000 C CNN
F 2 "" H 2150 7150 50  0001 C CNN
F 3 "" H 2150 7150 50  0001 C CNN
	1    2150 7150
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 7150 1500 7050
Wire Wire Line
	2150 7150 2150 7050
$Comp
L robot-rescue:Conn_01x03 J8
U 1 1 5ACCFEAF
P 7400 3000
F 0 "J8" H 7400 3200 50  0000 C CNN
F 1 "LEG1" H 7400 2800 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 7400 3000 50  0001 C CNN
F 3 "" H 7400 3000 50  0001 C CNN
	1    7400 3000
	1    0    0    -1  
$EndComp
Text GLabel 6600 2100 0    60   BiDi ~ 0
DATA
Wire Wire Line
	7200 2400 7050 2400
Wire Wire Line
	7050 2100 7050 2400
Connection ~ 7050 2900
Wire Wire Line
	6950 3000 7200 3000
Connection ~ 6950 2500
Wire Wire Line
	6850 3100 7200 3100
Connection ~ 6850 2600
Connection ~ 6850 3100
$Comp
L robot-rescue:Conn_01x03 J10
U 1 1 5ACD102B
P 7400 3600
F 0 "J10" H 7400 3800 50  0000 C CNN
F 1 "LEG2" H 7400 3400 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 7400 3600 50  0001 C CNN
F 3 "" H 7400 3600 50  0001 C CNN
	1    7400 3600
	1    0    0    -1  
$EndComp
$Comp
L robot-rescue:Conn_01x03 J11
U 1 1 5ACD103D
P 7400 4100
F 0 "J11" H 7400 4300 50  0000 C CNN
F 1 "EXT" H 7400 3900 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 7400 4100 50  0001 C CNN
F 3 "" H 7400 4100 50  0001 C CNN
	1    7400 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	7050 3500 7200 3500
Wire Wire Line
	6950 4100 7200 4100
Connection ~ 6950 3600
Wire Wire Line
	6850 4200 7200 4200
Wire Wire Line
	6850 2500 6850 2600
Connection ~ 6850 4200
$Comp
L robot-rescue:Conn_01x03 J3
U 1 1 5ACD2202
P 9550 4650
F 0 "J3" H 9550 4850 50  0000 C CNN
F 1 "Data" H 9550 4450 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 9550 4650 50  0001 C CNN
F 3 "" H 9550 4650 50  0001 C CNN
	1    9550 4650
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 5ACD24C2
P 5850 2850
F 0 "D1" H 5850 2950 50  0000 C CNN
F 1 "PWR" H 5850 2750 50  0000 C CNN
F 2 "LEDs:LED_1206_HandSoldering" H 5850 2850 50  0001 C CNN
F 3 "" H 5850 2850 50  0001 C CNN
	1    5850 2850
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R1
U 1 1 5ACD2583
P 5850 3300
F 0 "R1" V 5930 3300 50  0000 C CNN
F 1 "2.4k" V 5850 3300 50  0000 C CNN
F 2 "Resistors_SMD:R_1206_HandSoldering" V 5780 3300 50  0001 C CNN
F 3 "" H 5850 3300 50  0001 C CNN
	1    5850 3300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 5ACD2691
P 5850 3600
F 0 "#PWR06" H 5850 3350 50  0001 C CNN
F 1 "GND" H 5850 3450 50  0000 C CNN
F 2 "" H 5850 3600 50  0001 C CNN
F 3 "" H 5850 3600 50  0001 C CNN
	1    5850 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 2200 5850 2700
Wire Wire Line
	5850 3000 5850 3150
Wire Wire Line
	5850 3450 5850 3600
$Comp
L robot-rescue:Conn_01x03 J14
U 1 1 5ACD2D1C
P 9550 2500
F 0 "J14" H 9550 2700 50  0000 C CNN
F 1 "C3-4" H 9550 2300 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 9550 2500 50  0001 C CNN
F 3 "" H 9550 2500 50  0001 C CNN
	1    9550 2500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR07
U 1 1 5ACD2D22
P 6850 5700
F 0 "#PWR07" H 6850 5450 50  0001 C CNN
F 1 "GND" H 6850 5550 50  0000 C CNN
F 2 "" H 6850 5700 50  0001 C CNN
F 3 "" H 6850 5700 50  0001 C CNN
	1    6850 5700
	1    0    0    -1  
$EndComp
$Comp
L robot-rescue:Conn_01x03 J15
U 1 1 5ACD2D2E
P 9550 3000
F 0 "J15" H 9550 3200 50  0000 C CNN
F 1 "LEG3" H 9550 2800 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 9550 3000 50  0001 C CNN
F 3 "" H 9550 3000 50  0001 C CNN
	1    9550 3000
	1    0    0    -1  
$EndComp
Text GLabel 8700 2100 0    60   BiDi ~ 0
DATA
Wire Wire Line
	9350 2400 9200 2400
Wire Wire Line
	9200 2100 9200 2400
Connection ~ 9200 2900
Wire Wire Line
	9100 3000 9350 3000
Connection ~ 9100 2500
Wire Wire Line
	9000 3100 9350 3100
Connection ~ 9000 3100
$Comp
L robot-rescue:Conn_01x03 J12
U 1 1 5ACD2DCD
P 9550 3550
F 0 "J12" H 9550 3750 50  0000 C CNN
F 1 "LEG4" H 9550 3350 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 9550 3550 50  0001 C CNN
F 3 "" H 9550 3550 50  0001 C CNN
	1    9550 3550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR08
U 1 1 5ACD2DD3
P 9000 5700
F 0 "#PWR08" H 9000 5450 50  0001 C CNN
F 1 "GND" H 9000 5550 50  0000 C CNN
F 2 "" H 9000 5700 50  0001 C CNN
F 3 "" H 9000 5700 50  0001 C CNN
	1    9000 5700
	1    0    0    -1  
$EndComp
$Comp
L robot-rescue:Conn_01x03 J13
U 1 1 5ACD2DDF
P 9550 4050
F 0 "J13" H 9550 4250 50  0000 C CNN
F 1 "EXT" H 9550 3850 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 9550 4050 50  0001 C CNN
F 3 "" H 9550 4050 50  0001 C CNN
	1    9550 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	9200 3450 9350 3450
Connection ~ 9200 3950
Wire Wire Line
	9100 4050 9350 4050
Connection ~ 9100 3550
Wire Wire Line
	9000 4150 9350 4150
Wire Wire Line
	9000 2500 9000 2600
Connection ~ 9000 4150
Wire Wire Line
	6950 2400 6950 2500
Wire Wire Line
	9100 2400 9100 2500
Wire Wire Line
	9350 2600 9000 2600
Connection ~ 9000 2600
Wire Wire Line
	7200 2600 6850 2600
Wire Wire Line
	7200 3700 6850 3700
Connection ~ 6850 3700
Wire Wire Line
	9350 3650 9000 3650
Connection ~ 9000 3650
Text Notes 4400 1600 0    60   ~ 0
AX-12A Quadruped Power Distribution Board\nVersion 5\nNote: the molex pin numbers appear to be in reverse\n--------------------------------\n1 - Data\n2 - 12V\n3 - Ground\n----------------------------\nTrying to keep the current draw around 3A per cable:\nCX-Y: coxa motors for leg X and leg Y\nLegX: tibia, fibia, and tarsus motors for leg X
Text Notes 4350 1950 0    60   ~ 0
Power LED
Text Notes 6350 1900 0    60   ~ 0
AX-12A Interfaces
Text Notes 7400 5700 0    60   ~ 0
Data and Power Alternate Interfaces
$Comp
L robot-rescue:Conn_01x03 J2
U 1 1 5AF331DD
P 7400 4700
F 0 "J2" H 7400 4900 50  0000 C CNN
F 1 "RPi" H 7400 4500 50  0000 C CNN
F 2 "Connectors_Molex:Molex_SPOX-5267_22-03-5035_03x2.54mm_Straight" H 7400 4700 50  0001 C CNN
F 3 "" H 7400 4700 50  0001 C CNN
	1    7400 4700
	1    0    0    -1  
$EndComp
Connection ~ 6950 3000
Wire Wire Line
	6950 2400 6650 2400
Wire Wire Line
	6850 2500 6600 2500
Wire Wire Line
	7200 2500 6950 2500
Connection ~ 7050 3500
Wire Wire Line
	7050 4000 7200 4000
Wire Wire Line
	7200 3600 6950 3600
Wire Wire Line
	9350 2500 9100 2500
Wire Wire Line
	9100 2400 8750 2400
Wire Wire Line
	8750 2500 9000 2500
Wire Wire Line
	9200 3950 9350 3950
Connection ~ 9200 3450
Wire Wire Line
	9350 3550 9100 3550
Connection ~ 9100 3000
Wire Wire Line
	9350 2900 9200 2900
Wire Wire Line
	9200 2100 8700 2100
Connection ~ 9200 2400
Wire Wire Line
	7200 2900 7050 2900
Wire Wire Line
	7050 2100 6600 2100
Connection ~ 7050 2400
Wire Wire Line
	7050 4600 7200 4600
Connection ~ 7050 4000
Wire Wire Line
	9200 4550 9350 4550
Wire Wire Line
	9100 4650 9350 4650
Connection ~ 9100 4050
Wire Wire Line
	7200 4800 6850 4800
Connection ~ 6850 4800
Wire Wire Line
	9350 4750 9000 4750
Connection ~ 9000 4750
Wire Notes Line
	6000 4350 10200 4350
Wire Notes Line
	10200 4350 10200 5550
Wire Notes Line
	10200 6100 6000 6100
Wire Notes Line
	6000 5550 6000 4350
Wire Wire Line
	5850 2200 6650 2200
Wire Wire Line
	6650 2200 6650 2400
Connection ~ 6650 2400
Wire Wire Line
	7050 2900 7050 3500
Wire Wire Line
	6950 2500 6950 3000
Wire Wire Line
	6850 2600 6850 3100
Wire Wire Line
	6850 3100 6850 3700
Wire Wire Line
	6950 3600 6950 4100
Wire Wire Line
	6850 4200 6850 4800
Wire Wire Line
	9200 2900 9200 3450
Wire Wire Line
	9100 2500 9100 3000
Wire Wire Line
	9000 3100 9000 3650
Wire Wire Line
	9200 3950 9200 4550
Wire Wire Line
	9100 3550 9100 4050
Wire Wire Line
	9000 4150 9000 4750
Wire Wire Line
	9000 2600 9000 3100
Wire Wire Line
	6850 3700 6850 4200
Wire Wire Line
	9000 3650 9000 4150
Wire Wire Line
	6950 3000 6950 3600
Wire Wire Line
	7050 3500 7050 4000
Wire Wire Line
	9200 3450 9200 3950
Wire Wire Line
	9100 3000 9100 3550
Wire Wire Line
	9200 2400 9200 2900
Wire Wire Line
	7050 2400 7050 2900
Wire Wire Line
	7050 4000 7050 4600
Wire Wire Line
	9100 4050 9100 4650
Wire Wire Line
	6850 4800 6850 4900
Wire Wire Line
	9000 4750 9000 5100
Wire Wire Line
	6650 2400 6600 2400
$Comp
L Connector:USB_A J5
U 1 1 5BF9F178
P 5400 4250
F 0 "J5" H 5455 4717 50  0000 C CNN
F 1 "USB_A" H 5455 4626 50  0000 C CNN
F 2 "Connectors:USB_A" H 5550 4200 50  0001 C CNN
F 3 " ~" H 5550 4200 50  0001 C CNN
	1    5400 4250
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x05 J6
U 1 1 5BFA49E0
P 6200 4900
F 0 "J6" H 6120 4475 50  0000 C CNN
F 1 "5V Pwr" H 6120 4566 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x05_Pitch2.54mm" H 6200 4900 50  0001 C CNN
F 3 "~" H 6200 4900 50  0001 C CNN
	1    6200 4900
	-1   0    0    1   
$EndComp
Wire Wire Line
	6400 4800 6850 4800
Wire Wire Line
	6400 4900 6850 4900
Connection ~ 6850 4900
Wire Wire Line
	6850 4900 6850 5150
NoConn ~ 6400 5100
$Comp
L power:GND #PWR0101
U 1 1 5BFB9CA6
P 5400 4800
F 0 "#PWR0101" H 5400 4550 50  0001 C CNN
F 1 "GND" H 5400 4650 50  0000 C CNN
F 2 "" H 5400 4800 50  0001 C CNN
F 3 "" H 5400 4800 50  0001 C CNN
	1    5400 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 4800 5400 4750
Wire Wire Line
	5300 4650 5300 4750
Wire Wire Line
	5300 4750 5400 4750
Connection ~ 5400 4750
Wire Wire Line
	5400 4750 5400 4650
NoConn ~ 5700 4250
NoConn ~ 5700 4350
$Comp
L power:+5V #PWR0102
U 1 1 5BFC6D63
P 5850 4050
F 0 "#PWR0102" H 5850 3900 50  0001 C CNN
F 1 "+5V" H 5865 4223 50  0000 C CNN
F 2 "" H 5850 4050 50  0001 C CNN
F 3 "" H 5850 4050 50  0001 C CNN
	1    5850 4050
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0103
U 1 1 5BFC6E0E
P 6950 4600
F 0 "#PWR0103" H 6950 4450 50  0001 C CNN
F 1 "+5V" H 6965 4773 50  0000 C CNN
F 2 "" H 6950 4600 50  0001 C CNN
F 3 "" H 6950 4600 50  0001 C CNN
	1    6950 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0104
U 1 1 5BFC6E39
P 6500 4600
F 0 "#PWR0104" H 6500 4450 50  0001 C CNN
F 1 "+5V" H 6515 4773 50  0000 C CNN
F 2 "" H 6500 4600 50  0001 C CNN
F 3 "" H 6500 4600 50  0001 C CNN
	1    6500 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 4050 5850 4050
Wire Wire Line
	6400 4700 6500 4700
Wire Wire Line
	6500 4700 6500 4600
Wire Wire Line
	7200 4700 6950 4700
Wire Wire Line
	6950 4700 6950 4600
$Comp
L power:+5V #PWR0105
U 1 1 5BFCCF39
P 1000 7050
F 0 "#PWR0105" H 1000 6900 50  0001 C CNN
F 1 "+5V" H 1015 7223 50  0000 C CNN
F 2 "" H 1000 7050 50  0001 C CNN
F 3 "" H 1000 7050 50  0001 C CNN
	1    1000 7050
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5BFCD434
P 1000 7150
F 0 "#FLG0101" H 1000 7225 50  0001 C CNN
F 1 "PWR_FLAG" H 1000 7300 50  0000 C CNN
F 2 "" H 1000 7150 50  0001 C CNN
F 3 "" H 1000 7150 50  0001 C CNN
	1    1000 7150
	-1   0    0    1   
$EndComp
Wire Wire Line
	1000 7050 1000 7150
Wire Wire Line
	6950 4100 6700 4100
Wire Wire Line
	6700 4100 6700 5000
Wire Wire Line
	6700 5000 6400 5000
Connection ~ 6950 4100
$Comp
L Mechanical:MountingHole H1
U 1 1 5BFD2444
P 8950 700
F 0 "H1" H 9050 746 50  0000 L CNN
F 1 "MountingHole" H 9050 655 50  0000 L CNN
F 2 "Mounting_Holes:MountingHole_2.2mm_M2" H 8950 700 50  0001 C CNN
F 3 "~" H 8950 700 50  0001 C CNN
	1    8950 700 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 5BFD296E
P 8950 900
F 0 "H2" H 9050 946 50  0000 L CNN
F 1 "MountingHole" H 9050 855 50  0000 L CNN
F 2 "Mounting_Holes:MountingHole_2.2mm_M2" H 8950 900 50  0001 C CNN
F 3 "~" H 8950 900 50  0001 C CNN
	1    8950 900 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 5BFD29A2
P 8950 1100
F 0 "H3" H 9050 1146 50  0000 L CNN
F 1 "MountingHole" H 9050 1055 50  0000 L CNN
F 2 "Mounting_Holes:MountingHole_2.2mm_M2" H 8950 1100 50  0001 C CNN
F 3 "~" H 8950 1100 50  0001 C CNN
	1    8950 1100
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 5BFD29D8
P 8950 1300
F 0 "H4" H 9050 1346 50  0000 L CNN
F 1 "MountingHole" H 9050 1255 50  0000 L CNN
F 2 "Mounting_Holes:MountingHole_2.2mm_M2" H 8950 1300 50  0001 C CNN
F 3 "~" H 8950 1300 50  0001 C CNN
	1    8950 1300
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J4
U 1 1 5BFB1889
P 6400 2500
F 0 "J4" H 6320 2175 50  0000 C CNN
F 1 "Leg1-2" H 6320 2266 50  0000 C CNN
F 2 "Wire_Connections_Bridges:WireConnection_2.50mmDrill_LargePad" H 6400 2500 50  0001 C CNN
F 3 "~" H 6400 2500 50  0001 C CNN
	1    6400 2500
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J7
U 1 1 5BFB1BE8
P 8550 2500
F 0 "J7" H 8470 2175 50  0000 C CNN
F 1 "Leg3-4" H 8470 2266 50  0000 C CNN
F 2 "Wire_Connections_Bridges:WireConnection_2.50mmDrill_LargePad" H 8550 2500 50  0001 C CNN
F 3 "~" H 8550 2500 50  0001 C CNN
	1    8550 2500
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J17
U 1 1 5BFBD4E7
P 9550 5000
F 0 "J17" H 9629 4992 50  0000 L CNN
F 1 "12V" H 9629 4901 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 9550 5000 50  0001 C CNN
F 3 "~" H 9550 5000 50  0001 C CNN
	1    9550 5000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J18
U 1 1 5BFBD5C7
P 9550 5300
F 0 "J18" H 9629 5292 50  0000 L CNN
F 1 "12V" H 9629 5201 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 9550 5300 50  0001 C CNN
F 3 "~" H 9550 5300 50  0001 C CNN
	1    9550 5300
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J9
U 1 1 5BFBD605
P 7400 5050
F 0 "J9" H 7479 5042 50  0000 L CNN
F 1 "5V" H 7479 4951 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 7400 5050 50  0001 C CNN
F 3 "~" H 7400 5050 50  0001 C CNN
	1    7400 5050
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J16
U 1 1 5BFBD645
P 7400 5350
F 0 "J16" H 7479 5342 50  0000 L CNN
F 1 "5V" H 7479 5251 50  0000 L CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 7400 5350 50  0001 C CNN
F 3 "~" H 7400 5350 50  0001 C CNN
	1    7400 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 5050 6950 5050
Wire Wire Line
	6950 5050 6950 4700
Connection ~ 6950 4700
Wire Wire Line
	7200 5350 6950 5350
Wire Wire Line
	6950 5350 6950 5050
Connection ~ 6950 5050
Wire Wire Line
	7200 5150 6850 5150
Connection ~ 6850 5150
Wire Wire Line
	6850 5150 6850 5450
Wire Wire Line
	7200 5450 6850 5450
Connection ~ 6850 5450
Wire Wire Line
	6850 5450 6850 5700
Wire Wire Line
	9350 5000 9100 5000
Wire Wire Line
	9100 5000 9100 4650
Connection ~ 9100 4650
Wire Wire Line
	9350 5300 9100 5300
Wire Wire Line
	9100 5300 9100 5000
Connection ~ 9100 5000
Wire Wire Line
	9350 5100 9000 5100
Connection ~ 9000 5100
Wire Wire Line
	9000 5100 9000 5400
Wire Wire Line
	9350 5400 9000 5400
Connection ~ 9000 5400
Wire Wire Line
	9000 5400 9000 5700
$EndSCHEMATC
