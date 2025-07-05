from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
from m5mqtt import M5mqtt


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


topic_output = None
hrs = None
mins = None
secs = None
message_code = None
total_seconds = None
timetoshow = None
tempvar = None



image0 = M5Img("res/Background_Inicial_v0.2-min.png", x=0, y=0, parent=None)
label0 = M5Label('123456789012345678901234567', x=12, y=118, color=0x2d672c, font=FONT_MONT_18, parent=None)
labelsi = M5Label('SI', x=45, y=202, color=0x000, font=FONT_MONT_18, parent=None)
labelno = M5Label('NO', x=248, y=202, color=0x000, font=FONT_MONT_18, parent=None)
btnsi = M5Btn(text='o', x=49, y=229, w=10, h=10, bg_c=0xd81d1d, text_c=0xd81d1d, font=FONT_MONT_14, parent=None)
btnno = M5Btn(text='o', x=258, y=229, w=10, h=10, bg_c=0xd81d1d, text_c=0xd81d1d, font=FONT_MONT_14, parent=None)
btn_question = M5Btn(text='?', x=237, y=34, w=40, h=40, bg_c=0x76501c, text_c=0xe8b844, font=FONT_MONT_30, parent=None)
label_time = M5Label('0:00:00', x=25, y=46, color=0x3ba0ab, font=FONT_MONT_18, parent=None)



def btn_question_pressed():
  global topic_output, hrs, mins, secs, message_code, total_seconds, timetoshow, tempvar
  btn_question.set_hidden(True)
  m5mqtt.publish(str('rllabdevicesend'), str('btnQ'), 0)
  pass
btn_question.pressed(btn_question_pressed)

def fun_rllabdevice_(topic_data):
  global topic_output, hrs, mins, secs, message_code, total_seconds, timetoshow, tempvar
  topic_output = topic_data
  message_code = topic_output[0] + topic_output[1]
  print(message_code)
  if message_code=='00':
    label0.set_hidden(True)
    image0.set_img_src("res/Background_Inicial_v0.2-min.png")
    labelsi.set_hidden(True)
    labelno.set_hidden(True)
    btnsi.set_hidden(True)
    btnno.set_hidden(True)
    btn_question.set_hidden(True)
  elif message_code=='01':
    power.setVibrationEnable(True)
    wait_ms(1500)
    power.setVibrationEnable(False)
  elif message_code=='02':
    speaker.playTone(784, 1, volume=5)
  elif message_code=='03':
    speaker.playTone(784, 1, volume=5)
  elif message_code=='04':
    labelsi.set_hidden(False)
    labelno.set_hidden(False)
    btnsi.set_hidden(False)
    btnno.set_hidden(False)
  elif message_code=='05':
    labelsi.set_hidden(True)
    labelno.set_hidden(True)
    btnsi.set_hidden(True)
    btnno.set_hidden(True)
  elif message_code=='10':
    btn_question.set_hidden(False)
  elif message_code=='11':
    btn_question.set_hidden(True)
  elif message_code=='08':
    micropython.mem_info()
  elif message_code=='91':
    pass
  else:
    label0.set_text(str(topic_output))
    image0.set_img_src("res/Background_withLet-min-v0.2.png")
    label0.set_hidden(False)
    print(topic_output)
  pass

def buttonA_wasPressed():
  global topic_output, hrs, mins, secs, message_code, total_seconds, timetoshow, tempvar
  m5mqtt.publish(str('rllabdevicesend'), str('btnA'), 0)
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global topic_output, hrs, mins, secs, message_code, total_seconds, timetoshow, tempvar
  m5mqtt.publish(str('rllabdevicesend'), str('btnB'), 0)
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global topic_output, hrs, mins, secs, message_code, total_seconds, timetoshow, tempvar
  m5mqtt.publish(str('rllabdevicesend'), str('btnC'), 0)
  pass
btnC.wasPressed(buttonC_wasPressed)

@timerSch.event('timer0')
def ttimer0():
  global topic_output, hrs, mins, secs, message_code, total_seconds, timetoshow, tempvar
  hrs = int((total_seconds / 3600))
  mins = int(((total_seconds % 3600) / 60))
  secs = total_seconds % 60
  timetoshow = (str(((str(hrs) + str(mins)))) + str(secs))
  tempvar = formattime(hrs,mins,secs)

  label_time.set_text(str(tempvar))
  total_seconds = total_seconds - 1
  gc.collect()
  pass


import gc
label0.set_hidden(True)
timerSch.run('timer0', 1000, 0x00)
def formattime(hrs,mins,secs):
  temp = "{:00}:{:02}:{:02}".format(int(hrs), mins, secs)
  return temp

label0.set_long_mode(1)
total_seconds = 3600
power.setVibrationEnable(False)
power.setVibrationIntensity(50)
labelsi.set_hidden(True)
labelno.set_hidden(True)
btnsi.set_hidden(True)
btnno.set_hidden(True)
btn_question.set_hidden(True)
m5mqtt = M5mqtt('RLLabDevice', '192.168.70.113', 1883, 'mqttuser', 'A1234567#', 300)
m5mqtt.subscribe(str('rllabdevice'), fun_rllabdevice_)
m5mqtt.start()
