# Simple demo of reading the difference between channel 1 and 0 on an ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain
import time
import math
import matplotlib.pyplot as plt
import logging


# Import the ADS1x15 module.
from ADS1x15 import ADS1115


# Create an ADS1115 ADC (16-bit) instance.
#adc = ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
adc = ADS1115()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 16

voltList = []
stressList = []
timeList = []

logging.basicConfig(filename='data.log', filemode='w',level=logging.DEBUG)

Vex = 5
R = 350
GF = 123
E = 69 * 10 ** 9


print('Press Ctrl-C to quit...')
timeStart = time.time()
try:
    while True:
        # Read the difference between channel 0 and 1 (i.e. channel 0 minus channel 1).
        # Note you can change the differential value to the following:
        #  - 0 = Channel 0 minus channel 1
        #  - 1 = Channel 0 minus channel 3
        #  - 2 = Channel 1 minus channel 3
        #  - 3 = Channel 2 minus channel 3
        value = adc.read_adc_difference(0, gain=GAIN)
        # Note you can also pass an optional data_rate parameter above, see
        # simpletest.py and the read_adc function for more information.
        # Value will be a signed 12 or 16 bit integer value (depending on the ADC
        # precision, ADS1015 = 12-bit or ADS1115 = 16-bit).
        factor = value / 32767
        volts = factor * 4.096/GAIN
        voltList.append(volts)
        
        timerec = time.time()
        delta = timerec -timeStart
        
        timeList.append(delta)
        #print(volts)
        logging.info("volts {}".format(volts) + ", " + "time {}".format(delta))
        print('Channel 0 minus 1: {0}'.format(value))
        print('Voltage: {0}'.format(volts))
        
        
        # Pause for 0.01 seconds.
        time.sleep(0.01)
        
except KeyboardInterrupt:
    for volts in voltList:
        deltaR = volts / Vex * R
        strain = deltaR / (R * GF)
        stress = E * strain
        stressList.append(stress)
    
        
        
    
    plt.plot(timeList, stressList)
    plt.ylabel("Stress (N/m2)")
    plt.xlabel("Time(s)")
    plt.show()
except Exception as e:
    print(e)
