from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5mqtt import M5mqtt
import time, gc

# ─── CHECK DEVICE ──────────────────────────────────────────────

import network

atHome = True
if atHome:
    primary_network = 'blackcrow_01'
    primary_pass = '8001017170'
else:
    primary_network = 'blackcrow_prod01'
    primary_pass = 'e2aVwqCtfc5EsgGE852E'
    secondary_network = 'blackcrow_01'
    secondary_pass = '8001017170'


wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # ⚠️ Important: ensure the interface is active

mac = wlan.config('mac')
mac_str = ':'.join('{:02X}'.format(b) for b in mac)
print("MAC Address:", mac_str)

if (mac_str == '2C:BC:BB:82:92:F0'):  # main device
    mqttqueue = 'rllabdevice'
    mqttqueuesend = 'rllabdevicesend'
    print("Main device")
else:
    mqttqueue = 'rllabdevice2'
    mqttqueuesend = 'rllabdevicesend2'
    print("Mirror device")
    
# ─── UI SETUP ──────────────────────────────────────────────
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xffffff)        

# ─── UI ELEMENTS ────────────────────────────────────────────
image0 = M5Img("res/Background_Inicial_v0.2-min.png", x=0, y=0)


btnsi = M5Btn(text='o', x=39, y=192, w=40, h=40, bg_c=0x56acd3, text_c=0x56acd3, font=FONT_MONT_14)
btnno = M5Btn(text='o', x=244, y=192, w=40, h=40, bg_c=0x56acd3, text_c=0x56acd3, font=FONT_MONT_14)
labelsi = M5Label('SI', x=50, y=202, color=0x000, font=FONT_MONT_18)
labelno = M5Label('NO', x=248, y=202, color=0x000, font=FONT_MONT_18)
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

    elif message_code == '14':
        speaker.playWAV('/flash/res/ding_dis.wav', volume=6)
        
    # apagar pantalla
    elif message_code == '90':
        for el in [labelsi, labelno, btnsi, btnno, btn_question, label0]:
            el.set_hidden(True)
        screen.set_screen_brightness(0)
    
    # encender pantalla
    elif message_code == '91':
        image0.set_hidden(False)
        screen.set_screen_brightness(100)
    
    # reportar la batería del dispositivo
    elif message_code == '92':
        tempnada = '92:'
        tempnada = tempnada + str(power.getBatPercent()) + ','
        tempnada = tempnada +  str(power.getBatVoltage())+ ','
        tempnada = tempnada + str(power.getBatCurrent())
        m5mqtt.publish(mqttqueuesend, tempnada)

    # resetear
    elif message_code == '93':
        power.restart_after_seconds(2)

    # apagar
    elif message_code == '94':
        power.powerOff()

    else:
        label0.set_text(topic_output)
        image0.set_img_src("res/Background_withLet-min-v0.2.png")
        label0.set_hidden(False)
        print(topic_output)

    gc.collect()  # ✅ After handling message and possible UI/image changes

def hide_buttons():
    for el in [labelsi, labelno, btnsi, btnno, btn_question]:
        el.set_hidden(True)    
   
def btn_question_pressed():
    btn_question.set_hidden(True)
    speaker.playTone(220, 1/8, volume=6)
    speaker.playTone(110, 1/8, volume=6)
    m5mqtt.publish(mqttqueuesend, 'btnQ')

def handle_button(btn_id):
    speaker.playTone(220, 1/8, volume=6)
    speaker.playTone(110, 1/8, volume=6)
    hide_buttons()
    m5mqtt.publish(mqttqueuesend, btn_id)

def btn_si_pressed():
    speaker.playTone(220, 1/8, volume=6)
    speaker.playTone(110, 1/8, volume=6)
    hide_buttons()
    m5mqtt.publish(mqttqueuesend, 'btnA')
def btn_no_pressed():
    speaker.playTone(220, 1/8, volume=6)
    speaker.playTone(110, 1/8, volume=6)
    hide_buttons()
    m5mqtt.publish(mqttqueuesend, 'btnC')

# ─── EVENTS ─────────────────────────────────────────────────

btn_question.pressed(btn_question_pressed)
btnsi.pressed(btn_si_pressed)
btnno.pressed(btn_no_pressed)

btnA.wasPressed(lambda: handle_button('btnA'))
btnB.wasPressed(lambda: handle_button('btnB'))
btnC.wasPressed(lambda: handle_button('btnC'))

# ─── POWER / TIMER SETUP ────────────────────────────────────
power.setVibrationEnable(False)
power.setVibrationIntensity(50)
timerSch.run('timer0', 1000, 0x00)

# ─── MQTT INIT ──────────────────────────────────────────────
import wifiCfg

print("Starting Wifi")

MAX_RETRIES = 5
RETRY_DELAY_MS = 200
wifiCfg.doConnect(primary_network, primary_pass)
connected = False
if wifiCfg.wlan_sta.isconnected():
   connected = True

if not connected:
    print("Primary network failed. Trying fallback...")
    wifiCfg.doConnect(secondary_network, secondary_pass)
    if wifiCfg.wlan_sta.isconnected():
       connected = True

if connected:
    print("Wi-Fi connected:", wifiCfg.wlan_sta.ifconfig()[0])
else:
    print("Wi-Fi connection failed.")

m5mqtt = M5mqtt(mqttqueue, '192.168.70.113', 1883, 'mqttuser', 'A1234567#', 300)

m5mqtt.subscribe(mqttqueue, handle_message)
m5mqtt.start()


gc.collect()  # ✅ Final collection before going idle
