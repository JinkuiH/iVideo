'''
Author: JinkuiH jinkui7788@gmail.com
Date: 2023-06-23 18:40:50
LastEditors: JinkuiH jinkui7788@gmail.com
LastEditTime: 2023-06-23 19:04:05
FilePath: \iVideo\gen_video.py
Description: 将文本转换为音频

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''

import os
import azure.cognitiveservices.speech as speechsdk
from scipy.io.wavfile import write as write_wav
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription='1455ca4ec9d348619288470a048380c3', region='eastasia')
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='zh-CN-XiaochenNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

root = 'answears'
savePath = 'audio'
questionList = os.listdir(root)
for question in questionList:
    questionPath = os.path.join(root, question)
    answearList = os.listdir(questionPath)
    for answear in answearList:
        with open(os.path.join(questionPath,answear), 'r') as file:
            contents = file.read()
            speech_synthesis_result = speech_synthesizer.speak_text_async(contents).get()
            stream = speechsdk.AudioDataStream(speech_synthesis_result)
            saveTo = os.path.join(savePath, question)
            if not os.path.exists(saveTo):
                os.makedirs(saveTo)
            stream.save_to_wav_file(os.path.join(saveTo, '{}.wav'.format(answear)))

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")