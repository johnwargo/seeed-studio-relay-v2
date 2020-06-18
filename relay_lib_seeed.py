# =========================================================
# Seeed Studio Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
#
# Modified from the sample code on the Seeed Studio Wiki
# http://wiki.seeed.cc/Raspberry_Pi_Relay_Board_v1.0/
# =========================================================

# from __future__ import print_function

import smbus

# The number of relay ports on the relay board.
# This value should never change since Seed only makes 4 port boards
NUM_RELAY_PORTS = 4

# # Change the following value if your Relay board uses a different I2C address.
# DEVICE_ADDRESS = 0x20  # 7 bit address (will be left shifted to add the read write bit)
# # Don't change the values, there's no need for that.
# DEVICE_REG_MODE1 = 0x06
# DEVICE_REG_DATA = 0xff

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


class Relay():
    global bus

    def __init__(self, device_address=0x20):
        self.DEVICE_ADDRESS = device_address
        self.DEVICE_REG_MODE1 = 0x06
        self.DEVICE_REG_DATA = 0xff
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def relay_on(self, relay_num):
        if isinstance(relay_num, int):
            # do we have a valid relay number?
            if 0 < relay_num <= NUM_RELAY_PORTS:
                print('Turning relay {} on'.format(relay_num))
                self.DEVICE_REG_DATA &= ~(0x1 << (relay_num - 1))
                bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)
            else:
                print('Invalid relay #:{}'.format(relay_num))
        else:
            print('Relay number must be an Integer value')

    def relay_off(self, relay_num):
        if isinstance(relay_num, int):
            # do we have a valid relay number?
            if 0 < relay_num <= NUM_RELAY_PORTS:
                print('Turning relay {} off'.format(relay_num))
                self.DEVICE_REG_DATA |= (0x1 << (relay_num - 1))
                bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)
            else:
                print('Invalid relay #:{}'.format(relay_num))
        else:
            print('Relay number must be an Integer value')

    def relay_all_on(self):
        print('Turning all relays ON')
        self.DEVICE_REG_DATA &= ~(0xf << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def relay_all_off(self):
        print('Turning all relays OFF')
        self.DEVICE_REG_DATA |= (0xf << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def relay_toggle_port(self, relay_num):
        print('Toggling relay:', relay_num)
        if self.relay_get_port_status(relay_num):
            # it's on, so turn it off
            self.relay_off(relay_num)
        else:
            # it's off, so turn it on
            self.relay_on(relay_num)

    def relay_get_port_status(self, relay_num):
        # determines whether the specified port is ON/OFF
        print('Checking status of relay {}'.format(relay_num))
        res = self.relay_get_port_data(relay_num)
        if res > 0:
            mask = 1 << (relay_num - 1)
            # return the specified bit status
            # return (DEVICE_REG_DATA & mask) != 0
            return (self.DEVICE_REG_DATA & mask) == 0
        else:
            # otherwise (invalid port), always return False
            print("Specified relay port is invalid")
            return False

    def relay_get_port_data(self, relay_num):
        # gets the current byte value stored in the relay board
        print('Reading relay status value for relay {}'.format(relay_num))
        # do we have a valid port?
        if 0 < relay_num <= NUM_RELAY_PORTS:
            # read the memory location
            self.DEVICE_REG_DATA = bus.read_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1)
            # return the specified bit status
            return self.DEVICE_REG_DATA
        else:
            # otherwise (invalid port), always return 0
            print("Specified relay port is invalid")
            return 0
