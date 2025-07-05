'''
Core RGB-Color-Pick example base on LVGL.
Copyright (c) 2020 M5Stack
'''
from m5stack_ui import M5Screen, M5Cpicker, M5Label, EVENT_VALUE_CHANGED, ALIGN_IN_TOP_MID, FONT_MONT_18

scr = M5Screen()
scr.clean_screen()
scr.set_screen_bg_color(0xe1e1e1)
cpicker = M5Cpicker(w=180, h=180)
cpicker.set_align(ALIGN_IN_TOP_MID, x=0, y=15)

red_label = M5Label("Red:", font=FONT_MONT_18)
red_label.set_align(4)
red_label.set_text_color(0xff0000)
green_label = M5Label("Green:", font=FONT_MONT_18)
green_label.set_align(5, x=-30, y=0)
green_label.set_text_color(0x00ff00)
blue_label = M5Label("Blue:", font=FONT_MONT_18)
blue_label.set_align(6, x=-50, y=0)
blue_label.set_text_color(0x0000ff)

def cpicker_event_cb(obj, event):
    if event == EVENT_VALUE_CHANGED:
        color = obj.get_color()
        red = color.ch.red
        green = (color.ch.green_h << 3) + color.ch.green_l
        blue = color.ch.blue
        red_label.set_text("Red: %#X" % red)
        green_label.set_text("Green: %#X" % green)
        blue_label.set_text("Blue: %#X" % blue)

cpicker.set_cb(cpicker_event_cb)
