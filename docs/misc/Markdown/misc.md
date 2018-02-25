Name:   mcp23017
Info:   Configures the MCP23017 I2C GPIO expander
Load:   dtoverlay=mcp23017,<param>=<val>
Params: gpiopin                 Gpio pin connected to the INTA output of the
                                MCP23017 (default: 4)

        addr                    I2C address of the MCP23017 (default: 0x20)




Name:   i2s-gpio28-31
Info:   move I2S function block to GPIO 28 to 31
Load:   dtoverlay=i2s-gpio28-31
Params: <None>


Name:   i2c1-bcm2708
Info:   Enable the i2c_bcm2708 driver for the i2c1 bus
Load:   dtoverlay=i2c1-bcm2708,<param>=<val>
Params: sda1_pin                GPIO pin for SDA1 (2 or 44 - default 2)
        scl1_pin                GPIO pin for SCL1 (3 or 45 - default 3)
        pin_func                Alternative pin function (4 (alt0), 6 (alt2) -
                                default 4)


Name:   i2c-rtc
Info:   Adds support for a number of I2C Real Time Clock devices
Load:   dtoverlay=i2c-rtc,<param>=<val>
Params: ds1307                  Select the DS1307 device

        ds1339                  Select the DS1339 device

        ds3231                  Select the DS3231 device

        mcp7940x                Select the MCP7940x device

        mcp7941x                Select the MCP7941x device

        pcf2127                 Select the PCF2127 device

        pcf8523                 Select the PCF8523 device

        pcf8563                 Select the PCF8563 device

        trickle-resistor-ohms   Resistor value for trickle charge (DS1339-only)

        wakeup-source           Specify that the RTC can be used as a wakeup
                                source


Name:   i2c-pwm-pca9685a
Info:   Adds support for an NXP PCA9685A I2C PWM controller on i2c_arm
Load:   dtoverlay=i2c-pwm-pca9685a,<param>=<val>
Params: addr                    I2C address of PCA9685A (default 0x40)




Name:   i2c-mux
Info:   Adds support for a number of I2C bus multiplexers on i2c_arm
Load:   dtoverlay=i2c-mux,<param>=<val>
Params: pca9542                 Select the NXP PCA9542 device

        pca9545                 Select the NXP PCA9545 device

        pca9548                 Select the NXP PCA9548 device

        addr                    Change I2C address of the device (default 0x70)



Name:   i2c-gpio
Info:   Adds support for software i2c controller on gpio pins
Load:   dtoverlay=i2c-gpio,<param>=<val>
Params: i2c_gpio_sda            GPIO used for I2C data (default "23")

        i2c_gpio_scl            GPIO used for I2C clock (default "24")

        i2c_gpio_delay_us       Clock delay in microseconds
                                (default "2" = ~100kHz)

pandoc *.md -f markdown -t html -s --highlight-style pygments --mathjax -o test/index.html