from machine import Pin, SPI
import time
from cbus_slim_node import CbusNode
from lib.cbus2515 import Cbus2515
import asyncio

class pico_02_2515(CbusNode):
    def __init__(self, node_number, function):
        super().__init__(node_number, function)
        self.debug = False
        self.interface = 1  # 1 can, 2 ethernet

        # Setup the CAN Bus
        self.SPI_ID = 1
        self.SPI_CLK = Pin(10)
        self.SPI_MOSI = Pin(11)
        self.SPI_MISO = Pin(12)
        self.SPI_CS = Pin(13)
        self.SPI_INT = Pin(14)
        self.OSC_2515 = 16000000
        
        # self.spi = SPI(self.SPI_ID, sck=self.SPI_CLK, mosi=self.SPI_MOSI, miso=self.SPI_MISO)
        self.spi = SPI(self.SPI_ID, sck=self.SPI_CLK, mosi=self.SPI_MOSI, miso=self.SPI_MISO, baudrate=10000000)
        self.can = Cbus2515(self.spi, self.SPI_CS, self.SPI_INT, osc=self.OSC_2515, debug=self.debug)
        time.sleep(0.2)
        if self.debug:
            print("SPI Configuration: " + str(self.spi) + '\n')  # Display SPI config
            if self.can.initialised:
                print('CAN Initialised')
                print('CAN Id '+str(self.can.can_id))
            else:
                print('CAN NOT Initialised')
        self.can.change_mode(0)

    def send(self, msg):
        print("Pico Node Send - " + msg.upper())
        self.can.send(msg.upper())

    async def run(self):
        while True:
            while self.can.in_waiting():
                msg = self.can.receive()
                print(f'CAN {msg}')
                self.execute(msg)
                # print("Check")
            await asyncio.sleep_ms(100)
            #print(f'Running {self.can.monitor()}')
            
    async def print_details(self):
        while True:
            print(f'Running pico_02_2515 {self.can.in_waiting()}')
            await asyncio.sleep_ms(10000)
            
def process_message(msg):
    print(f'Message Processed {msg}')
            
async def main():


    node = pico_02_2515(200, process_message)

    node.can.change_mode(0)

    loop = asyncio.get_event_loop()

    loop.create_task(node.run())
    loop.create_task(node.print_details())
    loop.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    
    
