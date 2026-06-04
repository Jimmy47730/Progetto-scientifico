import numpy as np
import threading
import time
from audio.sources.sounddevice_source import SoundDeviceSource, list_input_devices


class AudioManager:
    """
    High-level manager that selects a data source for microphone input and provides
    playback utilities. Data sources produce `AudioFrame` objects placed into
    `self.audio_queue`.
    """

    def __init__(self, sample_rate: int = 44100, block_size: int = 512):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = 2

        # device selections (indices or None)
        self._device1 = None
        self._device2 = None
        self._source = SoundDeviceSource(self.sample_rate, self.block_size, self.channels, device1=None, device2=None)
        self._started = False

    def get_input_devices(self):
        """Return available input devices as a list of (index, name)."""
        return list_input_devices()

    def set_devices(self, device1, device2):
        """Set device indices for mic1 and mic2 and recreate the source. If the manager
        was running, the new source will be started automatically when possible."""
        self._device1 = device1
        self._device2 = device2
        # stop previous source
        try:
            if self._source is not None:
                self._source.stop()
        except Exception:
            pass
        # create new source with the chosen devices
        self._source = SoundDeviceSource(self.sample_rate, self.block_size, self.channels, device1=self._device1, device2=self._device2)
        # if previously started, attempt to start new source
        if self._started:
            try:
                self._source.start()
            except Exception:
                self._started = False

    @property
    def audio_queue(self):
        return self._source.audio_queue

    def start_listening(self):
        try:
            self._source.start()
            self._started = True
        except Exception:
            # source failed to start; mark as not started
            self._started = False

    def is_connected(self) -> bool:
        """True if the active source is running and producing frames."""
        return bool(self._started)

    def retry_connection(self) -> bool:
        """Attempt to reinitialize a real audio device source. Returns True on success."""
        try:
            try:
                # recreate source with current device selections
                self._source.stop()
            except Exception:
                pass
            self._source = SoundDeviceSource(self.sample_rate, self.block_size, self.channels, device1=self._device1, device2=self._device2)
            try:
                self._source.start()
                self._started = True
                return True
            except Exception:
                self._started = False
                return False
        except Exception:
            return False

    def stop_listening(self):
        try:
            self._source.stop()
        except Exception:
            pass

    def play_alert_sound(self, frequency: float = 880.0, duration: float = 0.2):
        def _play():
            try:
                import sounddevice as sd
                t = np.linspace(0, duration, int(self.sample_rate * duration), False)
                sine_wave = np.sin(frequency * t * 2 * np.pi).astype(np.float32)
                sd.play(sine_wave, samplerate=self.sample_rate)
            except Exception:
                try:
                    import winsound
                    winsound.Beep(int(frequency), int(duration * 1000))
                except Exception:
                    print("ALERT: beep (no audio backend available)")

        threading.Thread(target=_play, daemon=True).start()
