import asyncio
import platform
if platform.system() == "Windows":
    from utils import led_controller_fake as led
else:
    from utils import gpio_controller as led

FRWARD_PIN = 17
RIGHT_PIN = 27
LEFT_PIN = 22

current_angle = 0
time_to_full_angle = 0.22

# here we control the steernig
# we give High to the pin we want to turn until we reach the desired angle then we give low to all pins untill they reach the 0 angle

# async left
async def left():
    global current_angle
    print("left")
    led.SetVoltage(FRWARD_PIN, 0)
    led.SetVoltage(RIGHT_PIN, 0)
    led.SetVoltage(LEFT_PIN, 1)
    if current_angle == -1:
        await asyncio.sleep(time_to_full_angle * 2)
    else:
        await asyncio.sleep(time_to_full_angle)
    current_angle = 1
    led.SetVoltage(LEFT_PIN, 0)
    
# async right
async def right():
    global current_angle
    print("right")
    led.SetVoltage(FRWARD_PIN, 0)
    led.SetVoltage(LEFT_PIN, 0)
    led.SetVoltage(RIGHT_PIN, 1)
    if current_angle == 1:
        await asyncio.sleep(time_to_full_angle * 2)
    else:
        await asyncio.sleep(time_to_full_angle)
    current_angle = -1
    led.SetVoltage(RIGHT_PIN, 0)
    
async def forward():
    # turn the wheels to the forward position
    global current_angle
    print("forward")
    led.SetVoltage(RIGHT_PIN, 0)
    led.SetVoltage(LEFT_PIN, 0)
    
    if current_angle == -1:
        led.SetVoltage(LEFT_PIN, 1)
        await asyncio.sleep(time_to_full_angle)
        led.SetVoltage(LEFT_PIN, 0)
    elif current_angle == 1:
        led.SetVoltage(RIGHT_PIN, 1)
        await asyncio.sleep(time_to_full_angle)
        led.SetVoltage(RIGHT_PIN, 0)
    current_angle = 0
    led.SetVoltage(FRWARD_PIN, 1)

def reset():
    global current_angle
    led.SetVoltage(FRWARD_PIN, 0)
    led.SetVoltage(RIGHT_PIN, 0)
    led.SetVoltage(LEFT_PIN, 0)
    current_angle = 0
    
# if main show a control panel
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.title("Car Controller")
    root.geometry("200x200")
    
    forward_button = tk.Button(root, text="Forward", command=lambda: asyncio.run(forward()))
    forward_button.pack()
    
    left_button = tk.Button(root, text="Left", command=lambda: asyncio.run(left()))
    left_button.pack()
    
    right_button = tk.Button(root, text="Right", command=lambda: asyncio.run(right()))
    right_button.pack()
    
    reset_button = tk.Button(root, text="Reset", command=reset)
    reset_button.pack()
    
    root.mainloop()