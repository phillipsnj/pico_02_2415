from cbus_slim_node import CbusNode
import socket
import asyncio

class eth_cbus_node(CbusNode):
    def __init__(self, node_number, function, host, port):
        super().__init__(node_number, function)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.host = host  # Get local machine name
        self.port = port  # Reserve a port for your service.
        self.s.connect((host, port))
        self.function = function

    async def run(self):
        print(f'Starting messages_from_server')
        while True:
            # print(f'Receive from Server Loop')
            try:
                # Receive messages from the server
                message = self.s.recv(1024).decode()
                # print(f'Receive Loop 2')
            except Exception as e:
                if e.args[0] in (35, 10035):
                    pass
                # If an error occurs, break out of the loop
                else:
                    print(f"Error {str(e)}")
                    break
            else:
                messages = message.split(';')
                del messages[-1]
  #              self.s.send(msg.encode())
                for msg in messages:
                    print(f'Ethernet Node - Message Received from Server: {msg};')
                    self.execute((msg + ';'))

            await asyncio.sleep(0.01)

    def send(self, msg):
        # time.sleep(1)
        # print("Child Send : " + msg)
        self.s.send(msg.encode())




async def main(name: str) -> None:

    def process_message(msg):
        print(f'Ethernet Node -  Process Message: {msg}')
        if msg['status'] == 'on':
            local_node.send(local_node.ason(1))
        else:
            local_node.send(local_node.asof(1))

    cbus_header = ':SB060N'
    local_node = eth_cbus_node(600, process_message, "localhost", 5550)
    asyncio.create_task(local_node.run())
    # cbus_ethernet.start()
    local_node.send(f'{cbus_header}0D;')
    local_node.teach_long_event(300, 9, [1])
    local_node.send(local_node.pnn())
    local_node.send(local_node.acon(1))
    while True:
        await asyncio.sleep(0.01)


if __name__ == '__main__':
    # main('network Client')
    asyncio.run(main('Slim Cbus Node'))