import speech_recognition as sr
import pyttsx3
import os
from google.cloud import texttospeech
from google.cloud import texttospeech_v1
import streamlit as st
from textblob import TextBlob
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration
import regex as re


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "keys.json"


menu = ["Home","Modules","About"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.title("AML 2404 - AI and ML Lab")
    st.subheader("NLP Apps for Communication Domain")

    st.markdown('### Business Problem Statement:')
    problem_statemnt = '<p style="font-family:sans-serif; font-size: 18px;">As technology increases rapidly, the focus on developing communication skills has been neglected. Many people worldwide face this issue with communication in their daily activities, like conversations with new people, sending large texts via messages/mail, implications due to new languages, etc.</p>'
    st.markdown(problem_statemnt, unsafe_allow_html=True)

    st.markdown('### Modules:')
    st.markdown('##### Speech to Text')
    st.markdown('##### Text to Speech')
    st.markdown('##### Text Summarization')
    st.markdown('##### Sentiment Analysis')

elif choice == "Modules":
    action = st.radio("Please select your module:", ('text to speech','speech to text','Sentiment Analysis','Text Summarization'))


    if action == 'text to speech':
        st.subheader("Text to speech")
        text = st.text_input("Enter text")
        out_lang = st.selectbox(
            "Select your output language",
            ("English", "Hindi", "Telugu", "Tamil","Malayalam", "Bengali"),
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
                language_code="en-In", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
            # Select the type of audio file you want returned
            audio_config = texttospeech_v1.AudioConfig(
                # https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1#audioencoding
                audio_encoding=texttospeech_v1.AudioEncoding.MP3)
            # Perform text-to-speech request on the text input with the selected voice parameters and audio file type
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            # returning response's audio_content as binary.
            return response.audio_content,translation
        display_output_text = st.checkbox("Display output text")
        if st.button("Transcribe"):
            if not text:
                st.warning("Please fill out text input")
            else:
                audio_bytes,output_text=text_to_speech(text,output_language)
                st.markdown(f"### Your audio:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                if display_output_text:
                    st.markdown(f"### Output text:")
                    st.write(f" {output_text}")

    if action == 'speech to text':
            st.subheader("Speech to Text")

            in_lang = st.selectbox(
                "Select your input language",
                ("English", "Hindi","Telugu", "Tamil","Malayalam", "Bengali"),
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
            # elif in_lang == "korean":
            #     input_language = "ko"
            # elif in_lang == "Chinese":
            #     input_language = "zh-cn"
            # elif in_lang == "Japanese":
            #     input_language = "ja"

            out_lang = st.selectbox(
                "Select your output language",
                ("English", "Hindi","Telugu", "Tamil","Malayalam", "Bengali"),
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
            # elif out_lang == "korean":
            #     output_language = "ko"
            # elif out_lang == "Chinese":
            #     output_language = "zh-cn"
            # elif out_lang == "Japanese":
            #     output_language = "ja"


            try:
                def translate(text, to_language):
                    from google.cloud import translate_v2 as translate
                    translate_client = translate.Client()

                    if isinstance(text, bytes):
                        text = text.decode('utf-8')

                    # Text can also be a sequence of strings, in which case this method
                    # will return a sequence of results for each text.
                    result = translate_client.translate(
                        text, target_language=to_language)

                    print(u'Text: {}'.format(result['input']))
                    print(u'Translation: {}'.format(result['translatedText']))

                    return result['translatedText']

                def speech_to_text(input_language1,output_language1):
                    listener = sr.Recognizer()
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[1].id)
                    engine.setProperty("rate", 140)
                    engine.say("Hi there! I am Listening")
                    engine.runAndWait()
                    with sr.Microphone() as source:
                        listener.adjust_for_ambient_noise(source)
                        print("Listening...")
                        audio = listener.listen(source)
                        text = listener.recognize_google(audio, language=input_language1)
                        translation = translate(text, output_language1)
                    return translation
                if st.button("🎙️"):
                    output_text = speech_to_text(input_language,output_language)
                    st.markdown(f'###Output Text:')
                    st.write(f'{output_text}')
            except sr.UnknownValueError:
                print("Sorry, I did not get that. Please try again.")
            except sr.RequestError:
                print("Sorry, my service is down. Please try after some time")


    if action == 'Sentiment Analysis':
        def convert_to_df(sentiment):
            sentiment_dict = {'polarity': sentiment.polarity, 'subjectivity': sentiment.subjectivity}
            sentiment_df = pd.DataFrame(sentiment_dict.items(), columns=['metric', 'value'])
            return sentiment_df


        def analyze_token_sentiment(docx):
            analyzer = SentimentIntensityAnalyzer()
            pos_list = []
            neg_list = []
            neu_list = []
            for i in docx.split():
                res = analyzer.polarity_scores(i)['compound']
                if res > 0.1:
                    pos_list.append(i)
                    pos_list.append(res)

                elif res <= -0.1:
                    neg_list.append(i)
                    neg_list.append(res)
                else:
                    neu_list.append(i)

            result = {'positives': pos_list, 'negatives': neg_list, 'neutral': neu_list}
            return result


        def sentiment_analysis():
                st.title("Sentiment Analysis NLP App")

                with st.form(key='nlpForm'):
                    text = st.text_area("Enter Text Here")
                    submit_button = st.form_submit_button(label='Analyze')

                # layout
                col1, col2 = st.columns(2)
                if submit_button:
                    if not text:
                        st.warning("Please fill out input text")
                    else:
                        res = bool(re.match('[a-zA-Z\s]+$', text))
                        if res:
                            with col1:
                                st.info("Results")
                                sentiment = TextBlob(text).sentiment
                                st.write(sentiment)

                                # Emoji
                                if sentiment.polarity > 0:
                                    st.markdown("Sentiment:: Positive :smiley: ")
                                elif sentiment.polarity < 0:
                                    st.markdown("Sentiment:: Negative :angry: ")
                                else:
                                    st.markdown("Sentiment:: Neutral 😐 ")

                                # Dataframe
                                result_df = convert_to_df(sentiment)
                                st.dataframe(result_df)

                                # Visualization
                                c = alt.Chart(result_df).mark_bar().encode(
                                    x='metric',
                                    y='value',
                                    color='metric')
                                st.altair_chart(c, use_container_width=True)

                            with col2:
                                st.info("Token Sentiment")

                                token_sentiments = analyze_token_sentiment(text)
                                st.write(token_sentiments)
                        else:
                            st.warning('Enter Valid input containing only strings')
        sentiment_analysis()
    if action == 'Text Summarization':

        st.title('Text Summarization Demo')
        st.markdown('Using BART and T5 transformer model')

        model = st.selectbox('Select the model', ('BART', 'T5'))

        if model == 'BART':
            _num_beams = 4
            _no_repeat_ngram_size = 3
            _length_penalty = 1
            _min_length = 12
            _max_length = 128
            _early_stopping = True
        else:
            _num_beams = 4
            _no_repeat_ngram_size = 3
            _length_penalty = 2
            _min_length = 30
            _max_length = 200
            _early_stopping = True

        col1, col2, col3 = st.columns(3)
        _num_beams = col1.number_input("num_beams", value=_num_beams)
        _no_repeat_ngram_size = col2.number_input("no_repeat_ngram_size", value=_no_repeat_ngram_size)
        _length_penalty = col3.number_input("length_penalty", value=_length_penalty)

        col1, col2, col3 = st.columns(3)
        _min_length = col1.number_input("min_length", value=_min_length)
        _max_length = col2.number_input("max_length", value=_max_length)
        _early_stopping = col3.number_input("early_stopping", value=_early_stopping)

        text = st.text_area('Text Input')


        def run_model(input_text):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

            if model == "BART":
                bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
                bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
                input_text = str(input_text)
                input_text = ' '.join(input_text.split())
                input_tokenized = bart_tokenizer.encode(input_text, return_tensors='pt').to(device)
                summary_ids = bart_model.generate(input_tokenized,
                                                  num_beams=_num_beams,
                                                  no_repeat_ngram_size=_no_repeat_ngram_size,
                                                  length_penalty=_length_penalty,
                                                  min_length=_min_length,
                                                  max_length=_max_length,
                                                  early_stopping=_early_stopping)

                output = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g
                          in
                          summary_ids]
                st.write('Summary')
                st.success(output[0])

            else:
                t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
                t5_tokenizer = T5Tokenizer.from_pretrained("t5-base")
                input_text = str(input_text).replace('\n', '')
                input_text = ' '.join(input_text.split())
                input_tokenized = t5_tokenizer.encode(input_text, return_tensors="pt").to(device)
                summary_task = torch.tensor([[21603, 10]]).to(device)
                input_tokenized = torch.cat([summary_task, input_tokenized], dim=-1).to(device)
                summary_ids = t5_model.generate(input_tokenized,
                                                num_beams=_num_beams,
                                                no_repeat_ngram_size=_no_repeat_ngram_size,
                                                length_penalty=_length_penalty,
                                                min_length=_min_length,
                                                max_length=_max_length,
                                                early_stopping=_early_stopping)
                output = [t5_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in
                          summary_ids]
                st.write('Summary')
                st.success(output[0])


        if st.button('Submit'):
            if not text:
                st.warning("Please fill out input text")
            else:
                run_model(text)


elif(choice == 'About'):
    st.info('Efforts by:')
    st.markdown('Bhanu Prakash Mahadevuni C0850515')
    st.markdown('Deeksha Naikap C0835440')
    st.markdown('Pramod Reddy Gurrala C0850493')
    st.markdown('Sai Varun Kollipara C0828403')




