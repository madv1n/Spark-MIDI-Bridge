# Spark 40 MIDI Bridge

A lightweight utility to bridge the `M-VAVE Chocolate Plus` controller and `Positive Grid Spark 40` amp using your PC as a "brain". At this stage the app allows to change presets only
<div align="center"><img src="https://github.com/user-attachments/assets/8e62b142-152c-44df-bfa0-5c016c707819"></div>
<div align="center"><img src="https://github.com/user-attachments/assets/7ad0ae02-5e25-42e6-abdd-102b3984a81b"></div>

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

### 2. Connect the M-VAVE to PC (Bluetooth and USB)
The "Wake-up" Trick: Windows often keeps the Bluetooth adapter in a "sleep" mode for low-energy devices. To make the Spark Amp visible, you need to "wake up" the Bluetooth stack. The most reliable way is to have your pedal paired with the PC.
* For USB Mode (Recommended):
    * Pair the controller via Bluetooth first (Settings -> Devices -> Pair FootCtrlPlus). This is only required once to initialize the scan.
    * Connect the USB cable
    * Once the app shows SPARK: ONLINE, the Bluetooth link to the pedal is no longer needed. You can even move the pedal away or rely solely on the cable — the "handshake" with the amp is already established.
* For Bluetooth Mode:
    * Pair the controller via Bluetooth first (Settings -> Devices -> Pair FootCtrlPlus).
    * Keep the controller paired and switched to the "U" position.
    * The app will handle both the "wake-up" and the MIDI commands wirelessly.

### 3. Run the App
1. Ensure the controller is paired (to trigger the BLE scan).
2. Make sure your `Spark 40` is turned on and NOT connected to the Spark App on your phone (Spark can only talk to one "Master" at a time).
3. Run the `SparMidiBridge.exe`. `Windows`


For **`macOS`** `In work`

4. Wait for the green lights **`PEDAL: READY`** and **`SPARK: ONLINE`**
5. Have fun

## Troubleshooting

In work...

## Source Code
For developers and advanced users, the raw Python scripts are available in the `/lightweight` folder. You can run them directly if you have at least `Python 3.13` installed with the required libraries (bleak, pygame, winrt).

## System Requirements
Tested on: Windows 11

Hardware: Spark 40 Amp, M-VAVE Chocolate Plus

Backend: Bleak (BLE), Pygame (MIDI), winrt
