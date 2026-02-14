class CbusNode:
    def __init__(self, node_number, function):
        
        self.nodeId = node_number
        self.function = function
        self.debug = False
        self.events = {}
        self.count = 0
        self.canId = 75
        self.priority1 = 2
        self.priority2 = 3
        self.learn = False
        self.interface = 2  # 1 can, 2 ethernet
        self.manufId = 165
        self.moduleId = 58
        self.name = "CANPiNODE"
        self.minorVersion = "A"
        self.numEvents = 0
        self.numEventVariables = 0
        self.numNodeVariables = 0
        self.majorVersion = 1
        self.beta = 1  # 0  for normal version else beta version number
        self.consumer = False
        self.producer = True
        self.flim = False
        self.bootloader = False
        self.coe = False
        self.intOut = 0
        self.chrOut = ""

        self.parameters = []
        self.parameters.append(self.pad(9, 2))
        self.parameters.append(self.pad(self.manufId, 2))
        self.parameters.append(self.pad(ord(self.minorVersion), 2))
        self.parameters.append(self.pad(self.moduleId, 2))
        self.parameters.append(self.pad(self.numEvents, 2))
        self.parameters.append(self.pad(self.numEventVariables, 2))
        self.parameters.append(self.pad(self.numNodeVariables, 2))
        self.parameters.append(self.pad(self.majorVersion, 2))
        self.parameters.append(self.pad(self.flags(), 2))
        self.parameters.append(self.pad(0, 2))

        self.actions = {
            "90": self.accessory_long_on,
            "91": self.accessory_long_off,
            "98": self.accessory_short_on,
            "99": self.accessory_short_off,
            "73": self.send_parameter,
            "0D": self.query_node_number,
#            "10": self.params,
            }

    @staticmethod
    def pad(num, length):
        output = '0000000000' + hex(num)[2:]
        return output[length * -1:]

    @staticmethod
    def get_int(msg, start, length):
        return int(msg[start: start + length], 16)

    @staticmethod
    def get_str(msg, start, length):
        return msg[start: start + length]
    
    def get_op_code(self, msg):
        return self.get_str(msg, 7, 2)

    def get_node_id(self, msg):
        return int(self.get_str(msg, 9, 4), 16)
    
    def get_event_identifier(self, msg):
        return self.get_str(msg, 9, 8)

    def get_header(self):
        output = 0
        output = output + self.priority1
        output = output << 2
        output = output + self.priority2
        output = output << 7
        output = output + self.canId
        output = output << 5
        # print(str(output))
        # return str(output)
        # print (":S"+format(output, '02x')+"N")
        # return ":S"+format(output, '02x')+"N"
        return ":S" + hex(output)[2:] + "N"
        # return ":SB020N"

    def flags(self):
        flags = 0
        if self.consumer:
            flags += 1
        if self.producer:
            flags += 2
        if self.flim:
            flags += 4
        if self.bootloader:
            flags += 8
        if self.coe:
            flags += 16
        if self.learn:
            flags += 32
        return flags
    
    def query_node_number(self, msg):
        if self.debug:
            print("qnn received: " + msg)
        self.pnn()

    def pnn(self):
        flags = 0
        if self.consumer:
            flags += 1
        if self.producer:
            flags += 2
        if self.flim:
            flags += 4
        if self.bootloader:
            flags += 8
        if self.coe:
            flags += 16
        output = self.get_header() + "B6" + self.pad(self.nodeId, 4) + self.pad(self.manufId, 2) + self.pad(
            self.moduleId, 2) + self.pad(self.flags(), 2) + ";"
        self.send(output)
    
    def acon(self, event_id):
        """
        Sends a Accessory On Long Event to the CBUS Network
        :param event_id: Id for the event
        """
        output = self.get_header() + "90" + self.pad(self.nodeId, 4) + self.pad(event_id, 4) + ";"
        self.send(output)
    
    def acof(self, event_id):
        """
        Sends a Accessory Off Long Event to the CBUS Network
        :param event_id: Id for the event
        """
        output = self.get_header() + "91" + self.pad(self.nodeId, 4) + self.pad(event_id, 4) + ";"
        self.send(output)

    def ason(self, event_id):
        """
        Sends a Accessory On Short Event to the CBUS Network
        :param event_id: Id for the event
        """
        output = self.get_header() + "98" + self.pad(self.nodeId, 4) + self.pad(event_id, 4) + ";"
        self.send(output)
    
    def asof(self, event_id):
        """
        Sends a Accessory Off Short Event to the CBUS Network
        :param event_id: Id for the event
        """
        output = self.get_header() + "99" + self.pad(self.nodeId, 4) + self.pad(event_id, 4) + ";"
        self.send(output)
    
    def paran(self, param):
        print(f'Cbus Slim Node paran :{param} {len(self.parameters)}')
        if param < len(self.parameters):
            if self.debug:
                print("parameter : " + str(self.nodeId) + " : " + str(param) + " : " + str(self.parameters[param]))
            output = self.get_header() + "9B" + self.pad(self.nodeId, 4) + self.pad(param, 2) + self.parameters[param] + ";"
            if self.debug:
                print("parameter output : " + output)
            self.send(output)
        else:
            print(f'Cbus Slim Node paran Error:{param} {len(self.parameters)}')
            
    def event_message(self, operation, status, info, data):
        output = {}
        output['op'] = operation
        output['status'] = status
        output['info'] = info
        output['data'] = data
        return output

    def accessory_long_on(self, msg):
        event_identifier = self.get_event_identifier(msg)
        if self.get_event_identifier(msg) in self.events:
            print(f'Cbus slim Node Taught Event : {self.get_event_identifier(msg)}')
            if self.debug:
                print(f'accessory_long_on {msg} Output: {self.event_message('ACON', 'on', 'Event_information', [])}')
            self.function(self.event_message('ACON', 'on',  self.events[event_identifier], []))

    def accessory_long_off(self, msg):
        event_identifier = self.get_event_identifier(msg)
        if event_identifier in self.events:
            print(f'Cbus slim Node Taught Event : {self.get_event_identifier(msg)}')
            if self.debug:
                print(f'accessory_long_on {msg} Output: {self.event_message('ACOF', 'on', 'Event_information', [])}')
            self.function(self.event_message('ACOF', 'off', self.events[event_identifier], []))

    def accessory_short_on(self, msg):
        print(f'accessory_short_on {msg}')

    def accessory_short_off(self, msg):
        print(f'accessory_short_off {msg}')

    def send_parameter(self, msg):
        param = int(self.get_str(msg, 13, 2), 16)
        self.paran(param)

    def teach_long_event(self, node_id, event_id, variables):
        """
        Teaches a long CBUS event to the module
        :param node_id: node id of the event
        :param event_id: event od of the event
        :param variables: Variable that will be sent to the function when event
                is received. Can be String, number, list etc
        """
        new_id = self.pad(node_id, 4) + self.pad(event_id, 4)
        self.events[new_id.upper()] = variables
        print(f'Short Event Taught - Event Identifier : {new_id.upper()} Node: {node_id} Event: {event_id} with {variables}')

    def teach_short_event(self, event_id, variables):
        """
        Teaches a short CBUS event to the module
        :param event_id: event of the short event
        :param variables: Variable that will be sent to the function when event
               is received. Can be String, number, list etc
        """
        new_id = self.pad(0, 4) + self.pad(event_id, 4)
        self.events[new_id] = variables
        if self.debug:
            print(f'Short Event Taught {event_id} with {variables}')

    def action_opcode(self, msg):

        opcode = self.get_op_code(msg)
        if self.debug:
            print("Opcode : " + opcode)
        self.count += 1
        if self.debug:
            print("Msg Count" + str(self.count))
        if opcode in self.actions:
            if self.debug:
                print("Processing Opcode : " + opcode)
            func = self.actions[opcode]
            func(msg)
        else:
            if self.debug:
                print("Unknown Opcode : " + opcode)
            # self.Function(msg)
    
    def execute(self, msg):
        # self.Function(msg)
        if self.debug:
            print("Execute MSG : " + msg)
        self.action_opcode(msg)

    def send(self, message):
        print(f'Send Message {message}')