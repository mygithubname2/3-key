

import board
import digitalio
import storage

import supervisor
import usb_hid
import usb_midi
import usb_cdc

# usb_cdc.disable()   # Disable both serial devices.
usb_midi.disable()
# usb_hid.enable((usb_hid.Device.KEYBOARD,))   # Enable just KEYBOARD.

# footpad report descriptor
FOOTPAD_REPORT_DESCRIPTOR = bytes((  
    0x05, 0x0C,  # Usage Page (Consumer)    
    0x09, 0x03,  # Usage (Programmable Buttons)
    0xA1, 0x01,  # Collection (Application)    
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (0x01)
    0x29, 0x03,  #   Usage Maximum (0x03)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x95, 0x03,  #   Report Count (3) Button?
    0x75, 0x01,  #   Report Size (1)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,  #   Report Count (1)
    0x75, 0x05,  #   Report Size (5)   Padding
    0x81, 0x01,  #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,  #   Report Count (1)
    0x75, 0x08,  #   Report Size (8)    Padding
    0x81, 0x01,  #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
)) # 67 bytes


footpad = usb_hid.Device(
    report_descriptor=FOOTPAD_REPORT_DESCRIPTOR,
    usage_page=0x0C,           # Consumer Page
    usage=0x03,                # Programmable Buttons
    report_ids=(0,),           # Descriptor uses report ID 0.
    in_report_lengths=(2,),    # This footpad sends 2 bytes (3 bits for the buttons + 13 bits of padding).
    out_report_lengths=(0,),   # It does not receive any reports.
)


usb_hid.enable((footpad,)) 
usb_hid.set_interface_name("3KEY USB FOOTPEDAL")   # interface name within the USB Interface Descriptor
supervisor.set_usb_identification(
                                  manufacturer='3Key',             # usb manufacturer string
                                  product='3key USB Footpedal',    # usb product string
                                  vid=0x05F3,                     # Vendor ID
                                  pid=0x00FF                      # Product ID
)



button = digitalio.DigitalInOut(board.GP13)
button.pull = digitalio.Pull.UP

if button.value:
    storage.disable_usb_drive()


