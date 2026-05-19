from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
import queue
import time


@dataclass
class AudioFrame:
    samples: np.ndarray  # shape (block_size, channels)
    sample_rate: int
    timestamp: float


class DataSource(ABC):
    """Abstract data source. Implementations should push AudioFrame into `self.audio_queue`.
    """
    def __init__(self, sample_rate: int, block_size: int, channels: int = 2):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self.audio_queue = queue.Queue(maxsize=10)

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()

    def set_params(self, **kwargs):
        """Optional: update runtime params."""
        return

    def set_preset(self, preset: str):
        """Optional: choose a preset."""
        return
