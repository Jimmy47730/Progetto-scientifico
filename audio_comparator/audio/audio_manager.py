import numpy as np
import threading
import time
from audio.sources.simulator_source import SimulatorSource
from audio.sources.sounddevice_source import SoundDeviceSource


class AudioManager:
    """
    High-level manager that selects a data source for microphone input and provides
    playback utilities. Data sources produce `AudioFrame` objects placed into
    `self.audio_queue`.
    """

    def __init__(self, sample_rate: int = 44100, block_size: int = 512, simulate: bool = False):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = 2

        # choose source
        self._simulate = simulate
        self._source = None
        self._started = False
        self._init_source()

    def _init_source(self):
        # Prefer real device unless simulate flag set
        if not self._simulate:
            try:
                # create sounddevice-backed source but don't start it yet
                self._source = SoundDeviceSource(self.sample_rate, self.block_size, self.channels)
            except Exception:
                # sounddevice not available at all -> fallback to simulator
                self._source = SimulatorSource(self.sample_rate, self.block_size, self.channels)
        else:
            # if simulation requested, use simulator
            if self._simulate:
                self._source = SimulatorSource(self.sample_rate, self.block_size, self.channels)

    @property
    def audio_queue(self):
        return self._source.audio_queue

    def start_listening(self):
        try:
            self._source.start()
            self._started = True
        except Exception:
            # do not automatically switch to simulator; keep real source but mark as not started
            self._started = False

    def is_simulated(self) -> bool:
        """Return True if currently using the simulator source."""
        from audio.sources.simulator_source import SimulatorSource
        return self._simulate or isinstance(self._source, SimulatorSource)

    def is_connected(self) -> bool:
        """True if the active source is running and producing frames (or simulator)."""
        # simulator is always considered connected
        from audio.sources.simulator_source import SimulatorSource
        if isinstance(self._source, SimulatorSource):
            return True
        return bool(self._started)

    def retry_connection(self) -> bool:
        """Attempt to reinitialize a real audio device source. Returns True on success."""
        try:
            # If current source is simulator, try to create a real one
            if self.is_simulated():
                candidate = SoundDeviceSource(self.sample_rate, self.block_size, self.channels)
                try:
                    self._source.stop()
                except Exception:
                    pass
                self._source = candidate
                self._source.start()
                self._started = True
                self._simulate = False
                return True

            # If current source is real but not started, try to start it
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

    def set_sim_params(self, **kwargs):
        # delegate to source if it supports
        try:
            self._source.set_params(**kwargs)
        except Exception:
            pass

    def set_sim_preset(self, preset: str):
        try:
            self._source.set_preset(preset)
        except Exception:
            pass

    def switch_to_simulation(self):
        """Replace the current source with the simulator and start it."""
        try:
            # stop current source if running
            try:
                self._source.stop()
            except Exception:
                pass
            # create and start simulator source
            self._source = SimulatorSource(self.sample_rate, self.block_size, self.channels)
            self._source.start()
            self._simulate = True
            self._started = True
            return True
        except Exception:
            return False

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
