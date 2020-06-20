# =========================================================
# Seeed Studio Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
#
# Modified from the sample code on the Seeed Studio Wiki
# http://wiki.seeed.cc/Raspberry_Pi_Relay_Board_v1.0/
# =========================================================
# TODO: Implement logging for configurable output

import smbus

# This value should never change since Seeed only makes 4 port boards,
# but I made it a constructor option anyway
# The number of relay ports on the relay board.
# NUM_RELAY_PORTS = 4

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


class Relay():
    global bus

    def __init__(self, device_address=0x20, num_relays=4):
        print('Initializing relay board at {}'.format(device_address))
        self.DEVICE_ADDRESS = device_address
        self.NUM_RELAY_PORTS = num_relays
        self.DEVICE_REG_MODE1 = 0x06
        self.DEVICE_REG_DATA = 0xff
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def on(self, relay_num, debug=False):
        if isinstance(relay_num, int):
            # do we have a valid relay number?
            if 0 < relay_num <= self.NUM_RELAY_PORTS:
                if debug:
                    print('Turning relay {} on'.format(relay_num))
                self.DEVICE_REG_DATA &= ~(0x1 << (relay_num - 1))
                bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)
            else:
                print('Invalid relay: #{}'.format(relay_num))
        else:
            print('Relay number must be an Integer value')

    def off(self, relay_num, debug=False):
        if isinstance(relay_num, int):
            # do we have a valid relay number?
            if 0 < relay_num <= self.NUM_RELAY_PORTS:
                if debug:
                    print('Turning relay {} off'.format(relay_num))
                self.DEVICE_REG_DATA |= (0x1 << (relay_num - 1))
                bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)
            else:
                print('Invalid relay: #{}'.format(relay_num))
        else:
            print('Relay number must be an Integer value')

    def all_on(self, debug=False):
        if debug:
            print('Turning all relays ON')
        self.DEVICE_REG_DATA &= ~(0xf << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def all_off(self, debug=False):
        if debug:
            print('Turning all relays OFF')
        self.DEVICE_REG_DATA |= (0xf << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def toggle_port(self, relay_num, debug=False):
        if debug:
            print('Toggling relay:', relay_num)
        if self.get_port_status(relay_num):
            # it's on, so turn it off
            self.off(relay_num)
        else:
            # it's off, so turn it on
            self.on(relay_num)

    def get_port_status(self, relay_num, debug=False):
        # determines whether the specified port is ON/OFF
        if debug:
            print('Checking status of relay {}'.format(relay_num))
        res = self.get_port_data(relay_num)
        if res > 0:
            mask = 1 << (relay_num - 1)
            # return the specified bit status
            # return (DEVICE_REG_DATA & mask) != 0
            return (self.DEVICE_REG_DATA & mask) == 0
        else:
            # otherwise (invalid port), always return False
            print("Relay port ({}) is invalid".format(relay_num))
            return False

    def get_port_data(self, relay_num, debug=False):
        # gets the current byte value stored in the relay board
        if debug:
            print('Reading relay status value for relay {}'.format(relay_num))
        # do we have a valid port?
        if 0 < relay_num <= self.NUM_RELAY_PORTS:
            # read the memory location
            self.DEVICE_REG_DATA = bus.read_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1)
            # return the specified bit status
            return self.DEVICE_REG_DATA
        else:
            # otherwise (invalid port), always return 0
            print("Specified relay port is invalid")
            return 0

    def print_status_all(self):
        output = "| "
        for x in range(1, self.NUM_RELAY_PORTS+1):
            status = self.get_port_status(x)
            output += str(x)
            if status:
                output += ': On  | '
            else:
                output += ': Off | '
        print('Relay status: {}'.format(output))

    def print_status(self, relay_num):
        output = str(relay_num)
        status = self.get_port_status(relay_num)
        if status:
            output += ': On  '
        else:
            output += ': Off '
        print('Relay {}'.format(output))
