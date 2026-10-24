import importlib.util
import threading
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).parents[1]
    / "src"
    / "1.2.0. Spark 40, Spark 2, Spark Go"
    / "midi_runtime.py"
)


def load_runtime_class():
    spec = importlib.util.spec_from_file_location("midi_runtime", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MidiRuntime


class FakeInput:
    def __init__(self, events):
        self.events = events
        self.closed = False

    def close(self):
        self.events.append("input.close")
        self.closed = True

    def poll(self):
        return False


class FakeMidi:
    def __init__(self):
        self.events = []
        self.initialized = False

    def init(self):
        self.events.append("midi.init")
        self.initialized = True

    def quit(self):
        self.events.append("midi.quit")
        self.initialized = False

    def get_init(self):
        return self.initialized

    def get_count(self):
        self.events.append("midi.get_count")
        return 1

    def get_device_info(self, index):
        return (b"CoreMIDI", b"M-VAVE Chocolate", 1, 0, 0)

    def Input(self, index):
        self.events.append(f"midi.input:{index}")
        return FakeInput(self.events)


class MidiRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.MidiRuntime = load_runtime_class()

    def setUp(self):
        self.backend = FakeMidi()
        self.runtime = self.MidiRuntime(self.backend)

    def test_repeated_scans_do_not_restart_portmidi(self):
        self.assertEqual(["M-VAVE Chocolate"], self.runtime.list_input_names())
        self.assertEqual(["M-VAVE Chocolate"], self.runtime.list_input_names())

        self.assertEqual(1, self.backend.events.count("midi.init"))
        self.assertNotIn("midi.quit", self.backend.events)

    def test_restart_closes_input_before_reinitializing(self):
        self.runtime.open_input(0)
        self.backend.events.clear()

        self.runtime.restart()

        self.assertEqual(
            ["input.close", "midi.quit", "midi.init"],
            self.backend.events,
        )

    def test_native_backend_is_owned_by_one_thread(self):
        self.runtime.start()
        errors = []

        def use_from_another_thread():
            try:
                self.runtime.list_input_names()
            except RuntimeError as error:
                errors.append(str(error))

        thread = threading.Thread(target=use_from_another_thread)
        thread.start()
        thread.join()

        self.assertEqual(["MIDI backend accessed from multiple threads"], errors)


if __name__ == "__main__":
    unittest.main()
