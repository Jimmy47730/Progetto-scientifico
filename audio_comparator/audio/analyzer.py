import numpy as np
from scipy.fft import rfft, rfftfreq

class AudioAnalyzer:
    """
    Class responsible for mathematical analysis of audio data.
    It calculates amplitude and dominant frequency.
    """
    
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    def calculate_rms(self, audio_data: np.ndarray) -> float:
        """
        Calculates the Root Mean Square (RMS) of the audio buffer to determine amplitude/volume.
        """
        # Avoid division by zero or errors with empty arrays
        if len(audio_data) == 0:
            return 0.0
            
        # Calculate RMS
        rms = np.sqrt(np.mean(audio_data**2))
        return float(rms)

    def calculate_dominant_frequency(self, audio_data: np.ndarray) -> float:
        """
        Calculates the dominant frequency using Fast Fourier Transform (FFT).
        Applies a Hanning window to prevent spectral leakage.
        """
        if len(audio_data) == 0:
            return 0.0

        # Apply Hanning window
        windowed_data = audio_data * np.hanning(len(audio_data))
        
        # Calculate FFT
        fft_result = np.abs(rfft(windowed_data))
        frequencies = rfftfreq(len(windowed_data), d=1.0/self.sample_rate)
        
        # Find the peak frequency
        peak_index = np.argmax(fft_result)
        dominant_freq = frequencies[peak_index]
        
        return float(dominant_freq)