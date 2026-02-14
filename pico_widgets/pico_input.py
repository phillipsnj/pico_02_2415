from machine import Pin
# import time
import asyncio

class PicoInput():
    def __init__(self, pin, on_function, off_function):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.button_status = self.button.value()
        self.sleep_duration = 50
        self.on_function = on_function
        self.off_function = off_function
        
    async def check(self):
        print('Check Button '+str(self.button.value()))
        while True:
            # print(f'Check Button {self.button_status} {str(self.button.value())}')
            if self.button_status != self.button.value():
                print(f'Button Changed : {str(self.button.value())}')
                if self.button.value() == 0:
                    if self.on_function != None:
                       self.on_function() 
                else:
                    if self.off_function != None:
                        self.off_function()
                self.button_status = self.button.value()
            await asyncio.sleep_ms(self.sleep_duration)
#        tim = Timer(period=self.duration, mode=Timer.ONE_SHOT, callback = self.check)