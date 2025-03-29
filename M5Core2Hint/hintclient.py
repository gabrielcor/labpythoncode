from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5mqtt import M5mqtt
import time, gc

# ─── UI SETUP ──────────────────────────────────────────────
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

# ─── UI ELEMENTS ────────────────────────────────────────────
image0 = M5Img("res/Background_Inicial_v0.2-min.png", x=0, y=0)

labelsi = M5Label('SI', x=45, y=202, color=0x000, font=FONT_MONT_18)
labelno = M5Label('NO', x=248, y=202, color=0x000, font=FONT_MONT_18)
btnsi = M5Btn(text='o', x=49, y=229, w=10, h=10, bg_c=0xd81d1d, text_c=0xd81d1d, font=FONT_MONT_14)
btnno = M5Btn(text='o', x=258, y=229, w=10, h=10, bg_c=0xd81d1d, text_c=0xd81d1d, font=FONT_MONT_14)
btn_question = M5Btn(text='?', x=237, y=34, w=40, h=40, bg_c=0x76501c, text_c=0xe8b844, font=FONT_MONT_30)
label_time = M5Label('0:00:00', x=25, y=46, color=0x3ba0ab, font=FONT_MONT_18)
label0 = M5Label('12345678901234567890123451234', x=12, y=118, color=0x2d672c, font=FONT_MONT_18)
label0.set_long_mode(1)

# Initial UI state
for el in [labelsi, labelno, btnsi, btnno, btn_question, label0]:
    el.set_hidden(True)

gc.collect()  # ✅ After UI setup

# ─── GLOBAL STATE ───────────────────────────────────────────
topic_output = None
message_code = ''
total_seconds = 35940 # 3600  # Initial time in seconds

# ─── FUNCTIONS ──────────────────────────────────────────────

def formattime(h, m, s):
    return "{}:{:02}:{:02}".format(h, m, s)

def update_timer():
    global total_seconds
    hrs = total_seconds // 3600
    mins = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    label_time.set_text(formattime(hrs, mins, secs))
    total_seconds = max(total_seconds - 1, 0)
    gc.collect()

@timerSch.event('timer0')
def ttimer0():
    update_timer()

def handle_message(topic_data):
    global topic_output, message_code
    topic_output = topic_data
    message_code = topic_output[:2]
    print("Received code:",message_code)

    if message_code == '00':
        label0.set_hidden(True)
        image0.set_img_src("res/Background_Inicial_v0.2-min.png")
        for el in [labelsi, labelno, btnsi, btnno, btn_question]:
            el.set_hidden(True)

    elif message_code == '01':
        power.setVibrationEnable(True)
        wait_ms(1500)
        power.setVibrationEnable(False)

    elif message_code in ['02', '03']:
        speaker.playTone(784, 1, volume=5)

    elif message_code == '04':
        for el in [labelsi, labelno, btnsi, btnno]:
            el.set_hidden(False)

    elif message_code == '05':
        for el in [labelsi, labelno, btnsi, btnno]:
            el.set_hidden(True)

    elif message_code == '10':
        btn_question.set_hidden(False)

    elif message_code == '11':
        btn_question.set_hidden(True)

    elif message_code == '08':
        micropython.mem_info()

    elif message_code == '91':
        pass

    else:
        label0.set_text(topic_output)
        image0.set_img_src("res/Background_withLet-min-v0.2.png")
        label0.set_hidden(False)
        print(topic_output)

    gc.collect()  # ✅ After handling message and possible UI/image changes

def btn_question_pressed():
    btn_question.set_hidden(True)
    speaker.playTone(220, 1/8, volume=6)
    speaker.playTone(110, 1/8, volume=6)
    m5mqtt.publish('rllabdevicesend', 'btnQ')

def handle_button(btn_id):
    speaker.playTone(220, 1/8, volume=6)
    speaker.playTone(110, 1/8, volume=6)
    m5mqtt.publish('rllabdevicesend', btn_id)

# ─── EVENTS ─────────────────────────────────────────────────

btn_question.pressed(btn_question_pressed)
btnA.wasPressed(lambda: handle_button('btnA'))
btnB.wasPressed(lambda: handle_button('btnB'))
btnC.wasPressed(lambda: handle_button('btnC'))

# ─── POWER / TIMER SETUP ────────────────────────────────────
power.setVibrationEnable(False)
power.setVibrationIntensity(50)
timerSch.run('timer0', 1000, 0x00)

# ─── MQTT INIT ──────────────────────────────────────────────
import wifiCfg

# wifiCfg.doConnect('blackcrow_prod01', 'e2aVwqCtfc5EsgGE852E')
wifiCfg.doConnect('blackcrow_01', '8001017170')
while not wifiCfg.wlan_sta.isconnected():
    wait_ms(100)
print("Wi-Fi connected!")
# m5mqtt = M5mqtt('RLLabDevice', '192.168.70.113', 1883, 'mqttuser', 'A1234567#', 300)
m5mqtt = M5mqtt('RLLabDevice', '192.168.1.92', 1883, 'mqttuser', 'A1234567#', 300)
m5mqtt.subscribe('rllabdevice', handle_message)
m5mqtt.start()


gc.collect()  # ✅ Final collection before going idle
