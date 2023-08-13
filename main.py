import network
import socket
import time
import machine
import ntptime

ssid = 'SSID'
password = 'password'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    
try:
    connect()
except KeyboardInterrupt:
    machine.reset()

ntptime.settime()
CEST_diff=2 # UTC +2
CET_diff=1 # UTC +1
timezone_diff=0

def summer_winter_time(t):
    global timezone_diff
    year=time.localtime()[0]
    summer=list(time.localtime(time.mktime((year, 3, 31, 1, 0, 0, None, None))))
    summer[2] -= (summer[6] + 1) % 7
    winter=list(time.localtime(time.mktime((year, 10, 31, 1, 0, 0, None, None))))
    winter[2] -= (winter[6] + 1) % 7
    summer[6:8] = winter[6:8] = (None, None)
    if time.mktime(summer) < time.time() and time.mktime(winter) > time.time():
        timezone_diff=CEST_diff
    else:
        timezone_diff=CET_diff

summer_winter_time(None)

import array
import rp2

# Configure the number of WS2812 LEDs.
NUM_LEDS = 16
PIN_NUM = 0
f=open("brightness", "r")
brightness=float(f.read())
f.close()

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=machine.Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

started_brightness_up_timer = 0
started_brightness_down_timer = 0
f=open("morning_light","r")
morning_light=int(f.read())
f.close()
def time_check(t):
    global brightness_up_timer
    global started_brightness_up_timer
    global started_brightness_down_timer
    global morning_light
    global started_summer_winter_timer
    #time.licaltime() in GMT
    if time.localtime()[3] + timezone_diff > 6 and time.localtime()[3] + timezone_diff < 12 and started_brightness_up_timer == 0:
        brightness_up_timer=machine.Timer(period=15000, callback=brightness_up)
        started_brightness_up_timer=1
        started_brightness_down_timer=0
    if time.localtime()[3] + timezone_diff > 20 and started_brightness_down_timer == 0:
        brightness_down_timer=machine.Timer(period=60000, callback=brightness_down)
        started_brightness_down_timer=1
        started_brightness_up_timer=0
    if morning_light == 1 and time.localtime()[3] + timezone_diff > 12:
        morning_light = 0
        f=open("morning_light","w")
        f.write(str(morning_light))
        f.close()
    if time.localtime()[3] < 1 and started_summer_winter_timer == 0:
        started_summer_winter_timer = 1
        summer_winter_timer=machine.Timer(period=86400000, callback=summer_winter_time)
        
        
def brightness_up(t):
    global brightness
    global brightness_up_timer
    global light_state
    global morning_light
    if brightness > 0.8:
        machine.Timer.deinit(brightness_up_timer)
    else:
        brightness=brightness+0.01
        f=open("brightness","w")
        f.write(str(brightness))
        f.close()
        if morning_light == 1 and light_state == 1:
            pixels_fill(WARM_WHITE)
            pixels_show()
    if morning_light == 0 and light_state == 0:
        pixels_fill(WARM_WHITE)
        pixels_show()
        light_state = 1
        f=open("light_state", "w")
        f.write("1")
        f.close()
        morning_light = 1
        f=open("morning_light","w")
        f.write(str(morning_light))
        f.close()

        
        
def brightness_down(t):
    global brightness
    if brightness > 0.05 and brightness < 0.51:
        brightness=brightness-0.01
        f=open("brightness","w")
        f.write(str(brightness))
        f.close()
    elif brightness > 0.5:
        brightness=0.5
        f=open("brightness","w")
        f.write(str(brightness))
        f.close()
    else:
        machine.Timer.deinit(brightness_up_timer)
    if light_state == 1:
        pixels_fill(WARM_WHITE)
        pixels_show()


def button_press_handler(button):
    global light_state
    button.irq(handler=None)
    
    if button.value() == 0 and button_state == 1:
        if light_state == 0:
            pixels_fill(WARM_WHITE)
            pixels_show()
            light_state=1
            f=open("light_state", "w")
            f.write("1")
            f.close()
        else:
            pixels_fill(BLACK)
            pixels_show()
            light_state=0
            f=open("light_state", "w")
            f.write("0")
            f.close()
    time.sleep(0.1)
    button.irq(handler=button_press_handler)
  
        
WARM_WHITE = (255,220,200)
BLACK = (0,0,0)

general_timer=machine.Timer(period=5000, callback=time_check)

button_pin = 1
button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
button_state = button.value()
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_press_handler) # interrupt to turn lights on/off with physical button

f=open("light_state","r")
light_state=int(f.read())
f.close()

if light_state == 1:
    pixels_fill(WARM_WHITE)
    pixels_show()