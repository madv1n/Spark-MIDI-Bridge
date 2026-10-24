import threading


class MidiRuntime:
    """Own PortMidi on one thread and restart it only on explicit refresh."""

    def __init__(self, midi_backend):
        self._midi = midi_backend
        self._owner_thread = None
        self.input = None

    def _claim_thread(self):
        thread_id = threading.get_ident()
        if self._owner_thread is None:
            self._owner_thread = thread_id
        elif self._owner_thread != thread_id:
            raise RuntimeError("MIDI backend accessed from multiple threads")

    def start(self):
        self._claim_thread()
        if not self._midi.get_init():
            self._midi.init()

    def close_input(self):
        self._claim_thread()
        if self.input is not None:
            try:
                self.input.close()
            finally:
                self.input = None

    def restart(self):
        self._claim_thread()
        self.close_input()
        if self._midi.get_init():
            self._midi.quit()
        self._midi.init()

    def input_devices(self):
        self.start()
        devices = []
        for index in range(self._midi.get_count()):
            info = self._midi.get_device_info(index)
            if info and info[2]:
                name = info[1].decode(errors="replace").strip().replace("\x00", "")
                devices.append((index, name))
        return devices

    def list_input_names(self):
        return [name for _, name in self.input_devices()]

    def open_input(self, index):
        self._claim_thread()
        self.close_input()
        self.start()
        self.input = self._midi.Input(index)
        return self.input

    def read(self, limit=10):
        self._claim_thread()
        if self.input is None or not self.input.poll():
            return []
        return self.input.read(limit)

    def shutdown(self):
        self._claim_thread()
        self.close_input()
        if self._midi.get_init():
            self._midi.quit()
