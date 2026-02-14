# Example for the MERG pico_02_2515
# This example sends an event for each number in an Array.

from lib.can_pico_2515 import pico_02_2515
import asyncio
import time
from pico_widgets import PicoLed, PicoInput

# Function which runs when a taught event has been received
def process_message(msg):
    print(f'Message Processed {msg} {msg['status']} {msg['op']}')
    for event in msg['info']:
        node.acon(event) if msg['status'] == 'on' else node.acof(event)
    
# Functions that are actioned when the button is pressed and released.    
def button_on():
    print(f'Button On')
    node.acon(1)
    amber_led.on = True
    
def button_off():
    print(f'Button Off')
    node.acof(1)
    amber_led.on = False
    
# Setup the onboard button
button = PicoInput(22, button_on, button_off)

# Setup the on board LEDs
green_led = PicoLed(9)
amber_led = PicoLed(15)
amber_led.on = False
red_led = PicoLed(8)
red_led.flash = True

#Setup the Cbus Modules
node = pico_02_2515(200, process_message)

# Teach Event to Node
node.teach_long_event(300, 9, [1,3])

# Send Cbus Messages for FCU and MMC
node.pnn()
node.acon(1)

#Create Event Loop and add Tasks
loop = asyncio.get_event_loop()

loop.create_task(button.check())
loop.create_task(green_led.check())
loop.create_task(amber_led.check())
loop.create_task(red_led.check())
loop.create_task(node.run())
# loop.create_task(node.print_details())

loop.run_forever()
