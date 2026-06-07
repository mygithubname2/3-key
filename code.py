import board
import keypad
import neopixel
import usb_hid



from adafruit_hid.keycode import Keycode
#from adafruit_hid.footpad import Footpad
from footpad import Footpad

KEY_PINS = (board.GP14, board.GP13, board.GP12,)
KEYCODES = (1, 2, 4,)

footpad = Footpad(usb_hid.devices)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

pixel_pin = board.GP18
num_pixels = 3 # Change to the number of LEDs in your strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.9, auto_write=False)


while True:
    event = keys.events.get()
    if event:
        key_number = event.key_number

        if event.pressed:
            footpad.press(KEYCODES[key_number])
            pixels[key_number] = (255, 0, 255)
            pixels.show() 

        if event.released:
            footpad.release(KEYCODES[key_number])
            pixels[key_number] = (0, 0, 0)
            pixels.show()


