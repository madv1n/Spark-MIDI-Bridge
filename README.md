# Spark MIDI Bridge

A lightweight, one-click utility to connect any MIDI controller to `Positive Grid Spark` amps using your PC as the "brain".

<div align="center"><img src="https://github.com/user-attachments/assets/8e62b142-152c-44df-bfa0-5c016c707819"></div>
<div align="center"><img src="https://github.com/user-attachments/assets/c947fedc-e054-4d34-92a9-4afb963a397c"></div>

## Versions
| Version | Features | Status | Recommended for |
| :--- | :--- | :--- | :--- |
| **[v1.0.2. (Latest)](https://github.com/madv1n/Spark-MIDI-Bridge/releases)** | **Universal MIDI Support** | **Stable** | **Everyone (Best choice)** | | **Universa MIDI Support** | **Stable** | **Everyone (Best choice)** |
| **v1.0.0.** | Initial release (M-VAVE only) | Legacy | Only for M-VAVE Chocolate |

## Getting Started

### 1. Download Files
1.  Click the green **`<> Code`** button at the top of this page. or dowload file from Release Page *[(Latest version)](https://github.com/madv1n/Spark-MIDI-Bridge/releases)*
2.  Select **`Download ZIP`**.
3.  Extract the archive to a convenient folder.

## 📖 Quick Start

> [!IMPORTANT]
> **For M-VAVE Users:** You **MUST** pair your pedal via Windows Bluetooth settings (`FootCtrlPlus` device) **even if you are using a USB connection**. 
> If you don't pair it, the pedal will constantly enter "searching mode" (blinking light), which can cause connection instability and lag. Pairing it once ensures the pedal stays "locked" and stable.

1. **Prepare your Amp:** Turn on your Spark. Ensure it's **NOT** connected to the Spark mobile app.
2. **Connect MIDI:** Plug your controller into the PC (USB is recommended for stability).
3. **Run:** Open `SparkMidiBridge.exe`.
4. Select the amp model from the drop-down list.
5. **Done:** Wait for `SPARK: ONLINE` and `PEDAL: READY`.

`Ensure your pedal buttons send unique IDs (0, 1, 2, 3 or 1, 2, 3, 4) via CubeSuite. If the app sees the same "Button ID" for all presses, check your pedal's CC/PC settings`
    
For **`macOS`** `In work`

## 🛠 Hardware Compatibility
*I am actively looking for testers for other models!*

| Device | Status | Notes |
| :--- | :--- | :--- |
| **Spark 40** | ✅ Working | Fully tested by developer |
| **Spark 2** | ⏳ Testing | Should connect automatically. Need data! |
| **Spark MINI** | ⏳ Testing | Need confirmation on Bluetooth ID. |
| **Spark GO** | ⏳ Testing | Need confirmation on Bluetooth ID. |
| **M-VAVE Chocolate** | ✅ Working | Best experience via USB or Bluetooth. |

## 🧪 How to help
If you own a **Spark 2, MINI, or GO**, you can help even if you don't have a MIDI pedal:
1. Run the app with your amp turned on.
2. Change the amp model from the drop-down list
2. Wait and check if the log says `SPARK: ONLINE`.
3. If it doesn't, please [Open an Issue](https://github.com/madv1n/Spark-MIDI-Bridge/issues) and tell me your amp model and how it's named in your Windows Bluetooth settings.

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
