import streamlit as st
from transformers import pipeline
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from audio_recorder_streamlit import audio_recorder
import numpy as np
from scipy.io import wavfile
from io import BytesIO
#import librosa
#import soundfile

checkpoint = "openai/whisper-small.en"  

@st.cache(allow_output_mutation=True)
def model():
    #pipe = pipeline("automatic-speech-recognition", model=checkpoint)
    processor = WhisperProcessor.from_pretrained(checkpoint)
    model = WhisperForConditionalGeneration.from_pretrained(checkpoint)
    return processor, model

audio_bytes = audio_recorder(text="Click Me", recording_color="#e8b62c", neutral_color="#6aa36f", icon_name="user", icon_size="1x", sample_rate = 16_000)

#pipe = model()
processor, model = model()

if audio_bytes:
    new_audio = st.audio(audio_bytes, format="audio/wav")
    #audio_np = np.array(new_audio)
    #data_s16 = np.frombuffer(audio_bytes, dtype=np.int16) #count=len(audio_bytes)//2, offset=0)
    #float_data = data_s16 * 0.5**15
    bytes_io = BytesIO(audio_bytes)
    
    # Read the file sample rate and data using wavfile
    sample_rate, audio_data = wavfile.read(bytes_io)
    audio_input = {"array": np.frombuffer(audio_data[:,0], np.int16).flatten().astype(np.float32) / 32768.0, #audio_data[:,0].astype(np.float32)*(1/32768.0), 
                   "sampling_rate": sample_rate}
    
    input_features = processor(audio_inpuy["array"], sampling_rate=audio_input["sampling_rate"], return_tensors="pt").input_features 
    
    predicted_ids = model.generate(input_features)
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    
    st.write(audio_input)
    st.write(transcription)
    #st.write(pipe(audio_input)["text"])
    
