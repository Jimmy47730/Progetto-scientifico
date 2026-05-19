import time
from .base import DataSource, AudioFrame
try:
    import sounddevice as sd
    _HAS_SOUNDDEVICE = True
except Exception:
    sd = None
    _HAS_SOUNDDEVICE = False


class SoundDeviceSource(DataSource):
    def __init__(self, sample_rate: int, block_size: int, channels: int = 2):
        super().__init__(sample_rate, block_size, channels)
        self._stream = None

    def _callback(self, indata, frames, timeinfo, status):
        if status:
            print(f"Audio Callback Status/Error: {status}")
        try:
            # Wrap into AudioFrame
            frame = AudioFrame(samples=indata.copy(), sample_rate=self.sample_rate, timestamp=time.time())
            self.audio_queue.put_nowait(frame)
        except Exception:
            pass

    def start(self):
        if not _HAS_SOUNDDEVICE:
            raise RuntimeError("sounddevice not available")
        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                channels=self.channels,
                callback=self._callback
            )
            self._stream.start()
        except Exception as e:
            raise

    def stop(self):
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None
