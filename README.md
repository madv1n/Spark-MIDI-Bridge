# Spark 40 MIDI Bridge

A lightweight and robust utility to connect MIDI foot controllers to the **Positive Grid Spark 40** amplifier via your computer.
![spark](https://github.com/user-attachments/assets/0aaeafa0-2b30-4143-a534-9a5edcaf4a1c)
## Getting Started

### Prerequisites
The program requires **Python 3.12** or lower.
* **Windows**: Download from [python.org](https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe). *Check "Add Python to PATH" during installation.*
* **macOS**: Verify in Terminal: `python3 --version` or download it from [python.org](https://www.python.org/ftp/python/3.12.7/python-3.12.7-macos11.pkg)

### 1. Download Files
1.  Click the green **`<> Code`** button at the top of this page.
2.  Select **`Download ZIP`**.
3.  Extract the archive to a convenient folder.

### 2. USB Connection (Wired)
This is the most straightforward and reliable method.
1. Connect the controller to your computer using a USB cable.
2. Turn on your controller to the "U" position.
3. No additional software is required for the computer to recognize the device.

### 3. Bluetooth Connection (Wireless)
If you prefer to connect your controller to the computer wirelessly:
1. Turn on your controller to the "U" position.
2. Pair the controller with the computer.
3. Install [MIDIberry](https://apps.microsoft.com/detail/9n39720h2m05?rtc=1&hl=en-US&gl=US) application (to route the Bluetooth MIDI signal).
4. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) (to create a virtual MIDI port).
5. Open the loopMIDI. To create a MIDI Port click **`+`**
6. Open the MIDIBerry. From the **`INPUT`** field select your controller - **`FootCtrlPlus(Bluetooth MIDI..)`**. From the **`OUTPUT`** field select the **`loopMIDI Port [1]`**

### 4. One-Click Launch

For **`Windows`** run the `SparkMIDIBridge.bat`. First run will auto-install all necessary libraries - `bleak`, `pygame`, and `Pillow`.

For **`macOS`** Users:
1. Open Terminal, type `chmod +x `, (and be sure to press space after +x) and drag the `.command` file into the window. Press Enter.
2. If you see a "damaged file" error, run:
`sudo xattr -rd com.apple.quarantine [drag_file_here]`

Statuses will be **`MIDI: READY`** and **`SPARK: ONLINE`**

## Troubleshooting

* **SPARK: OFF**: Ensure Spark is ON and **not** connected to the official mobile app. Restart the Spark and `SparkMIDIBridge.bat`.
* **MIDI: OFF**: Restart the controller and the `SparkMIDIBridge.bat`.
