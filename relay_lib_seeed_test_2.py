#!/usr/bin/python
'''*****************************************************************************************************************
    Seeed Studio Relay Board Library V2
    Test Application #2
    By John M. Wargo (https://www.johnwargo.com)
********************************************************************************************************************'''

import sys
import time

from seeed_relay_v1 import Relay


def process_loop():
    # turn all of the relays on
    relay.all_on()
    relay.print_status_all()
    # wait a second
    time.sleep(1)
    # turn all of the relays off
    relay.all_off()
    relay.print_status_all()
    # wait a second
    time.sleep(1)

    # now cycle each relay every second in an infinite loop
    while True:
        # test the on/off methods
        print('Testing on/off methods')
        for i in range(1, 5):
            relay.on(i)
            relay.print_status_all()
            time.sleep(1)
            relay.off(i)
            relay.print_status_all()
            time.sleep(1)

        # test the toggle method
        print('Testing the toggle methods')
        for i in range(1, 5):
            relay.toggle_port(i)
            relay.print_status_all()
            time.sleep(1)
            relay.toggle_port(i)
            relay.print_status_all()
            time.sleep(1)

        print('Repeating loop')


# Now see what we're supposed to do next
if __name__ == "__main__":
    # Create the relay object
    relay = Relay()

    try:
        process_loop()
    except KeyboardInterrupt:
        print("\nExiting application")
        # turn off all of the relays
        relay.all_off()
        # exit the application
        sys.exit(0)
