# This is an example of using the base CBUS class on your PC.
# Requires a Cbus network connection on the same PC

from lib.eth_node import eth_cbus_node
import asyncio

def process_message(msg):
    print(f'Ethernet Node -  Process Message: {msg}')
    for event in msg['info']:
        local_node.acon(event) if msg['status'] == 'on' else local_node.acof(event)

local_node = eth_cbus_node(600, process_message, "localhost", 5550)

local_node.teach_long_event(300, 9, [1,10])
local_node.pnn()
local_node.acon(1)

#Create Event Loop and add Tasks
loop = asyncio.new_event_loop()

loop.create_task(local_node.run())

loop.run_forever()