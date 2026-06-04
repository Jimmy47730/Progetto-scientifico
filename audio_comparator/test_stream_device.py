import time
from audio.audio_manager import AudioManager
from audio.sources.sounddevice_source import list_input_devices

print('Available devices:', list_input_devices())

am = AudioManager()
# Try to set a specific device index known from the previous list
device_index = 27
print('Setting devices to', device_index)
am.set_devices(device_index, device_index)

print('Started before:', am._started)
try:
    am.start_listening()
    print('Started after start_listening:', am._started)
except Exception as e:
    print('Start failed exception:', e)

ok = False
for i in range(5):
    try:
        item = am.audio_queue.get(timeout=1)
        if hasattr(item, 'samples'):
            print('Got frame with samples shape:', item.samples.shape)
        else:
            print('Got item:', type(item))
        ok = True
        break
    except Exception as e:
        print('No frame yet:', e)

print('Result ok:', ok)
try:
    am.stop_listening()
except Exception:
    pass
