#!/usr/bin/python
'''*****************************************************************************************************************
    Seeed Studio Relay Board Example
    By John M. Wargo
    www.johnwargo.com
********************************************************************************************************************'''

import sys
import time

from relay_lib_seeed import Relay


def process_loop():
    # turn all of the relays on
    relay.relay_all_on()
    # wait a second
    time.sleep(1)
    # turn all of the relays off
    relay.relay_all_off()
    # wait a second
    time.sleep(1)

    # now cycle each relay every second in an infinite loop
    while True:
        for i in range(1, 5):
            relay.relay_on(i)
            time.sleep(1)
            relay.relay_off(i)


# Now see what we're supposed to do next
if __name__ == "__main__":
    # Create the relay object
    relay = Relay()

    try:
        process_loop()
    except KeyboardInterrupt:
        print("\nExiting application")
        # turn off all of the relays
        relay.relay_all_off()
        # exit the application
        sys.exit(0)
