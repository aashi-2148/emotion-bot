from pyt2s.services import stream_elements
from gtts import gTTS 
import os 
def convert_mp3_to_webm(input_file, bitrate="128k"):
    output_file = input_file.split(".")[0]+".webm"
    print(input_file)
    print(output_file)
    cmd = f"ffmpeg -i {input_file} {output_file} -y"
    print(cmd)
    os.system(cmd)
    os.remove(input_file)
def text_to_speech(ai_generated_response):
    # Convert AI response to speech using gTTS
    tts = gTTS(text=ai_generated_response, lang='en')
    tts.save("response.mp3")  # Save the speech audio as a file
    convert_mp3_to_webm("response.mp3")
text_to_speech()
