import os
import sys
import json
import threading
import asyncio
import pygame.midi
import multiprocessing

# Windows-specific imports
try:
    import winrt.windows.devices.midi as midi
    import winrt.windows.devices.enumeration as enumeration
    from winrt.windows.storage.streams import DataReader
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False

from bleak import BleakScanner, BleakClient
import tkinter as tk
from tkinter import ttk, messagebox

# Configuration
CONFIG_FILE = "spark_config.json"
WRITE_UUID = "0000ffc1-0000-1000-8000-00805f9b34fb"
SPARK_MAC_PREFIX = "F7:EB:ED"

# Базовый шаблон команды
PRESET_TEMPLATE = "01fe000053fe1a000000000000000000f0013a1501{:02x}0000{:02x}f7"

class SparkMidiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spark MIDI Bridge")
        self.root.geometry("570x360")
        self.root.configure(bg="#f5f5f5")
        
        if os.path.exists("icon.ico"):
            try: self.root.iconbitmap("icon.ico")
            except: pass
        
        self.amp_model = tk.StringVar(value="Spark 40")
        self.mapping = { f"btn{i}": tk.StringVar(value=f"Preset {(i % 4) + 1}") for i in range(0, 128) }
        
        self.spark_client = None
        self.midi_usb_in = None    
        self.midi_bt_port = None   
        
        pygame.midi.init()
        self.load_config()
        self.setup_ui()
        
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()
        
        asyncio.run_coroutine_threadsafe(self.spark_search_loop(), self.loop)
        asyncio.run_coroutine_threadsafe(self.midi_search_loop(), self.loop)

    def get_hex_command(self, action_name):
        try:
            num_part = ''.join(filter(str.isdigit, action_name))
            preset_idx = int(num_part) - 1
            preset_idx = max(0, min(3, preset_idx))
            
            protocol_byte = 0x38 if self.amp_model.get() == "Spark 40" else 0x0a
            return PRESET_TEMPLATE.format(protocol_byte, preset_idx)
        except:
            return None

    def setup_ui(self):
        main = tk.Frame(self.root, bg="#f5f5f5")
        main.pack(expand=True, fill="both")
        
        tk.Label(main, text="SPARK MIDI BRIDGE", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)
        
        model_frame = tk.Frame(main, bg="#f5f5f5")
        model_frame.pack(pady=5)
        tk.Label(model_frame, text="Amp Model:", bg="#f5f5f5", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        model_combo = ttk.Combobox(model_frame, textvariable=self.amp_model, values=["Spark 40", "Mini / GO / Spark 2"], state="readonly", width=15)
        model_combo.pack(side="left", padx=5)

        st_frame = tk.Frame(main, bg="#f5f5f5")
        st_frame.pack(pady=2)
        self.midi_lbl = tk.Label(st_frame, text="PEDAL: DISCONNECTED", fg="#c0392b", bg="#f5f5f5", font=("Arial", 9, "bold"))
        self.midi_lbl.pack(side="left", padx=20)
        self.spark_lbl = tk.Label(st_frame, text="SPARK: DISCONNECTED", fg="#c0392b", bg="#f5f5f5", font=("Arial", 9, "bold"))
        self.spark_lbl.pack(side="left", padx=20)

        grid = tk.Frame(main, bg="white", relief="groove", borderwidth=1)
        grid.pack(pady=10, padx=20, fill="x")
        
        preset_list = ["Preset 1", "Preset 2", "Preset 3", "Preset 4"]
        letters = ["A", "B", "C", "D"]
        for i in range(0, 4):
            f = tk.Frame(grid, bg="white")
            f.pack(side="left", expand=True, pady=10)
            tk.Label(f, text=f"BTN {i} ({letters[i]})", bg="white", font=("Arial", 8, "bold")).pack()
            ttk.Combobox(f, textvariable=self.mapping[f"btn{i}"], values=preset_list, width=10, state="readonly").pack(padx=5, pady=5)

        tk.Button(main, text="SAVE CONFIGURATION", command=self.save_config, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=20).pack(pady=10)
        
        self.log_box = tk.Text(main, height=10, font=("Consolas", 9), state="disabled", bg="white", fg="black")
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)

    def log(self, msg):
        self.root.after(0, self._log, msg)

    def _log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def send_to_spark(self, btn_id, status=None):
        msg_type = "PC" if (status and 192 <= status <= 207) else "CC"
        
        key = f"btn{btn_id}"
        if key not in self.mapping:
            self.mapping[key] = tk.StringVar(value="Preset 1")
            self.log(f"New ID detected: {btn_id}. Added to mapping.")

        action_name = self.mapping[key].get()
        hex_data = self.get_hex_command(action_name)
        
        if hex_data:
            self.log(f"Action: {msg_type} {btn_id} -> {action_name} ({self.amp_model.get()})")
            if self.spark_client and self.spark_client.is_connected:
                try:
                    await self.spark_client.write_gatt_char(WRITE_UUID, bytes.fromhex(hex_data), response=False)
                except Exception as e:
                    self.log(f"Send Error: {e}")

    def on_bt_midi_message(self, sender, args):
        if not IS_WINDOWS: return
        try:
            reader = DataReader.from_buffer(args.message.raw_data)
            data = [reader.read_byte() for _ in range(reader.unconsumed_buffer_length)]
            if len(data) >= 2:
                status, data1 = data[0], data[1]
                if (176 <= status <= 207):
                    asyncio.run_coroutine_threadsafe(self.send_to_spark(data1, status), self.loop)
        except: pass

    async def spark_search_loop(self):
        while True:
            if not self.spark_client or not self.spark_client.is_connected:
                try:
                    self.spark_lbl.config(text="SPARK: SCANNING", fg="#f39c12")
                    devs = await BleakScanner.discover(timeout=4.0)
                    target = None
                    for d in devs:
                        name = str(d.name if d.name else "Unknown").lower()
                        address = str(d.address).upper()
                        if "spark" in name or address.startswith(SPARK_MAC_PREFIX):
                            target = d
                            break
                    
                    if target:
                        self.log(f"Connecting to: {target.name}")
                        self.spark_client = BleakClient(target.address)
                        await self.spark_client.connect()
                        self.spark_lbl.config(text="SPARK: ONLINE", fg="#27ae60")
                        self.log("Spark connection established.")
                except:
                    self.spark_lbl.config(text="SPARK: DISCONNECTED", fg="#c0392b")
                    self.spark_client = None
            await asyncio.sleep(5)

    async def midi_search_loop(self):
        while True:
            if not self.midi_usb_in:
                for i in range(pygame.midi.get_count()):
                    info = pygame.midi.get_device_info(i)
                    if info and info[2] and any(x in info[1].decode().lower() for x in ["foot", "midi", "m-vave"]):
                        try:
                            self.midi_usb_in = pygame.midi.Input(i)
                            self.log(f"Wired Pedal Linked: {info[1].decode()}")
                            self.midi_lbl.config(text="PEDAL: USB READY", fg="#27ae60")
                        except: self.midi_usb_in = None
            
            if self.midi_usb_in:
                try:
                    if self.midi_usb_in.poll():
                        for event in self.midi_usb_in.read(10):
                            status, data1 = event[0][0], event[0][1]
                            if (176 <= status <= 207):
                                await self.send_to_spark(data1, status)
                except:
                    self.midi_usb_in = None
                    self.midi_lbl.config(text="PEDAL: DISCONNECTED", fg="#c0392b")
                    self.log("Wired Pedal disconnected.")

            if IS_WINDOWS and not self.midi_bt_port and not self.midi_usb_in:
                try:
                    all_devs = await enumeration.DeviceInformation.find_all_async()
                    target = next((d for d in all_devs if d.name and any(x in d.name.lower() for x in ["footctrl", "m-vave"]) and "midi" in d.name.lower()), None)
                    if target:
                        port = await midi.MidiInPort.from_id_async(target.id)
                        if port:
                            self.midi_bt_port = port
                            self.midi_bt_port.add_message_received(self.on_bt_midi_message)
                            self.midi_lbl.config(text="PEDAL: BT READY", fg="#27ae60")
                            self.log(f"Wireless Pedal Linked: {target.name}")
                except: pass
            await asyncio.sleep(0.1)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    d = json.load(f)
                    if "amp_model" in d: self.amp_model.set(d["amp_model"])
                    for k,v in d.items(): 
                        if k in self.mapping: self.mapping[k].set(v)
            except: pass

    def save_config(self):
        config_data = {k: v.get() for k, v in self.mapping.items()}
        config_data["amp_model"] = self.amp_model.get()
        with open(CONFIG_FILE, "w") as f: 
            json.dump(config_data, f)
        messagebox.showinfo("Success", "Configuration saved!")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = SparkMidiApp(root)
    root.mainloop()