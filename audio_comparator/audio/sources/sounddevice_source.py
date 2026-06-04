import time
import threading
import queue
from .base import DataSource, AudioFrame

try:
    import sounddevice as sd
    _HAS_SOUNDDEVICE = True
except Exception:
    sd = None
    _HAS_SOUNDDEVICE = False


def list_input_devices():
    """Return a list of (index, name) for available input-capable devices.
    If `sounddevice` is not available, returns an empty list."""
    if not _HAS_SOUNDDEVICE:
        return []
    devs = []
    try:
        for i, d in enumerate(sd.query_devices()):
            if d.get('max_input_channels', 0) > 0:
                devs.append((i, d.get('name', str(i))))
    except Exception:
        return []
    return devs


class SoundDeviceSource(DataSource):
    """A data source that can capture either a single multi-channel InputStream
    or two separate device inputs (one channel each) and emits interleaved
    stereo `AudioFrame` objects on `self.audio_queue`.
    """
    def __init__(self, sample_rate: int, block_size: int, channels: int = 2, device1=None, device2=None):
        super().__init__(sample_rate, block_size, channels)
        self._streams = []
        self._device1 = device1
        self._device2 = device2
        self._running = False
        self._combiner_thread = None
        self._q1 = queue.Queue(maxsize=8)
        self._q2 = queue.Queue(maxsize=8)

    def _single_callback(self, indata, frames, timeinfo, status):
        if status:
            # don't spam, but keep a simple print for debugging
            print(f"Audio Callback Status/Error: {status}")
        try:
            frame = AudioFrame(samples=indata.copy(), sample_rate=self.sample_rate, timestamp=time.time())
            self.audio_queue.put_nowait(frame)
        except Exception:
            pass

    def _cb1(self, indata, frames, timeinfo, status):
        if status:
            print(f"Device1 status: {status}")
        try:
            self._q1.put_nowait(indata.copy())
        except Exception:
            pass

    def _cb2(self, indata, frames, timeinfo, status):
        if status:
            print(f"Device2 status: {status}")
        try:
            self._q2.put_nowait(indata.copy())
        except Exception:
            pass

    def _combiner_loop(self):
        # Combine matching blocks from _q1 and _q2 into stereo frames
        import numpy as np
        while self._running:
            try:
                a = self._q1.get(timeout=0.1)
                b = self._q2.get(timeout=0.1)
                try:
                    # ensure shapes are (block_size, 1) or (block_size,)
                    a = a.reshape(self.block_size, -1)[:, 0]
                    b = b.reshape(self.block_size, -1)[:, 0]
                    interleaved = np.vstack((a, b)).T.astype('float32')
                    frame = AudioFrame(samples=interleaved, sample_rate=self.sample_rate, timestamp=time.time())
                    try:
                        self.audio_queue.put_nowait(frame)
                    except Exception:
                        pass
                except Exception:
                    pass
            except queue.Empty:
                continue

    def start(self):
        if not _HAS_SOUNDDEVICE:
            raise RuntimeError("sounddevice not available")

        # If both device1 and device2 are provided and they are different,
        # open two single-channel streams and combine them.
        try:
            self._running = True
            self._streams = []
            # lazy import numpy to avoid heavy import if sd unavailable
            import numpy as np

            if self._device1 is not None and self._device2 is not None and self._device1 != self._device2:
                s1 = sd.InputStream(samplerate=self.sample_rate, blocksize=self.block_size,
                                     channels=1, device=self._device1, callback=self._cb1)
                s2 = sd.InputStream(samplerate=self.sample_rate, blocksize=self.block_size,
                                     channels=1, device=self._device2, callback=self._cb2)
                s1.start(); s2.start()
                self._streams = [s1, s2]
                # start combiner thread
                self._combiner_thread = threading.Thread(target=self._combiner_loop, daemon=True)
                self._combiner_thread.start()
            else:
                # single stream mode (either device1==device2 or devices not specified)
                device = self._device1 if self._device1 is not None else None
                s = sd.InputStream(samplerate=self.sample_rate, blocksize=self.block_size,
                                    channels=self.channels, device=device, callback=self._single_callback)
                s.start()
                self._streams = [s]
        except Exception:
            # ensure running flag is reset on failure
            self._running = False
            raise

    def stop(self):
        self._running = False
        try:
            for s in self._streams:
                try:
                    s.stop(); s.close()
                except Exception:
                    pass
        except Exception:
            pass
        self._streams = []
        try:
            if self._combiner_thread is not None:
                self._combiner_thread.join(timeout=0.5)
        except Exception:
            pass
        self._combiner_thread = None
