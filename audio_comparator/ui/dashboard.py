from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout,
    QGroupBox, QFormLayout, QDoubleSpinBox, QPushButton, QComboBox
)
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
from collections import deque

class TerminalDashboard(QMainWindow):
    """
    A minimalist, terminal-styled GUI to display real-time waveforms.
    """
    
    def __init__(self, block_size: int, audio_manager=None, history_len: int = 60):
        super().__init__()
        self.block_size = block_size
        self.audio_manager = audio_manager
        self.history_len = history_len
        
        # Setup Window
        self.setWindowTitle("MIC COMPARATOR - TERMINAL VIEW")
        self.resize(800, 600)
        self.setStyleSheet("background-color: black; color: #00FF00; font-family: monospace;")
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Info Labels
        self.info_label = QLabel("INITIALIZING DSP...")
        self.info_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.info_label)

        # Source status and retry
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Source: UNKNOWN")
        self.status_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFF00;")
        status_layout.addWidget(self.status_label)

        self.retry_btn = QPushButton("Retry Connection")
        status_layout.addWidget(self.retry_btn)
        self.switch_sim_btn = QPushButton("Switch to Simulated")
        status_layout.addWidget(self.switch_sim_btn)
        layout.addLayout(status_layout)

        # No-data indicator
        self.no_data_label = QLabel("")
        self.no_data_label.setStyleSheet("font-size: 12px; color: #FF0000;")
        layout.addWidget(self.no_data_label)
        
        # Setup PyQtGraph Config (Terminal Green style)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', '#00FF00')
        
        # Plot 1: Mic 1 (waveform)
        self.plot1_widget = pg.PlotWidget(title="MIC 1 (LEFT CHANNEL)")
        self.curve1 = self.plot1_widget.plot(pen=pg.mkPen('#00FF00', width=1))
        self.plot1_widget.setYRange(-1, 1)
        layout.addWidget(self.plot1_widget)

        # Plot 2: Mic 2 (waveform)
        self.plot2_widget = pg.PlotWidget(title="MIC 2 (RIGHT CHANNEL)")
        self.curve2 = self.plot2_widget.plot(pen=pg.mkPen('#00FF00', width=1))
        self.plot2_widget.setYRange(-1, 1)
        layout.addWidget(self.plot2_widget)

        # Time-series section: amplitude and frequency over time for each mic
        ts_box = QGroupBox("Per-second Time Series (updates every second)")
        ts_layout = QHBoxLayout(ts_box)

        # Mic1 amplitude
        self.m1_amp_plot = pg.PlotWidget(title="MIC1 Amplitude (RMS)")
        self.m1_amp_curve = self.m1_amp_plot.plot(pen=pg.mkPen('#00FF00', width=2))
        self.m1_amp_plot.setYRange(0, 1)
        ts_layout.addWidget(self.m1_amp_plot)

        # Mic1 frequency
        self.m1_freq_plot = pg.PlotWidget(title="MIC1 Dominant Frequency (Hz)")
        self.m1_freq_curve = self.m1_freq_plot.plot(pen=pg.mkPen('#00FF00', width=2))
        self.m1_freq_plot.setYRange(0, 5000)
        ts_layout.addWidget(self.m1_freq_plot)

        layout.addWidget(ts_box)

        # Mic2 time series
        ts2_box = QGroupBox("")
        ts2_layout = QHBoxLayout(ts2_box)

        self.m2_amp_plot = pg.PlotWidget(title="MIC2 Amplitude (RMS)")
        self.m2_amp_curve = self.m2_amp_plot.plot(pen=pg.mkPen('#00FF00', width=2))
        self.m2_amp_plot.setYRange(0, 1)
        ts2_layout.addWidget(self.m2_amp_plot)

        self.m2_freq_plot = pg.PlotWidget(title="MIC2 Dominant Frequency (Hz)")
        self.m2_freq_curve = self.m2_freq_plot.plot(pen=pg.mkPen('#00FF00', width=2))
        self.m2_freq_plot.setYRange(0, 5000)
        ts2_layout.addWidget(self.m2_freq_plot)

        layout.addWidget(ts2_box)

        # Discrepancy plot (difference in RMS: mic1 - mic2)
        self.disc_plot = pg.PlotWidget(title="Amplitude Discrepancy (MIC1 - MIC2)")
        self.disc_curve = self.disc_plot.plot(pen=pg.mkPen('#FF0000', width=2))
        self.disc_plot.setYRange(-1, 1)
        layout.addWidget(self.disc_plot)

        # X-axis/time base for history
        self._time_index = deque(maxlen=self.history_len)
        self._m1_amp = deque([0.0]*self.history_len, maxlen=self.history_len)
        self._m1_freq = deque([0.0]*self.history_len, maxlen=self.history_len)
        self._m2_amp = deque([0.0]*self.history_len, maxlen=self.history_len)
        self._m2_freq = deque([0.0]*self.history_len, maxlen=self.history_len)
        self._disc = deque([0.0]*self.history_len, maxlen=self.history_len)

        # Controls for simulation parameters
        ctrl_box = QGroupBox("Simulation Controls")
        ctrl_layout = QFormLayout(ctrl_box)

        self.freq1_spin = QDoubleSpinBox()
        self.freq1_spin.setRange(20.0, 5000.0)
        self.freq1_spin.setValue(440.0)
        self.freq1_spin.setSingleStep(1.0)
        ctrl_layout.addRow("Mic1 Frequency (Hz)", self.freq1_spin)

        self.freq2_spin = QDoubleSpinBox()
        self.freq2_spin.setRange(20.0, 5000.0)
        self.freq2_spin.setValue(442.0)
        self.freq2_spin.setSingleStep(1.0)
        ctrl_layout.addRow("Mic2 Frequency (Hz)", self.freq2_spin)

        self.amp1_spin = QDoubleSpinBox()
        self.amp1_spin.setRange(0.0, 1.0)
        self.amp1_spin.setValue(0.3)
        self.amp1_spin.setSingleStep(0.01)
        ctrl_layout.addRow("Mic1 Amplitude", self.amp1_spin)

        self.amp2_spin = QDoubleSpinBox()
        self.amp2_spin.setRange(0.0, 1.0)
        self.amp2_spin.setValue(0.25)
        self.amp2_spin.setSingleStep(0.01)
        ctrl_layout.addRow("Mic2 Amplitude", self.amp2_spin)

        self.noise_spin = QDoubleSpinBox()
        self.noise_spin.setRange(0.0, 0.5)
        self.noise_spin.setValue(0.005)
        self.noise_spin.setSingleStep(0.001)
        ctrl_layout.addRow("Noise Level", self.noise_spin)

        self.apply_btn = QPushButton("Apply Simulation Settings")
        ctrl_layout.addRow(self.apply_btn)

        # Preset selector
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(["sine", "impulse", "noise", "chirp", "speech"]) 
        self.preset_btn = QPushButton("Apply Preset")
        ctrl_layout.addRow("Preset", self.preset_combo)
        ctrl_layout.addRow(self.preset_btn)

        layout.addWidget(ctrl_box)

        # Connect control signals
        self.apply_btn.clicked.connect(self._apply_sim_settings)
        self.preset_btn.clicked.connect(self._apply_preset)
        self.retry_btn.clicked.connect(self._on_retry)
        self.switch_sim_btn.clicked.connect(self._on_switch_sim)

        # X-axis data (Sample indices)
        self.x_data = np.arange(self.block_size)

        # Timer to refresh time-series UI if needed
        self.ts_timer = QTimer()
        self.ts_timer.setInterval(1000)
        self.ts_timer.timeout.connect(self._refresh_time_series)
        self.ts_timer.start()
        
    def update_graphs(self, mic1_data: np.ndarray, mic2_data: np.ndarray):
        """
        Updates the waveform graphs with new data.
        """
        self.curve1.setData(self.x_data, mic1_data)
        self.curve2.setData(self.x_data, mic2_data)
        
    def update_info(self, text: str):
        """
        Updates the text label.
        """
        self.info_label.setText(text)

    def append_timepoint(self, rms1: float, freq1: float, rms2: float, freq2: float):
        """Append a per-second sample to the history buffers."""
        # Maintain a simple counter-based time index
        idx = (self._time_index[-1] + 1) if len(self._time_index) else 0
        self._time_index.append(idx)
        self._m1_amp.append(rms1)
        self._m1_freq.append(freq1)
        self._m2_amp.append(rms2)
        self._m2_freq.append(freq2)
        self._disc.append(rms1 - rms2)

    def update_source_status(self, simulated: bool, connected: bool = True):
        """Update the source status indicator."""
        # Always enable the switch button so user can toggle modes
        self.switch_sim_btn.setEnabled(True)
        if simulated:
            self.status_label.setText("Source: SIMULATED")
            self.status_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #ffff00;")
            self.retry_btn.setEnabled(True)
            self.switch_sim_btn.setText("Switch to Real")
        else:
            if connected:
                self.status_label.setText("Source: REAL (connected)")
                self.status_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #00FF00;")
                self.retry_btn.setEnabled(False)
            else:
                self.status_label.setText("Source: REAL (no data)")
                self.status_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FF0000;")
                self.retry_btn.setEnabled(True)
            self.switch_sim_btn.setText("Switch to Simulated")

    def set_no_data(self, no_data: bool):
        if no_data:
            self.no_data_label.setText("NO DATA RECEIVED")
        else:
            self.no_data_label.setText("")

    def _refresh_time_series(self):
        """Redraw the time-series plots from buffers."""
        x = np.arange(-len(self._m1_amp)+1, 1)
        self.m1_amp_curve.setData(x, np.array(self._m1_amp))
        self.m1_freq_curve.setData(x, np.array(self._m1_freq))
        self.m2_amp_curve.setData(x, np.array(self._m2_amp))
        self.m2_freq_curve.setData(x, np.array(self._m2_freq))
        self.disc_curve.setData(x, np.array(self._disc))

    def _apply_sim_settings(self):
        if not self.audio_manager:
            return
        f1 = float(self.freq1_spin.value())
        f2 = float(self.freq2_spin.value())
        a1 = float(self.amp1_spin.value())
        a2 = float(self.amp2_spin.value())
        n = float(self.noise_spin.value())
        try:
            self.audio_manager.set_sim_params(freq1=f1, freq2=f2, amp1=a1, amp2=a2, noise=n)
        except Exception:
            pass

    def _apply_preset(self):
        if not self.audio_manager:
            return
        preset = str(self.preset_combo.currentText())
        try:
            self.audio_manager.set_sim_preset(preset)
        except Exception:
            pass

    def _on_retry(self):
        if not self.audio_manager:
            return
        ok = False
        try:
            ok = self.audio_manager.retry_connection()
        except Exception:
            ok = False

        # Update UI based on result
        try:
            sim = self.audio_manager.is_simulated()
        except Exception:
            sim = True
        self.update_source_status(simulated=sim, connected=ok)
        if ok:
            self.info_label.setText("Reconnected to real device.")
        else:
            self.info_label.setText("Retry failed — still simulated or no device.")

    def _on_switch_sim(self):
        if not self.audio_manager:
            return
        # Toggle: if currently simulated, try to switch back to real; otherwise switch to simulated
        try:
            is_sim = self.audio_manager.is_simulated()
        except Exception:
            is_sim = False

        if is_sim:
            # show intermediate no-data state immediately while attempting reconnect
            self.update_source_status(simulated=False, connected=False)
            self.set_no_data(True)

            # attempt to reconnect to real device
            ok = False
            try:
                ok = self.audio_manager.retry_connection()
            except Exception:
                ok = False

            # update UI after attempt
            try:
                sim = self.audio_manager.is_simulated()
            except Exception:
                sim = False
            self.update_source_status(simulated=sim, connected=ok)
            if ok:
                self.info_label.setText("Switched to real device.")
                self.set_no_data(False)
            else:
                self.info_label.setText("Failed to switch to real device.")
        else:
            ok = False
            try:
                ok = self.audio_manager.switch_to_simulation()
            except Exception:
                ok = False
            try:
                sim = self.audio_manager.is_simulated()
            except Exception:
                sim = True
            self.update_source_status(simulated=sim, connected=ok)
            if ok:
                self.info_label.setText("Switched to simulated source.")
            else:
                self.info_label.setText("Failed to switch to simulated source.")