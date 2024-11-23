# Libraries
import pyaudio
import os
import shutil
import wave
from pydub import AudioSegment
import threading
import time
from pynput import keyboard

# Recording state
recording = False

# Recorder Func
def voice_recorder():
    try:
        # Parameters 
        frames = []
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNEL = 1
        RATE = 44100
        instance = pyaudio.PyAudio()
        stream = instance.open(format=FORMAT, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=CHUNK)
        global recording
        while recording is True:
            data = stream.read(CHUNK, exception_on_overflow = False)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        instance.terminate()
        time.sleep(0.1)
        save_file(frames)  
        pass  
    except Exception as e:
        print(f'Error in voice_recorder: {e}')
        


# Save File Func
def save_file(FRAMES):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    instance = pyaudio.PyAudio()  
    time_of_recording = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(instance.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(FRAMES))
    wf.close()
    download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    sound = AudioSegment.from_wav("output.wav")
    sound.export(f"output{time_of_recording}.mp3", format="mp3")
    shutil.move(f'output{time_of_recording}.mp3', download_path)
    os.remove('output.wav')

# Recorder Input Reviewinator 3000
def recording_input(key):
    global recording
    if key == keyboard.Key.space:
        if not recording:
            recording = True
            print('Voice Recorder Started')
            recording_thread.start()
        else:
            recording = False
            recording_thread.join()
            print('Voice Recording Finished')
            return False

# Thread
recording_thread = threading.Thread(target=voice_recorder)  

# Main
print('Press space to start')
with keyboard.Listener(on_press=recording_input) as listener:
    listener.join()   