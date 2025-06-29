import os, sys, io
import M5
from M5 import *



label0 = None


def setup():
  global label0

  M5.begin()
  Widgets.fillScreen(0xffffff)
  label0 = Widgets.Label("Hola que tal", 51, 71, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)



def loop():
  global label0
  M5.update()


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
