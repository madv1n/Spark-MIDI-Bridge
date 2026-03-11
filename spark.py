import os
import sys
import subprocess
import json
import threading
import asyncio

def install_dependencies():
    required = ['bleak', 'pygame', 'Pillow']
    for lib in required:
        try:
            __import__(lib.lower() if lib != 'Pillow' else 'PIL')
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_dependencies()

import pygame.midi
from bleak import BleakScanner, BleakClient
import tkinter as tk
from tkinter import ttk, messagebox

CONFIG_FILE = "spark_config.json"
WRITE_UUID = "0000ffc1-0000-1000-8000-00805f9b34fb"
SPARK_ACTIONS = {
    "Preset 1": "01fe000053fe1a000000000000000000f0013a150138000000f7",
    "Preset 2": "01fe000053fe1a000000000000000000f0013a150138000001f7",
    "Preset 3": "01fe000053fe1a000000000000000000f0013a150138000002f7",
    "Preset 4": "01fe000053fe1a000000000000000000f0013a150138000003f7",
}

class SparkMidiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spark MIDI Bridge")
        self.root.geometry("570x320") # Компактнее
        self.mapping = { f"btn{i}": tk.StringVar(value=f"Preset {i}") for i in range(1, 6) }
        self.load_config()
        self.setup_ui()
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()
        asyncio.run_coroutine_threadsafe(self.main_bridge_loop(), self.loop)

    def setup_ui(self):
        main = tk.Frame(self.root, bg="#f5f5f5")
        main.pack(expand=True, fill="both")
        tk.Label(main, text="SPARK MIDI BRIDGE", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=5)
        
        st_frame = tk.Frame(main, bg="#f5f5f5")
        st_frame.pack(pady=2)
        self.midi_lbl = tk.Label(st_frame, text="MIDI: OFF", fg="#c0392b", bg="#f5f5f5", font=("Arial", 9, "bold"))
        self.midi_lbl.pack(side="left", padx=10)
        self.spark_lbl = tk.Label(st_frame, text="SPARK: OFF", fg="#c0392b", bg="#f5f5f5", font=("Arial", 9, "bold"))
        self.spark_lbl.pack(side="left", padx=10)

        grid = tk.Frame(main, bg="white", relief="groove", borderwidth=1)
        grid.pack(pady=10, padx=10, fill="x")
        for i in range(1, 5):
            f = tk.Frame(grid, bg="white")
            f.pack(side="left", expand=True, pady=10)
            tk.Label(f, text=f"BTN {i}", bg="white", font=("Arial", 7, "bold")).pack()
            ttk.Combobox(f, textvariable=self.mapping[f"btn{i}"], values=list(SPARK_ACTIONS.keys()), width=10, state="readonly").pack(padx=2, pady=2)

        tk.Button(main, text="SAVE", command=self.save_config, bg="#2ecc71", fg="white", font=("Arial", 9, "bold")).pack(pady=5)
        self.log_box = tk.Text(main, height=6, font=("Consolas", 8), state="disabled", bg="#eee")
        self.log_box.pack(padx=10, pady=5, fill="x")

    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"> {msg}\n")
        if int(self.log_box.index('end-1c').split('.')[0]) > 50: self.log_box.delete('1.0', '2.0')
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def save_config(self):
        with open(CONFIG_FILE, "w") as f: json.dump({k: v.get() for k, v in self.mapping.items()}, f)
        messagebox.showinfo("OK", "Saved!")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    d = json.load(f)
                    for k,v in d.items(): 
                        if k in self.mapping: self.mapping[k].set(v)
            except: pass

    async def main_bridge_loop(self):
        pygame.midi.init()
        midi_in, client = None, None
        while True:
            if not midi_in:
                for i in range(pygame.midi.get_count()):
                    info = pygame.midi.get_device_info(i)
                    if info and info[2] and any(x in info[1].decode().lower() for x in ["foot", "midi", "m-vave", "sinco"]):
                        try:
                            midi_in = pygame.midi.Input(i)
                            self.midi_lbl.config(text="MIDI: READY", fg="#27ae60")
                            break
                        except: pass
            else:
                try:
                    if not pygame.midi.get_device_info(midi_in.device_id): raise Exception()
                except:
                    midi_in.close(); midi_in = None
                    self.midi_lbl.config(text="MIDI: OFF", fg="#c0392b")

            if not client or not client.is_connected:
                try:
                    devs = await BleakScanner.discover(timeout=2.0)
                    spark = next((d for d in devs if d.name and "Spark" in d.name), None)
                    if spark:
                        client = BleakClient(spark.address)
                        await client.connect()
                        self.spark_lbl.config(text="SPARK: ONLINE", fg="#27ae60")
                        self.log(f"Connected to Spark")
                except: self.spark_lbl.config(text="SPARK: OFF", fg="#c0392b")

            if midi_in and client and client.is_connected:
                try:
                    if midi_in.poll():
                        for event in midi_in.read(10):
                            key = f"btn{event[0][1]}"
                            if key in self.mapping:
                                action = self.mapping[key].get()
                                await client.write_gatt_char(WRITE_UUID, bytes.fromhex(SPARK_ACTIONS[action]), response=False)
                                self.log(f"Sent: {action}")
                except: pass
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SparkMidiApp(root)
    root.mainloop()