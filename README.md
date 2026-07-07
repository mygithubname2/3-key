
## Discription
This is a hardware and software solution to allow a 3 button macropad to emulate a foot pedal for dictation without needing Autohotkey. The hardware is cheap and the firmware is easy to install. Once installed, the dictation software will see it and treat it exactly like a standard 3 button foot pedal. 

<img src="assets/3key%20macropad.jpg" width="300" />

## Prerequisites
* A Waveshare RP2040-Keyboard-3 board [https://www.waveshare.com/rp2040-keyboard-3.htm]
* Custom keycaps (optional) [https://yuzukeycaps.com/] 
* A USB Type-C data cable (ensure it supports data transfer, not just charging)
* A computer (Windows, macOS, or Linux)

 
## Installation Guide

### Step 1: Download CircuitPython
Because the Waveshare 3-Key board is powered by the standard RP2040 microcontroller, it uses the standard Raspberry Pi Pico build of CircuitPython.
1. Go to the official [CircuitPython download page for the Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/).
2. Click the **DOWNLOAD .UF2 NOW** button to download the latest stable release.

### Step 2: Enter Bootloader Mode
To flash CircuitPython onto the board, you must put the RP2040 into its UF2 bootloader mode.
1. Locate the **BOOT** and **RESET** buttons on the bottom/back of the board. 
2. While the board is plugged into your computer via USB:
   * Press and **hold** the **BOOT** button.
   * While still holding BOOT, press and release the **RESET** button.
   * Finally, release the **BOOT** button.
   
   *(Alternatively: Unplug the board, hold down the BOOT button, plug the USB cable into your computer, and then release the BOOT button).*
3. A new removable USB mass storage drive named **`RPI-RP2`** will appear on your computer.

### Step 3: Install CircuitPython
1. Locate the `.uf2` file you downloaded in Step 1.
2. Drag and drop (or copy and paste) the `.uf2` file into the root directory of the **`RPI-RP2`** drive.
3. Once the file transfer completes, the board will automatically restart. 
4. The `RPI-RP2` drive will disappear, and a new drive named **`CIRCUITPY`** will mount to your computer. CircuitPython is now successfully installed!

### Step 4: Upload the Custom Firmware
With CircuitPython running, the board will automatically execute the `code.py` file found on the root of the drive.
1. Clone or download this repository to your local machine.
2. Open the **`CIRCUITPY`** drive on your computer.
3. Copy the contents of this repository (specifically `boot.py`, `code.py`, and `footpad.py` and any included `/lib` folder or asset files) directly into the root directory of the **`CIRCUITPY`** drive.
4. Replace any existing files if prompted. 
5. CircuitPython will automatically detect the changes, soft-reboot, and begin running the new firmware immediately.

### Step 5: Configure the Firmware
The configuration webpage can be accessed at https://mygithubname2.github.io/3-key/

## Troubleshooting
* **The `RPI-RP2` drive doesn't appear:** Ensure your USB-C cable supports data transfer. Try switching to a different cable or USB port.
* **How do I change the code?:** Once the code is running, to modify the Firmware, unplug the board, hold down the MIDDLE button, plug the USB cable into your computer, and then release the MIDDLE button once the circuitpython harddrive has been mounted.
