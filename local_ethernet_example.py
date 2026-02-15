from lib.eth_node import eth_cbus_node
# import socket
import asyncio

def process_message(msg):
    print(f'Ethernet Node -  Process Message: {msg}')
    for event in msg['info']:
        local_node.acon(event) if msg['status'] == 'on' else local_node.acof(event)

#cbus_header = ':SB060N'
local_node = eth_cbus_node(600, process_message, "localhost", 5550)

# cbus_ethernet.start()
#local_node.send(f'{cbus_header}0D;')
local_node.teach_long_event(300, 9, [1,10])
local_node.pnn()
local_node.acon(1)

#Create Event Loop and add Tasks
loop = asyncio.new_event_loop()

loop.create_task(local_node.run())
# loop.create_task(node.print_details())

loop.run_forever()