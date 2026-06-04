import sys
import queue
import argparse
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import our custom modules
from audio.audio_manager import AudioManager
from audio.analyzer import AudioAnalyzer
from ui.dashboard import TerminalDashboard
from audio.sources.base import AudioFrame

# Constants
SAMPLE_RATE = 44100
# 512 samples at 44.1kHz = ~11.6 milliseconds
BLOCK_SIZE = 512 

class ApplicationController:
    """
    Main controller linking Audio Manager, Analyzer, and UI.
    """
    def __init__(self):
        # Initialize sub-systems
        self.audio_manager = AudioManager(sample_rate=SAMPLE_RATE, block_size=BLOCK_SIZE)
        self.analyzer = AudioAnalyzer(sample_rate=SAMPLE_RATE)
        self.ui = TerminalDashboard(block_size=BLOCK_SIZE, audio_manager=self.audio_manager)
        
        # Status variables to prevent continuous speaker triggering
        self.sound_cooldown = 0
        
        # Setup the QTimer loop (runs every 10ms)
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_audio_queue)
        self.timer.start(10) # 10 milliseconds interval

        # Storage for most recent per-block analysis values
        self.last_rms1 = 0.0
        self.last_rms2 = 0.0
        self.last_freq1 = 0.0
        self.last_freq2 = 0.0
        self.last_frame_time = None

        # Timer to push per-second aggregated samples to the UI time-series
        self.second_timer = QTimer()
        self.second_timer.timeout.connect(self.push_timepoint)
        self.second_timer.start(1000)

    def process_audio_queue(self):
        """
        Pulls data from the audio callback queue and processes it.
        """
        try:
            # Get the latest audio block from the queue
            # indata shape is (512, 2)
            item = self.audio_manager.audio_queue.get_nowait()
            # Accept either AudioFrame objects or raw numpy arrays for backward compatibility
            if isinstance(item, AudioFrame):
                indata = item.samples
            else:
                indata = item

            # Extract channels
            mic1_data = indata[:, 0]
            mic2_data = indata[:, 1]
            
            # 1. Update Graphs
            self.ui.update_graphs(mic1_data, mic2_data)

            # mark that we received a frame
            try:
                import time as _time
                self.last_frame_time = _time.time()
            except Exception:
                self.last_frame_time = None
            
            # 2. Analyze Audio
            rms1 = self.analyzer.calculate_rms(mic1_data)
            rms2 = self.analyzer.calculate_rms(mic2_data)
            
            freq1 = self.analyzer.calculate_dominant_frequency(mic1_data)
            freq2 = self.analyzer.calculate_dominant_frequency(mic2_data)
            
            # 3. Update UI Text
            info_text = (
                f"MIC 1 -> Amp: {rms1:.4f} | Freq: {freq1:.1f} Hz\n"
                f"MIC 2 -> Amp: {rms2:.4f} | Freq: {freq2:.1f} Hz"
            )
            self.ui.update_info(info_text)
            
            # 4. Compare and Trigger Speaker (Example Logic)
            self.handle_comparison_logic(rms1, rms2)
            # update last values for time-series
            self.last_rms1 = rms1
            self.last_rms2 = rms2
            self.last_freq1 = freq1
            self.last_freq2 = freq2
            
        except queue.Empty:
            # No new audio data available yet, just pass
            pass

    def handle_comparison_logic(self, rms1: float, rms2: float):
        """
        Compares microphones and triggers speaker if needed.
        """
        # Decrease cooldown timer
        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1
            
        # Example condition: If Mic 1 is significantly louder than Mic 2
        # and amplitude is above a noise floor threshold (e.g., 0.05)
        NOISE_FLOOR = 0.05
        
        if rms1 > NOISE_FLOOR and rms1 > (rms2 * 1.5):
            if self.sound_cooldown == 0:
                # Trigger a beep at 880Hz (A5)
                # self.audio_manager.play_alert_sound(frequency=880.0)
                # Set cooldown to ~50 loops (about 500ms) to avoid spamming the speaker
                self.sound_cooldown = 50 

    def run(self):
        """
        Starts the application flow.
        """
        # Populate device list in UI
        try:
            devices = self.audio_manager.get_input_devices()
            self.ui.populate_device_list(devices)
        except Exception:
            pass
        
        self.audio_manager.start_listening()
        # Update source status on startup
        try:
            conn = self.audio_manager.is_connected()
            self.ui.update_source_status(connected=conn)
        except Exception:
            pass
        self.ui.show()

    def push_timepoint(self):
        """Called every second to append last-block metrics to the UI time-series."""
        try:
            # Append timepoint
            self.ui.append_timepoint(self.last_rms1, self.last_freq1, self.last_rms2, self.last_freq2)

            # Check for no-data condition (no frames in last ~1.0s)
            import time as _time
            no_data = True
            if self.last_frame_time is not None and (_time.time() - self.last_frame_time) < 1.0:
                no_data = False

            # Update UI source status and no-data indicator
            try:
                conn = self.audio_manager.is_connected()
                self.ui.update_source_status(connected=conn)
                if no_data:
                    self.ui.set_no_data(True)
                else:
                    self.ui.set_no_data(False)
            except Exception:
                pass

        except Exception:
            pass

    def cleanup(self):
        """
        Properly closes streams when the application exits.
        """
        self.audio_manager.stop_listening()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Comparator")
    args, remaining = parser.parse_known_args()

    # Initialize the Qt Application
    app = QApplication(remaining)
    
    # Initialize our Controller
    controller = ApplicationController()

    controller.run()

    # Execute the Qt Event Loop
    exit_code = app.exec()

    # Cleanup after closing the window
    controller.cleanup()
    sys.exit(exit_code)