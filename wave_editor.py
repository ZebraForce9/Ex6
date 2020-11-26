from wave_helper import *
from typing import List


def reverse_audio(filename: str):
    audio_data: List[List[int]] = load_wave(filename)[1]
    return audio_data[::-1]
