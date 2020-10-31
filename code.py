rint(" ")
print(" ")
print("   AUTONOMOUS")
print("  CORDWOOD CAR")
print("   BY HACKRC")
import time
import board
import busio
import adafruit_vl53l0x
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_display_shapes.triangle import Triangle
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pca9685
from adafruit_servokit import ServoKit

global thrinit, thrnum, turninc, cruiseang, reverseang

thrinit = 92
thrnum = thrinit
turninc = 10
cruiseang = 130
reverseang = 80


switch = digitalio.DigitalInOut(board.D21)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

led5 = DigitalInOut(board.D11)
led5.direction = Direction.OUTPUT
led6 = DigitalInOut(board.D12)
led6.direction = Direction.OUTPUT
led1 = DigitalInOut(board.D13)
led1.direction = Direction.OUTPUT
led2 = DigitalInOut(board.D14)
led2.direction = Direction.OUTPUT
led3 = DigitalInOut(board.D15)
led3.direction = Direction.OUTPUT
led4 = DigitalInOut(board.D16)
led4.direction = Direction.OUTPUT

xs1 = digitalio.DigitalInOut(board.D17)
xs1.direction = digitalio.Direction.OUTPUT
xs2 = digitalio.DigitalInOut(board.D9)
xs2.direction = digitalio.Direction.OUTPUT
xs3 = digitalio.DigitalInOut(board.D10)
xs3.direction = digitalio.Direction.OUTPUT

xs1.value = False
xs2.value = False
xs3.value = False

displayio.release_displays()

i2c = board.I2C()
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 60

kit = ServoKit(channels=16, address=0x40)
left_motor = kit.servo[1]
right_motor = kit.servo[0]

left_motor.angle = thrinit

right_motor.angle = thrinit
time.sleep(1)


xs1.value = True
time.sleep(0.1)

i2c.try_lock()
i2c.writeto(0x29, bytes([0x8A, 0x2A]))
time.sleep(0.1)

xs2.value = True
time.sleep(0.1)

i2c.unlock()
i2c.try_lock()

i2c.writeto(0x29, bytes([0x8A, 0x2B]))
time.sleep(0.1)
i2c.unlock()
time.sleep(0.1)

xs3.value = True
time.sleep(0.1)
i2c.try_lock()
i2c.writeto(0x29, bytes([0x8A, 0x2C]))
time.sleep(0.1)
i2c.unlock()

xs1.value = True
xs2.value = True
xs3.value = True
i2c.try_lock()
i2c.scan()
i2c.unlock()

vl531 = adafruit_vl53l0x.VL53L0X(i2c=i2c,address=0x2A, io_timeout_s=0)
vl532 = adafruit_vl53l0x.VL53L0X(i2c=i2c,address=0x2B, io_timeout_s=0)
vl533 = adafruit_vl53l0x.VL53L0X(i2c=i2c,address=0x2C, io_timeout_s=0)

r1=str(vl531.range)
r2=str(vl532.range)
r3=str(vl533.range)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

splash = displayio.Group(max_size=100)
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # Black
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

text = "MAIN POWER UP...."
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=1, y=5)
splash.append(text_area)

time.sleep(1)

text = "LASER 1 ONLINE...."
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=1, y=20)
splash.append(text_area)
time.sleep(.3)

text = "LASER 2 ONLINE...."
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=1, y=35)
splash.append(text_area)
time.sleep(.3)

text = "LASER 3 ONLINE...."
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=1, y=50)
splash.append(text_area)
time.sleep(.5)

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # Black
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

splash.pop(-1)
splash.pop(-1)
splash.pop(-1)
splash.pop(-1)
splash.pop(-1)

my_bitmap = displayio.OnDiskBitmap(open("/hackadaylogo_64.bmp", "rb"))
my_tilegrid = displayio.TileGrid(my_bitmap, pixel_shader=displayio.ColorConverter())
splash.append(my_tilegrid)
text = "HACKADAY"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=73, y=18)
splash.append(text_area)
text = "2020"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=85, y=42)
splash.append(text_area)

time.sleep(1)

splash.pop(-1)
splash.pop(-1)
splash.pop(-1)

t1p1x=50
t1p1y=32
t1p2x=30
t1p2y=0
t1p3x=0
t1p3y=25

t2p1x=65
t2p1y=32
t2p2x=40
t2p2y=1
t2p3x=90
t2p3y=1

t3p1x=80
t3p1y=32
t3p2x=128
t3p2y=25
t3p3x=98
t3p3y=0

triangle1 = Triangle(t1p1x, t1p1y, t1p2x, t1p2y, t1p3x, t1p3y, fill=0xFFFF00, outline=0x000000)
triangle2 = Triangle(t2p1x, t2p1y, t2p2x, t2p2y, t2p3x, t2p3y, fill=0xFFFF00, outline=0x000000)
triangle3 = Triangle(t3p1x, t3p1y, t3p2x, t3p2y, t3p3x, t3p3y, fill=0xFFFF00, outline=0x000000)
splash.append(triangle1)
splash.append(triangle2)
splash.append(triangle3)

distmax=8190

t1p2xmax=t1p1x
t1p2xmin=t1p2x
t1p2ymax=t1p1y
t1p2ymin=t1p2y
t1p3xmax=t1p1x
t1p3xmin=t1p3x
t1p3ymax=t1p1y
t1p3ymin=t1p3y

t2p2xmax=t2p1x
t2p2xmin=t2p2x
t2p2ymax=t2p1y
t2p2ymin=t2p2y
t2p3xmax=t2p1x
t2p3xmin=t2p3x
t2p3ymax=t2p1y
t2p3ymin=t2p3y

t3p2xmax=t3p1x
t3p2xmin=t3p2x
t3p2ymax=t3p1y
t3p2ymin=t3p2y
t3p3xmax=t3p1x
t3p3xmin=t3p3x
t3p3ymax=t3p1y
t3p3ymin=t3p3y

distrange = distmax
text = " LEFT   FRONT  RIGHT"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=41)
splash.append(text_area)
text = " IN MILLIMETERS"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=17, y=56)
splash.append(text_area)

def led_on(led_num):
    lc_string=str(led_num)
    lc_string_strip=lc_string.strip()
    led_on_exec='led'+str(led_num)+'.value = True'
    exec(led_on_exec)

def led_off(led_num):
    lc_string=str(led_num)
    lc_string_strip=lc_string.strip()
    led_off_exec='led'+str(led_num)+'.value = False'
    exec(led_off_exec)

def led_all_on():
    for ledcount in range(1,7):
        lc_string=str(ledcount)
        lc_string_strip=lc_string.strip()
        led_all_on_exec='led'+lc_string_strip+'.value = True'
        exec(led_all_on_exec)

def led_all_off():
    for ledcount in range(1,7):
        lc_string=str(ledcount)
        lc_string_strip=lc_string.strip()
        led_all_off_exec='led'+lc_string_strip+'.value = False'
        exec(led_all_off_exec)

def convertscales(oldvalue, oldmax, oldmin, newmax, newmin):
	oldrange = (oldmax - oldmin)
	newrange = (newmax - newmin)
	newvalue = (((oldvalue - oldmin) * newrange) / oldrange) + newmin
	return(newvalue)

def led_left():
    led1.value=True
    led2.value=True
    time.sleep(.01)
    led1.value=False
    led2.value=False
def led_center():
    led3.value=True
    led4.value=True
    time.sleep(.01)
    led3.value=False
    led4.value=False

def led_right():
    led5.value=True
    led6.value=True
    time.sleep(.01)
    led5.value=False
    led6.value=False

def autodrive():

    
    r1=str(vl531.range)
    r2=str(vl532.range)
    r3=str(vl533.range)
    rz1="{:0>4}".format(r1)
    rz2="{:0>4}".format(r2)
    rz3="{:0>4}".format(r3)
    #print(":"+rz1+":"+str(rz2)+":"+str(rz3)+":")
    r1int=int(r1)
    r2int=int(r2)
    r3int=int(r3)
    dt=time.time()
    print('DRIVING!'+str(dt))
    left_motor.angle = cruiseang
    right_motor.angle = cruiseang
    if r1int<500 and r2int>2000 and r3int>2000:
        left_motor.angle = cruiseang
        right_motor.angle = cruiseang - turninc
        time.sleep(.3)
        right_motor.angle = cruiseang
    if r1int>2000 and r2int<2000 and r3int<500:
        left_motor.angle = cruiseang - turninc
        right_motor.angle = cruiseang
        time.sleep(.3)
        left_motor.angle = cruiseang
    if r1int<500 and r2int<500 and r3int<500:
        left_motor.angle = thrinit
        right_motor.angle = thrinit
        time.sleep(.5)
        if r1int>=r3int:
            left_motor.angle = reverseang
            right_motor.angle = reverseang - turninc
        else:
            left_motor.angle = reverseang - turninc
            right_motor.angle = reverseang
        time.sleep(2.5)
        left_motor.angle = cruiseang
        right_motor.angle = cruiseang

    if r1int>500 and r2int<500 and r3int>500:
        if r1int>=r3int:
            left_motor.angle = cruiseang - turninc
            right_motor.angle = cruiseang
        else:
            left_motor.angle = cruiseang
            right_motor.angle = cruiseang  - turninc
        time.sleep(1)


def nightrider():
    for nrl in range(1,6):
        nrl_string=str(nrl)
        nrl2=nrl+1
        nrl2_string=str(nrl2)
        nrl_string_strip=nrl_string.strip()
        nrl2_string_strip=nrl2_string.strip()
        led_nrl_exec='led'+nrl_string_strip+'.value = True'
        exec(led_nrl_exec)
        time.sleep(.02)
        if nrl2 <= 6:
            led_nrl2_exec='led'+nrl2_string_strip+'.value = True'
            exec(led_nrl2_exec)
            time.sleep(.02)
        led_nrl_off_exec='led'+nrl_string_strip+'.value = False'
        exec(led_nrl_off_exec)
        time.sleep(.02)
        if nrl2 <= 6:
            led_nrl2_off_exec='led'+nrl2_string_strip+'.value = False'
            time.sleep(.02)
            exec(led_nrl2_off_exec)

    for nrl in range(6,1,-1):
        nrl_string=str(nrl)
        nrl2=nrl-1
        nrl2_string=str(nrl2)
        nrl_string_strip=nrl_string.strip()
        nrl2_string_strip=nrl2_string.strip()
        led_nrl_exec='led'+nrl_string_strip+'.value = True'
        exec(led_nrl_exec)
        time.sleep(.02)
        if nrl2 >= 1:
            led_nrl2_exec='led'+nrl2_string_strip+'.value = True'
            exec(led_nrl2_exec)
            time.sleep(.02)
        led_nrl_off_exec='led'+nrl_string_strip+'.value = False'
        exec(led_nrl_off_exec)
        time.sleep(.02)
        if nrl2 >= 1:
            led_nrl2_off_exec='led'+nrl2_string_strip+'.value = False'
            time.sleep(.02)
            exec(led_nrl2_off_exec)

    time.sleep(.5)

nightrider()
nightrider()
led_all_off()
loopcount = 0
while True:
        loopcount = loopcount+1
        if switch.value==True:
            splash.pop(-1)
            text = " AutoDrive Disabled"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            left_motor.angle = thrinit
            right_motor.angle = thrinit
        else:
            splash.pop(-1)
            text = " AutoDrive in --5--"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            time.sleep(1)
            splash.pop(-1)
            text = " AutoDrive in --4--"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            time.sleep(1)
            splash.pop(-1)
            text = " AutoDrive in --3--"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            time.sleep(1)            
            splash.pop(-1)
            text = " AutoDrive in --2--"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            time.sleep(1)
            splash.pop(-1)
            text = " AutoDrive in --1--"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            time.sleep(1)
            splash.pop(-1)
            text = " AutoDrive Engaged"
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=6, y=56)
            splash.append(text_area)
            led_all_on()
            while switch.value==False:
                autodrive()
            led_all_off()
        r1=str(vl531.range)
        r2=str(vl532.range)
        r3=str(vl533.range)
        rz1="{:0>4}".format(r1)
        rz2="{:0>4}".format(r2)
        rz3="{:0>4}".format(r3)
        #print(":"+rz1+":"+str(rz2)+":"+str(rz3)+":")

        r1int=int(r1)
        r2int=int(r2)
        r3int=int(r3)

        text = r1
        text_area = label.Label(terminalio.FONT, text=text, color=0x000000, x=15, y=19)
        splash.append(text_area)
        text = r2
        text_area = label.Label(terminalio.FONT, text=text, color=0x000000, x=56, y=8)
        splash.append(text_area)
        text = r3
        text_area = label.Label(terminalio.FONT, text=text, color=0x000000, x=92, y=19)
        splash.append(text_area)

        time.sleep(0.02)

        splash.pop(-1)
        splash.pop(-1)
        splash.pop(-1)

        if r1int<1000:
            led_on(1)
            led_on(2)
        else:
            led_off(1)
            led_off(2)
        if r2int<1000:
            led_on(3)
            led_on(4)
        else:
            led_off(3)
            led_off(4)
        if r3int<1000:
            led_on(5)
            led_on(6)
        else:
            led_off(5)
            led_off(6)
