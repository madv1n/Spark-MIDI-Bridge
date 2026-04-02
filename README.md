# Spark MIDI Bridge

A lightweight, one-click utility to connect any MIDI controller to `Positive Grid Spark` amps using your PC as the "brain".

<div align="center"><img src="https://github.com/user-attachments/assets/8e62b142-152c-44df-bfa0-5c016c707819"></div>
<div align="center"><img src="https://github.com/user-attachments/assets/9191e1df-6f42-42dc-8292-ba02661552dd"></div>

## Versions
| Version | Features |
| :--- | :--- |
| **[v1.1.0 (Latest)](https://github.com/madv1n/Spark-MIDI-Bridge/releases)** | **Spark 2 support, easy mapping mode** |
| **v1.0.2** | **Universal MIDI Support. Now supports every BT/USB Midi** |
| **v1.0.0** | Initial release (M-VAVE only) |

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
5. Easy Mapping (Learn Mode) - Click the LEARN button under any preset and press the physical button on your MIDI controller to link them instantly. This allows you to use your pedal’s current settings without any hardware reconfiguration. (Note: Click SAVE CONFIGURATION to store your custom layout permanently).
6. **Done:** Wait for `SPARK: ONLINE` and `PEDAL: READY`.

For **`macOS`** `In work`

## 🛠 Hardware Compatibility
*I am actively looking for testers for other models!*

| Device | Status | Notes |
| :--- | :--- | :--- |
| **Spark 40** | ✅ Working | Fully tested by developer |
| **Spark 2** | ✅ Working | Supports preset switching |
| **Spark MINI** | ⏳ Testing | Need more data |
| **Spark GO** | ⏳ Testing | Need more data |

## 🧪 How to help
If you own a **MINI, or GO**, you can help even if you don't have a MIDI pedal.

Since different hardware revisions of the Spark series may use varying Internal Model IDs, you might need to calibrate the communication profile:

1. Launch `SparkScanner.exe`: Execute the bridge application and verify the status shows `SPARK: ONLINE`.
2. Protocol Discovery: Click "START SCAN". The utility will cycle through known protocol layers to find a match for your specific hardware.
3. Completion: Observe the Amp's preset LEDs. Once they toggle, press "STOP". The utility will lock the identified Model ID for your configuration.
4. If it doesn't, please [Open an Issue](https://github.com/madv1n/Spark-MIDI-Bridge/issues) and tell me your amp model.

## 📜 Credits & Acknowledgments
This project uses research and protocol documentation from the following open-source projects:
* **[SparkMIDI](https://github.com/paulhamsh/SparkMIDI)** — for the original Sysex command structures.

## ⚖️ Legal Disclaimer & Safety

**USE THIS SOFTWARE AT YOUR OWN RISK.** 1. **Not Official:** This project is an independent, community-driven tool and is **NOT affiliated with, authorized, maintained, or endorsed by Positive Grid LLC**. 
2. **Trademarks:** "Spark", "Positive Grid", "Spark LIVE", and all related product names are trademarks or registered trademarks of Positive Grid LLC. They are used here solely for **interoperability** and identification purposes.
3. **No Liability:** The author is not responsible for any potential damage to your amplifier, MIDI hardware, computer, or for any loss of data.
4. **Experimental:** Support for newer models (Spark 2, Spark LIVE) is based on community research and is considered **experimental**.
5. **Testing:** Always test your setup thoroughly before using it in a live performance or critical environment.

This software is provided "as is" under the **GPL-3.0 License**, without warranty of any kind.

## Support my project
If this tool helps you, you can support further development:

<a href="https://www.buymeacoffee.com/pk_rpforge" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px;width: 217px !important;" ></a>
