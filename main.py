from m5stack import *
from m5stack_ui import *
from m5ui import *
from uiflow import *

import network
import machine

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xffffff)        

setScreenColor(0x111111)

# Get device MAC and determine name
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

mac = wlan.config('mac')
mac_str = ':'.join('{:02X}'.format(b) for b in mac)

device_name = 'Main' if mac_str == '2C:BC:BB:82:92:F0' else 'Mirror'

# Create a button that shows device_name

btn = M5Btn(text=device_name, x=60, y=100, w=200, h=80,
            bg_c=0x222222, text_c=0xFFFFFF, font=FONT_MONT_14, parent=None)

client_started = False

# Button press handler
def on_btn_pressed():
    global client_started
    if not client_started:
        client_started = True
        speaker.playTone(220, 1/8, volume=6)
        speaker.playTone(110, 1/8, volume=6)
        btn.set_hidden(True)

        screen = M5Screen()
        screen.clean_screen()
        screen.set_screen_bg_color(0xffffff)        
        wait_ms(500)
        exec(open('hintclient.py').read())

# Bind the event
btn.pressed(on_btn_pressed)
