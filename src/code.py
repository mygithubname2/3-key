import board
import keypad
import neopixel
import usb_hid
import usb_cdc
import microcontroller

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from footpad import Footpad

KEY_PINS = (board.GP14, board.GP13, board.GP12,)

# Initialize all HID outputs
keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
footpad = Footpad(usb_hid.devices)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

pixel_pin = board.GP18
num_pixels = 3 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.9, auto_write=False, pixel_order=neopixel.RGB)

# Arrays for live state
key_colors = []
key_mappings = []
key_toggle = [0, 0, 0]             
key_logical_state = [False, False, False] 

# 1. Load Colors (NVM Bytes 0-8)
for i in range(3):
    nvm_index = i * 3
    try:
        r = microcontroller.nvm[nvm_index]
        g = microcontroller.nvm[nvm_index + 1]
        b = microcontroller.nvm[nvm_index + 2]
        key_colors.append((r, g, b))
    except Exception:
        key_colors.append((255, 0, 255))

# 2. Load Key Mappings (NVM Bytes 10-15)
for i in range(3):
    map_index = 10 + (i * 2)
    try:
        m_type = microcontroller.nvm[map_index]
        m_code = microcontroller.nvm[map_index + 1]
        if m_type > 2:
            m_type = 0
            m_code = [1, 2, 4][i] 
        key_mappings.append([m_type, m_code])
    except Exception:
        key_mappings.append([0, [1, 2, 4][i]])

# 3. Load Brightness (NVM Byte 9)
try:
    stored_brightness = microcontroller.nvm[9]
    pixels.brightness = stored_brightness / 255.0
except IndexError:
    pixels.brightness = 0.9

# 4. Load LED Mode (NVM Byte 16)
try:
    led_mode = microcontroller.nvm[16]
    # --- UPDATED: Allow 0, 1, or 2 ---
    if led_mode > 2:
        led_mode = 0
except IndexError:
    led_mode = 0

# 5. Load Toggle Mode (NVM Bytes 17-19)
for i in range(3):
    try:
        t_val = microcontroller.nvm[17 + i]
        if t_val > 1: t_val = 0
        key_toggle[i] = t_val
    except Exception:
        pass

def apply_gamma(color, gamma=2.8):
    r, g, b = color
    r_corr = int(((r / 255.0) ** gamma) * 255 + 0.5)
    g_corr = int(((g / 255.0) ** gamma) * 255 + 0.5)
    b_corr = int(((b / 255.0) ** gamma) * 255 + 0.5)
    return (r_corr, g_corr, b_corr)

# --- NEW: Helper function to determine LED color based on mode and state ---
def update_single_led(index):
    is_down = key_logical_state[index]
    if is_down:
        # If pressed/down: OFF if Inverse (2), ON otherwise
        pixels[index] = (0, 0, 0) if led_mode == 2 else apply_gamma(key_colors[index])
    else:
        # If released/up: OFF if Reactive (0), ON otherwise
        pixels[index] = (0, 0, 0) if led_mode == 0 else apply_gamma(key_colors[index])
    pixels.show()

def update_all_leds():
    for i in range(3):
        is_down = key_logical_state[i]
        if is_down:
            pixels[i] = (0, 0, 0) if led_mode == 2 else apply_gamma(key_colors[i])
        else:
            pixels[i] = (0, 0, 0) if led_mode == 0 else apply_gamma(key_colors[i])
    pixels.show()

# Run immediately to light up the board based on preference
update_all_leds()

while True:
    # Check for incoming serial data
    if usb_cdc.data and usb_cdc.data.in_waiting > 0:
        try:
            raw_data = usb_cdc.data.readline().decode('utf-8').strip()
            if raw_data:
                # Handle SYNC handshake
                if raw_data == "SYNC":
                    for i in range(3):
                        r, g, b = key_colors[i]
                        usb_cdc.data.write(f"{i},COLOR,{r},{g},{b}\n".encode('utf-8'))
                        m_type, m_code = key_mappings[i]
                        usb_cdc.data.write(f"{i},MAP,{m_type},{m_code}\n".encode('utf-8'))
                        usb_cdc.data.write(f"{i},TOGGLE,{key_toggle[i]}\n".encode('utf-8'))
                    
                    current_b = int(pixels.brightness * 255)
                    usb_cdc.data.write(f"BRIGHTNESS,{current_b}\n".encode('utf-8'))
                    usb_cdc.data.write(f"LEDMODE,{led_mode}\n".encode('utf-8'))
                
                else:
                    parts = raw_data.split(',')
                    
                    if len(parts) == 2 and parts[0] == "BRIGHTNESS":
                        b_val = int(parts[1])
                        pixels.brightness = b_val / 255.0
                        pixels.show()
                        microcontroller.nvm[9] = b_val
                        
                    # --- UPDATED: Allow mode 2 ---
                    elif len(parts) == 2 and parts[0] == "LEDMODE":
                        l_val = int(parts[1])
                        if l_val in (0, 1, 2):
                            led_mode = l_val
                            microcontroller.nvm[16] = led_mode
                            update_all_leds()
                    
                    elif len(parts) == 3 and parts[1] == "TOGGLE":
                        k_idx = int(parts[0])
                        t_val = int(parts[2])
                        if 0 <= k_idx < 3:
                            key_toggle[k_idx] = t_val
                            microcontroller.nvm[17 + k_idx] = t_val
                            key_logical_state[k_idx] = False
                            footpad.release_all()
                            keyboard.release_all()
                            mouse.release_all()
                            update_single_led(k_idx)
                    
                    elif len(parts) == 4 and parts[1] == "MAP":
                        k_idx = int(parts[0])
                        m_type = int(parts[2])
                        m_code = int(parts[3])
                        
                        if 0 <= k_idx < 3:
                            key_mappings[k_idx] = [m_type, m_code]
                            map_index = 10 + (k_idx * 2)
                            microcontroller.nvm[map_index] = m_type
                            microcontroller.nvm[map_index + 1] = m_code

                    elif len(parts) == 4:
                        k_idx = int(parts[0])
                        r = int(parts[1])
                        g = int(parts[2])
                        b = int(parts[3])
                        
                        if 0 <= k_idx < 3:
                            key_colors[k_idx] = (r, g, b)
                            nvm_index = k_idx * 3
                            microcontroller.nvm[nvm_index] = r
                            microcontroller.nvm[nvm_index + 1] = g
                            microcontroller.nvm[nvm_index + 2] = b
                            update_single_led(k_idx)
                            
        except Exception:
            pass 

    # Handle Key Presses
    event = keys.events.get()
    if event:
        key_number = event.key_number
        m_type, m_code = key_mappings[key_number]
        is_toggle = key_toggle[key_number] == 1

        if event.pressed:
            if is_toggle:
                key_logical_state[key_number] = not key_logical_state[key_number]
                is_down = key_logical_state[key_number]
            else:
                key_logical_state[key_number] = True
                is_down = True

            if is_down:
                if m_type == 0: footpad.press(m_code)
                elif m_type == 1: keyboard.press(m_code)
                elif m_type == 2: mouse.press(m_code)
                
                update_single_led(key_number)
                if usb_cdc.data: usb_cdc.data.write(f"{key_number},DOWN\n".encode('utf-8'))
            
            else:
                if m_type == 0: footpad.release(m_code)
                elif m_type == 1: keyboard.release(m_code)
                elif m_type == 2: mouse.release(m_code)
                
                update_single_led(key_number)
                if usb_cdc.data: usb_cdc.data.write(f"{key_number},UP\n".encode('utf-8'))

        if event.released:
            if not is_toggle:
                key_logical_state[key_number] = False
                
                if m_type == 0: footpad.release(m_code)
                elif m_type == 1: keyboard.release(m_code)
                elif m_type == 2: mouse.release(m_code)
                
                update_single_led(key_number)
                if usb_cdc.data: usb_cdc.data.write(f"{key_number},UP\n".encode('utf-8'))