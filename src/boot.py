import board
import digitalio
import storage
import supervisor
import usb_hid
import usb_midi
import usb_cdc

usb_midi.disable()
usb_cdc.enable(console=True, data=True)

# footpad report descriptor
FOOTPAD_REPORT_DESCRIPTOR = bytes((  
    0x05, 0x0C,  # Usage Page (Consumer)    
    0x09, 0x03,  # Usage (Programmable Buttons)
    0xA1, 0x01,  # Collection (Application)    
    0x85, 0x04,  #   Report ID (4) <--- NEW: Assigned a unique ID
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (0x01)
    0x29, 0x03,  #   Usage Maximum (0x03)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x95, 0x03,  #   Report Count (3)
    0x75, 0x01,  #   Report Size (1)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,  #   Report Count (1)
    0x75, 0x05,  #   Report Size (5)   Padding
    0x81, 0x01,  #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,  #   Report Count (1)
    0x75, 0x08,  #   Report Size (8)    Padding
    0x81, 0x01,  #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
)) # 69 bytes

footpad = usb_hid.Device(
    report_descriptor=FOOTPAD_REPORT_DESCRIPTOR,
    usage_page=0x0C,           
    usage=0x03,                
    report_ids=(4,),           # <--- NEW: Tell CircuitPython to use ID 4
    in_report_lengths=(2,),    
    out_report_lengths=(0,),   
)

# Enable Keyboard, Mouse, and Footpad simultaneously
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE, footpad)) 

usb_hid.set_interface_name("3KEY USB MACROPAD")
supervisor.set_usb_identification(
    manufacturer='3Key',             
    product='3key USB Macropad',    
    vid=0x05F3,                     
    pid=0x00FF                      
)

button = digitalio.DigitalInOut(board.GP13)
button.pull = digitalio.Pull.UP

if button.value:
    storage.disable_usb_drive()