import gpiod

def TurnOnLED(PIN):
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(1)
    led_line.release()
    
    
def TurnOffLED(PIN):
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(0)
    led_line.release()
    
def SetVoltage(PIN, value):
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(value)
    led_line.release()