from machine import Pin, PWM
import time
import asyncio

class PicoLed():
    def __init__(self, led_pin):
        self.led = PWM(Pin(led_pin))
        self.led.freq(50)
        self.gamma = [0,256,768,2304,5120,9216,15616,23808,34560,47616,65535]
        #self.action_time = time.ticks_ms()
        self.on = True
        self.level = 10
        self.position(self.level)
        self.flash_frequency = 5
        self.flash_duration = 500
        self.sleep_duration = 50
        self.flash = False
        self.counter = 0
#        self.tim = Timer(period=self.flash_duration, mode=Timer.ONE_SHOT, callback = self.check)
        
    async def check(self):
        while True:
            if self.flash:
                # print(f'Pico_LED2 Check {self.counter} {self.sleep_duration}')
                self.counter += 1
                if self.counter > int(self.flash_duration/self.sleep_duration):
                    if self.on:
                        self.position(0)
                        self.on = False
                    else:
                        self.position(self.level)
                        self.on = True
                    self.counter = 0
            else:
                if self.on:
                    self.position(self.level)
                else:
                    self.position(0)
            await asyncio.sleep_ms(self.sleep_duration)
        
    def position(self, value):
        self.value = value
        if self.value > 10: self.value = 10
        if self.value <0 : self.value = 0
        self.led.duty_u16(self.gamma[self.value])