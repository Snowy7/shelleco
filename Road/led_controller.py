import gpiod
RIGHT_LED_PIN = 22
LEFT_LED_PIN = 17
STOP_LED_PIN = 27

def TurnOnLED(PIN):
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(1)
    led_line.release()
    last_state = 1
    
def TurnOffLED(PIN):
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(0)
    led_line.release()
    last_state = 0