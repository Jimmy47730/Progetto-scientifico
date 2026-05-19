import sys
import threading
import time
from PyQt6.QtWidgets import QApplication

from main import ApplicationController

def run_demo():
    app = QApplication(sys.argv)
    controller = ApplicationController(simulate=True)
    controller.run()

    def cycle_presets():
        presets = ['sine', 'chirp', 'noise', 'impulse', 'speech']
        while True:
            for p in presets:
                controller.audio_manager.set_sim_preset(p)
                # reflect in UI if available
                try:
                    controller.ui.preset_combo.setCurrentText(p)
                except Exception:
                    pass
                time.sleep(4)

    t = threading.Thread(target=cycle_presets, daemon=True)
    t.start()

    sys.exit(app.exec())

if __name__ == '__main__':
    run_demo()
