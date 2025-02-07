from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time

BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)  # DIO0 for RX done

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = bytes(payload).decode('utf-8', errors='ignore')
        print(f"Received: {data}")
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            time.sleep(0.5)

# LoRa Configuration (Match these settings with your ESP32 transmitter!)
lora = LoRaReceiver(verbose=False)
lora.set_freq(915.0)  # Set frequency to 915MHz (adjust as needed)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(12)         # Spreading Factor (SF7-SF12)
lora.set_bandwidth(125e3)            # Bandwidth: 125 kHz
lora.set_coding_rate(5)              # Coding Rate: 4/5
lora.set_preamble_length(8)          # Preamble Length
lora.set_sync_word(0x12)             # Sync Word (must match transmitter)
lora.set_rx_crc(True)                # Enable CRC

try:
    print("Starting LoRa Receiver...")
    lora.start()
except KeyboardInterrupt:
    print("\nExiting...")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
