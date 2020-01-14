#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from google.cloud import texttospeech

from utils import save_data, load_data

client = texttospeech.TextToSpeechClient()

voices = [
    "ja-JP-Wavenet-A",
    "ja-JP-Wavenet-B",
    "ja-JP-Wavenet-C",
    "ja-JP-Wavenet-D",
]

def text_to_speech(text: str, path: str): 
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    for i, voice_name in enumerate(voices):
        voice = texttospeech.types.VoiceSelectionParams(
            name=voice_name,
            language_code='ja-JP')
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        with open(path + "_v{}.mp3".format(i), 'wb') as out:
            out.write(response.audio_content)

def main():
    entries = load_data()
    base_path = os.path.join("C:\\", "Users", "40057686", "OneDrive", "JPN5000_Audio2")
    os.makedirs(base_path)

    for entry in entries:
        id = int(entry["data"]["entry_id"])
        audio_filename = "{0:04d}_entry".format(id)
        text_to_speech(entry["data"]["entry_name"], os.path.join(base_path, audio_filename))

        for i, example in enumerate(entry["examples"]):
            audio_filename = "{0:04d}_example_{1}".format(id, i)
            text_to_speech(example["jp"], os.path.join(base_path, audio_filename))
    print("Complete!")


if __name__ == "__main__":
    main()



