#!/usr/bin/env python3
import time
import PyLora

def main():
    # Initialize the LoRa module.
    # The init() function sets up SPI and configures the GPIOs as per the default pin mapping.
    PyLora.init()

    # Set the operating frequency in Hz (e.g., 915 MHz -> 915000000).
    PyLora.set_frequency(915000000)

    # Enable CRC checking (recommended for reliable packet detection).
    PyLora.enable_crc()

    print("LoRa receiver initialized and set to 915 MHz. Waiting for packets...")

    try:
        while True:
            # Put the module in receive mode.
            PyLora.receive()

            # Wait until a packet is available.
            while not PyLora.packet_available():
                time.sleep(0.01)

            # Retrieve the received packet.
            packet = PyLora.receive_packet()
            print("Packet received: {}".format(packet))

    except KeyboardInterrupt:
        print("Receiver stopped by user.")

if __name__ == "__main__":
    main()
