import numpy as np
import threading
import time
from .base import DataSource, AudioFrame


class SimulatorSource(DataSource):
    def __init__(self, sample_rate: int, block_size: int, channels: int = 2):
        super().__init__(sample_rate, block_size, channels)
        self._running = False
        self._thread = None
        self._phase = 0.0

        # default params
        self.sim_freq1 = 440.0
        self.sim_freq2 = 442.0
        self.sim_amp1 = 0.3
        self.sim_amp2 = 0.25
        self.sim_noise = 0.005
        self.sim_preset = 'sine'

        # state for some presets
        self._impulse_counter = 0
        self._chirp_phase = 0.0

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None

    def _loop(self):
        t_step = self.block_size / float(self.sample_rate)
        while self._running:
            freq1 = float(self.sim_freq1)
            freq2 = float(self.sim_freq2)
            amp1 = float(self.sim_amp1)
            amp2 = float(self.sim_amp2)
            noise = float(self.sim_noise)

            t = (np.arange(self.block_size) / float(self.sample_rate)).astype(np.float32)
            phase1 = 2.0 * np.pi * freq1 * t + self._phase
            phase2 = 2.0 * np.pi * freq2 * t + self._phase * 1.01

            if self.sim_preset == 'sine':
                mic1 = (amp1 * np.sin(phase1)).astype(np.float32)
                mic2 = (amp2 * np.sin(phase2)).astype(np.float32)
            elif self.sim_preset == 'impulse':
                mic1 = (np.random.randn(self.block_size) * (noise * 0.2)).astype(np.float32)
                mic2 = (np.random.randn(self.block_size) * (noise * 0.2)).astype(np.float32)
                self._impulse_counter += 1
                if self._impulse_counter >= int(self.sample_rate / float(self.block_size)):
                    self._impulse_counter = 0
                    idx = np.random.randint(0, max(1, self.block_size-10))
                    mic1[idx:idx+6] += amp1 * np.hanning(6)
                    mic2[idx:idx+6] += amp2 * np.hanning(6)
            elif self.sim_preset == 'noise':
                mic1 = (np.random.randn(self.block_size) * (noise + amp1*0.1)).astype(np.float32)
                mic2 = (np.random.randn(self.block_size) * (noise + amp2*0.1)).astype(np.float32)
            elif self.sim_preset == 'chirp':
                f0 = max(20.0, freq1 - 200)
                f1c = min(self.sample_rate/2 - 100, freq1 + 200)
                sweep = np.linspace(f0, f1c, self.block_size)
                mic1 = (amp1 * np.sin(2.0 * np.pi * sweep * t + self._chirp_phase)).astype(np.float32)
                mic2 = (amp2 * np.sin(2.0 * np.pi * sweep * t + self._chirp_phase*1.02)).astype(np.float32)
                self._chirp_phase += 0.1
            elif self.sim_preset == 'speech':
                carrier1 = np.random.randn(self.block_size).astype(np.float32)
                carrier2 = np.random.randn(self.block_size).astype(np.float32)
                env = 0.3 + 0.7 * (0.5 + 0.5 * np.sin(2.0*np.pi*2.0*t + self._phase))
                mic1 = (amp1 * env * carrier1 * 0.3).astype(np.float32)
                mic2 = (amp2 * env * carrier2 * 0.3).astype(np.float32)
            else:
                mic1 = (amp1 * np.sin(phase1)).astype(np.float32)
                mic2 = (amp2 * np.sin(phase2)).astype(np.float32)

            if self.sim_preset not in ('noise',):
                if noise > 0.0:
                    mic1 += (np.random.randn(self.block_size) * noise).astype(np.float32)
                    mic2 += (np.random.randn(self.block_size) * noise).astype(np.float32)

            interleaved = np.vstack((mic1, mic2)).T
            frame = AudioFrame(samples=interleaved, sample_rate=self.sample_rate, timestamp=time.time())
            try:
                self.audio_queue.put_nowait(frame)
            except Exception:
                pass

            self._phase += 2.0 * np.pi * freq1 * t_step
            self._phase = self._phase % (2.0 * np.pi)
            time.sleep(t_step)

    def set_params(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, 'sim_' + k):
                setattr(self, 'sim_' + k, v)

    def set_preset(self, preset: str):
        self.sim_preset = preset
