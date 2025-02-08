from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time
import binascii

BOARD.setup()

class LoRaWANReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaWANReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)  # DIO0 for RX done

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = bytes(payload)
        dev_addr = data[:4]  # Extract DevAddr (first 4 bytes)
        message = data[4:].decode('utf-8', errors='ignore')

        print(f"Received from {binascii.hexlify(dev_addr).decode('utf-8')}: {message}")
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            time.sleep(0.5)

# LoRa Configuration (Match these settings with your ESP32 transmitter!)
lora = LoRaWANReceiver(verbose=False)
lora.set_freq(433.0)  # Set frequency to 433 MHz for RA-02
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(12)         # Spreading Factor (SF7-SF12)
lora.set_bandwidth(125e3)            # Bandwidth: 125 kHz
lora.set_coding_rate(5)              # Coding Rate: 4/5
lora.set_preamble_length(8)          # Preamble Length
lora.set_sync_word(0x34)             # Sync Word for LoRaWAN
lora.set_rx_crc(True)                # Enable CRC

try:
    print("Starting LoRaWAN Receiver...")
    lora.start()
except KeyboardInterrupt:
    print("\nExiting...")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
