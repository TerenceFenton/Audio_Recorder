# Libraries
import pyaudio
import os
import shutil
import wave
from pydub import AudioSegment
from datetime import datetime

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATE = 44100
instance = pyaudio.PyAudio()
stream = instance.open(format=FORMAT, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=CHUNK)
now = datetime.now()
time_of_recording = now.strftime("%Y-%m-%d %H:%M:%S")

# Recorder Func
def voice_recorder(CHUNK, RATE, stream):
    frames = []
    seconds = 3
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    instance.terminate()
    return frames

# Save File Func
def save_file(FRAMES):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    instance = pyaudio.PyAudio()
    prompt = input(f'Save File? (Y/N): ')
    real_inputs = ['Y', 'N', 'y', 'n']

    while prompt not in real_inputs:
        print('Please only answer Y or N')
        prompt = input(f'Save File? (Y/N): ')
    
    if prompt == 'Y' or prompt == 'y':
        now = datetime.now()
        time_of_recording = now.strftime("%Y-%m-%d %H:%M:%S")
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

# Interactive Func
def interactive_experience(CHUNK, RATE, stream):
    prompt = input(f'Start Recording? (Y/N): ')
    real_inputs = ['Y', 'N', 'y', 'n']

    while prompt not in real_inputs:
        print('Please only answer Y or N')
        prompt = input(f'Start Recording? (Y/N): ')
    
    if prompt == 'Y' or prompt == 'y':
        print('Recording Sample')
        frames = voice_recorder(CHUNK, RATE, stream)
        print('Recording Complete')
        save_file(frames)

    print('Have a great day')
    

# Moving Parts:
interactive_experience(CHUNK, RATE, stream)