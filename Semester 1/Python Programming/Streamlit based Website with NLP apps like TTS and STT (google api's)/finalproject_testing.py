import speech_recognition as sr
import pyttsx3
import os
from google.cloud import texttospeech
from google.cloud import texttospeech_v1
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "keys.json"

action = st.radio("What would you like to do?", ('speech to text','text to speech'))


if action == 'text to speech':
    st.title("Text to speech")

    text = st.text_input("Enter text")

    out_lang = st.selectbox(
        "Select your output language",
        ("English", "Hindi", "Telugu", "Tamil","Malayalam", "Bengali", "korean", "Chinese", "Japanese"),
    )
    if out_lang == "English":
        output_language = "en"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Telugu":
        output_language = "te"
    elif out_lang == "Tamil":
        output_language = "ta"
    elif out_lang == "Malayalam":
        output_language = "ml"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "korean":
        output_language = "ko"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Japanese":
        output_language = "ja"


    # Instantiates a client
    client = texttospeech_v1.TextToSpeechClient()


    def translate(text, language):
        from google.cloud import translate_v2 as translate
        translate_client = translate.Client()

        if isinstance(text, bytes):
            text = text.decode('utf-8')

        result = translate_client.translate(
            text, target_language=language)

        print(u'Text: {}'.format(result['input']))
        print(u'Translation: {}'.format(result['translatedText']))

        print(u'Detected source language: {}'.format(
            result['detectedSourceLanguage'])
        )
        return result['translatedText']

    def text_to_speech(input_text,output_language):

        translation = translate(input_text, output_language)
        synthesis_input = texttospeech_v1.SynthesisInput(text=translation)

        voice = texttospeech_v1.VoiceSelectionParams(
            language_code="en-GB", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech_v1.AudioConfig(
            # https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1#audioencoding
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # returning response's audio_content as binary.
        return response.audio_content,translation

    display_output_text = st.checkbox("Display output text")

    if st.button("convert"):
        audio_bytes,output_text=text_to_speech(text,output_language)
        st.markdown(f"## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        if display_output_text:
            st.markdown(f"## Output text:")
            st.write(f" {output_text}")

if action == 'speech to text' :
    st.title("Speech to Text")
    in_lang = st.selectbox(
        "Select your input language",
        ("English", "Hindi","Telugu", "Tamil","Malayalam", "Bengali", "korean", "Chinese", "Japanese"),
    )
    if in_lang == "English":
        input_language = "en"
    elif in_lang == "Hindi":
        input_language = "hi"
    elif in_lang == "Telugu":
        input_language = "te"
    elif in_lang == "Tamil":
        input_language = "ta"
    elif in_lang == "Malayalam":
        input_language = "ml"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "korean":
        input_language = "ko"
    elif in_lang == "Chinese":
        input_language = "zh-cn"
    elif in_lang == "Japanese":
        input_language = "ja"

    out_lang = st.selectbox(
        "Select your output language",
        ("English", "Hindi","Telugu", "Tamil","Malayalam", "Bengali", "korean", "Chinese", "Japanese"),
    )
    if out_lang == "English":
        output_language = "en"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Telugu":
        output_language = "te"
    elif out_lang == "Tamil":
        output_language = "ta"
    elif out_lang == "Malayalam":
        output_language = "ml"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "korean":
        output_language = "ko"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Japanese":
        output_language = "ja"


    try:
        def translate(text, language):
            from google.cloud import translate_v2 as translate
            translate_client = translate.Client()

            if isinstance(text, bytes):
                text = text.decode('utf-8')

            # Text can also be a sequence of strings, in which case this method
            # will return a sequence of results for each text.
            result = translate_client.translate(
                text, target_language=language)

            print(u'Text: {}'.format(result['input']))
            print(u'Translation: {}'.format(result['translatedText']))

            return result['translatedText']

        def speech_input(input_language1,output_language1):
            listener = sr.Recognizer()
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty("rate", 150)
            engine.say("Hi there! I am your converter. Please input your speech")
            engine.runAndWait()
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = listener.listen(source)
                text = listener.recognize_google(audio, language=input_language1)
                translation = translate(text, output_language1)
            return translation
        if st.button("🎙️"):
            output_text = speech_input(input_language,output_language)
            st.markdown(f'#Output Text:')
            st.write(f'{output_text}')
    except sr.UnknownValueError:
        print("Sorry, I did not get that")
    except sr.RequestError:
        print("Sorry, my service is down")
