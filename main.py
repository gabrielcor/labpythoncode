from m5stack import *
from m5ui import *
from uiflow import *

setScreenColor(0x111111)

label = M5TextBox(20, 100, "Press A to start hintclient", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)

client_started = False

def check_button(timer):
    global client_started
    if btnA.isPressed() and not client_started:
        client_started = True
        label.setText("Starting...")
        timer.deinit()  # 🛑 stop the timer
        wait_ms(500)
        exec(open('hintclient.py').read())

# Start a timer that checks every 1000ms for button press
timer = machine.Timer(-1)
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=check_button)
