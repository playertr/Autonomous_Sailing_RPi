# Copied from https://www.raspberrypi.org/forums/viewtopic.php?t=265284
# Derived from sosandroid's AMS_AS5048B Arduino library,
# https://github.com.cnpmjs.org/sosandroid/AMS_AS5048B

import sys
import smbus
import time
from datetime import datetime

bus = smbus.SMBus(1)
#RE_ADDRESS_LIST = [0x40, 0x41]
RE_ADDRESS_LIST = [0x40]
RE_ZEROMSB_REG = 0x16  # Zero, most significant byte
RE_ZEROLSB_REG = 0x17  # Zero, least significant byte
RE_MAGNMSB_REG = 0xFC  # Magnitude, most significant byte
RE_MAGNLSB_REG = 0xFD  # Magnitude, least significant byte
RE_ANGLEMSB_REG = 0xFE  # Angle, most significant byte
RE_ANGLELSB_REG = 0xFF  # Angle, least significant byte


# sets initial position to zero
for RE_ADDRESS in RE_ADDRESS_LIST:
    bus.write_byte_data(RE_ADDRESS, RE_ZEROMSB_REG, 0x00)
    bus.write_byte_data(RE_ADDRESS, RE_ZEROLSB_REG, 0x00)
    ANG_M = bus.read_byte_data(RE_ADDRESS, RE_ANGLEMSB_REG)
    ANG_L = bus.read_byte_data(RE_ADDRESS, RE_ANGLELSB_REG)
    bus.write_byte_data(RE_ADDRESS, RE_ZEROMSB_REG, ANG_M)
    bus.write_byte_data(RE_ADDRESS, RE_ZEROLSB_REG, ANG_L)

# polling
while True:
    startTime = time.time()
    ANG_M1 = bus.read_byte_data(0x40, RE_ANGLEMSB_REG)
    ANG_L1 = bus.read_byte_data(0x40, RE_ANGLELSB_REG)
    # bit shifting to access 14-bit value. Docs p. 25
    ANG1 = (ANG_M1 << 6)+(ANG_L1 & 0x3f) 
    ANG1 = ANG1 * 360.0 / 16384.0
    
    MAG_M1 = bus.read_byte_data(0x40, RE_MAGNMSB_REG)
    MAG_L1 = bus.read_byte_data(0x40, RE_MAGNLSB_REG)
    # bit shifting to access 14-bit value. Docs p. 25
    MAG1 = (MAG_M1 << 6)+(MAG_L1 & 0x3f) 

    print("Angle: %7f Magnitude: %7d" %(ANG1, MAG1))
    #print("Time taken: " + str(time.time()-startTime))
    
    time.sleep(0.1)
