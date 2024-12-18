import gpiod
LED_PIN = 17

def TurnOnLED():
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(LED_PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(1)
    led_line.release()
    
def TurnOffLED():
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(LED_PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(0)
    led_line.release()