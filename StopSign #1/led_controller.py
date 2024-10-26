import gpiod
LED_PIN = 17

last_state = 0

def TurnOnLED():
    if last_state == 1:
        return
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(LED_PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(1)
    led_line.release()
    last_state = 1
    
def TurnOffLED():
    if last_state == 0:
        return
    chip = gpiod.Chip('gpiochip4')
    led_line = chip.get_line(LED_PIN)
    led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    led_line.set_value(0)
    led_line.release()
    last_state = 0