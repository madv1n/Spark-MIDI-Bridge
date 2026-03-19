# Spark MIDI Bridge

A lightweight utility to bridge the `M-VAVE Chocolate Plus` controller and `Positive Grid Spark 40` amp using your PC as a "brain". At this stage the app allows to change presets only

Note on `Spark 2` Support:
The bridge is designed to detect any device with "Spark" in its name. While it was primarily developed for Spark 40, it should theoretically discover and connect to Spark 2 automatically. If you own a Spark 2, please help us by testing it and reporting your results!

<div align="center"><img src="https://github.com/user-attachments/assets/8e62b142-152c-44df-bfa0-5c016c707819"></div>
<div align="center"><img src="https://github.com/user-attachments/assets/e9241080-751b-482c-9f01-369cc4a2dffa"></div>

## Why use this bridge?
Standalone: No need for MidiBerry, loopMIDI, or any other virtual MIDI cables.

Direct Link: Connects your pedal directly to the Spark amp via software.

Low Latency: Optimized for real-time performance.

## Connection Modes

The bridge supports two ways to talk to your pedal:
    USB (Recommended): Lowest latency, rock-solid stability.
    Bluetooth: Wireless freedom, but requires a stable system Bluetooth stack. 

## Getting Started

### 1. Download Files
1.  Click the green **`<> Code`** button at the top of this page.
2.  Select **`Download ZIP`**.
3.  Extract the archive to a convenient folder.

### 2. MIDI Setup Guide for Spark Bridge
To ensure the program works correctly, the buttons on your pedal must send unique signals. If the app shows the same "Button ID" for every press, please update your pedal settings via CubeSuite (or your pedal's configuration app) as follows:
1. Button Mapping (IDs)
Each physical button (A, B, C, D) must have its own unique number. Recommended settings:
    * Button A: ID 0 (or 1)
    * Button B: ID 1 (or 2)
    * Button C: ID 2 (or 3)
    * Button D: ID 3 (or 4)
2. Message Type (Mode)
The Spark Bridge app is universal and supports both major MIDI message types. You can use either:
    * CC (Control Change): The most common "stompbox" mode.
    * PC (Program Change): Often used for preset switching.
3. Value (For CC Mode)
    * If you are using CC mode, make sure the "Value" is set to 127 (this ensures the signal is strong enough to be detected as a "press").
How to Verify
Connect your pedal to your PC.
* Press buttons A, B, C, and D one by one while watching the Log window in the Spark Bridge app.
You should see different numbers appear: Action: BTN 0..., Action: BTN 1..., etc.

### 3. Connect the M-VAVE to PC (Bluetooth and USB)
The "Wake-up" Trick: Windows often keeps the Bluetooth adapter in a "sleep" mode for low-energy devices. To make the Spark Amp visible, you need to "wake up" the Bluetooth stack. The most reliable way is to have your pedal paired with the PC.
* For USB Mode (Recommended):
    * Pair the controller via Bluetooth first (Settings -> Devices -> Pair FootCtrlPlus). This is only required once to initialize the scan.
    * Connect the USB cable
    * Once the app shows SPARK: ONLINE, the Bluetooth link to the pedal is no longer needed. You can even move the pedal away or rely solely on the cable — the "handshake" with the amp is already established.
* For Bluetooth Mode:
    * Pair the controller via Bluetooth first (Settings -> Devices -> Pair FootCtrlPlus).
    * Keep the controller paired and switched to the "U" position.
    * The app will handle both the "wake-up" and the MIDI commands wirelessly.

### 4. Run the App
1. Ensure the controller is paired (to trigger the BLE scan).
2. Make sure your `Spark 40` is turned on and NOT connected to the Spark App on your phone (Spark can only talk to one "Master" at a time).
3. Run the `SparMidiBridge.exe`. `Windows`


For **`macOS`** `In work`

4. Wait for the green lights **`PEDAL: READY`** and **`SPARK: ONLINE`**
5. Have fun

## Troubleshooting

In work...

## Source Code
For developers and advanced users, the raw Python scripts are available in the `/src` folder. You can run them directly if you have at least `Python 3.13` installed with the required libraries (bleak, pygame, winrt).

## System Requirements
Tested on: Windows 11

Hardware: Spark 40 Amp, M-VAVE Chocolate Plus

Backend: Bleak (BLE), Pygame (MIDI), winrt

## Tested & Verified Combinations
* M-VAVE Chocolate Plus - Positive Grid Spark (40) firmware V1.10.8.25 ✅

## 🧪 Community Testing (Help Needed!)
I want this bridge to be a universal tool for the Spark community. If you own different hardware, you can help by providing its system identity.

How to help:
* Connect your hardware (MIDI pedal or different Spark amp) to your computer (BT and USB).

Report the exact Device Name:

* In the Bluetooth & Devices settings, find the exact string name of your device (e.g., M-VAVE Chocolate...FootCtrlPlus, SINCO...).

Open an Issue: Use the "New Hardware Support" tag and paste the device names there.

Currently seeking data for:
* Amps: Spark 2, Spark GO, Spark MINI, Spark LIVE.

* Pedals: Line 6 FBV, Behringer FCB1010, IK Multimedia BlueBoard, etc.

Your contribution will help me add "Plug & Play" support for these devices in the next update!

## 📜 Credits & Acknowledgments
This project uses research and protocol documentation from the following open-source projects:
* **[SparkMIDI](https://github.com/paulhamsh/SparkMIDI)** — for the original Sysex command structures.

## Disclaimer
**Use this software at your own risk.** - This project is NOT affiliated with, authorized, or endorsed by Positive Grid.
- The author is not responsible for any potential damage to your amplifier, MIDI hardware, or computer.
- Always test your setup before using it in a live performance.

## Support my project
If this tool helps you, you can support further development:

<a href="https://www.buymeacoffee.com/pk_rpforge" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px;width: 217px !important;" ></a>
