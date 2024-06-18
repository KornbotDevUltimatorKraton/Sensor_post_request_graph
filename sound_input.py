import json 
import requests
import sounddevice as sd
# Define the callback function to process audio data
current_sound = [] 
package_sound = []
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    if any(indata):
        # 'indata' contains the audio input raw values as a NumPy ndarray
        #print(indata.tolist())
        #print(len(indata.tolist()))
        current_sound.append(len(indata.tolist()))
        if len(current_sound) >2:
                     current_sound.remove(current_sound[0])
        for s in indata.tolist():
                  package_sound.append(s[0]) 
                  if len(package_sound) > current_sound[0]:
                                package_sound.remove(package_sound[0])
        data = {"kornbot380@hotmail.com":{"Sound_sensor":{"mic_1":package_sound}}}                    
        print(package_sound)
        try: 
            #res_mic = requests.post("http://192.168.50.192:5899/sensor_request",json=data)   
            res_mic = requests.post("https://roboreactor.com/sensor_request",json=data)   
        except:
            print("Error server loose connection")

# Set the audio parameters
sample_rate = 44100  # Sample rate in Hz

# Open an input stream and start capturing audio in a loop
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Recording... (Press Ctrl+C to stop)")
    try:
        while True:
            pass  # Continuously capture audio until Ctrl+C is pressed
    except KeyboardInterrupt:
        print("\nRecording stopped.")


