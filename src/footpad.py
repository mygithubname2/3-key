
# from . import find_device # used if this file is in the adafruit_hid folder
from adafruit_hid.__init__ import find_device

try:
    from typing import Sequence
    import usb_hid
except ImportError:
    pass


class Footpad:
    """Send USB HID footpad reports."""
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 2
    MIDDLE_BUTTON = 4

    def __init__(self, devices: Sequence[usb_hid.Device], timeout: int = None) -> None:
        self._footpad_device = find_device(devices, usage_page=0x0C, usage=0x03, timeout=timeout)
        self.report = bytearray(2)      
        # Bytearray to send footpad reports.
        # report[0] buttons pressed (LEFT, MIDDLE, RIGHT)
        # report[1] buffer

    def press(self, buttons: int) -> None:
        self.report[0] |= buttons
        self._send()

    def release(self, buttons: int) -> None:
        self.report[0] &= ~buttons
        self._send()
 
    def release_all(self) -> None:
        self.report[0] = 0
        self._send()

    def click(self, buttons: int) -> None:
        self.press(buttons)
        self.release(buttons)

    def _send(self) -> None:
        self.report[1] = 0
        self._footpad_device.send_report(self.report)

 