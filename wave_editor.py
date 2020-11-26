from wave_helper import *
from typing import List


def get_audio_data(filename: str) -> List[List[int]]:
    return load_wave(filename)[1]


def reverse_audio(audio_data: List[List[int]]) -> List[List[int]]:
    return audio_data[::-1]


def speed_up_audio(audio_data: List[List[int]]) -> List[List[int]]:
    return audio_data[::2]
