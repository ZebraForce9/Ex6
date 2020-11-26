from wave_helper import *
from typing import List


def get_audio_data(filename: str) -> List[List[int]]:
    return load_wave(filename)[1]


def reverse_audio(audio_data: List[List[int]]) -> List[List[int]]:
    return audio_data[::-1]


def speed_up_audio(audio_data: List[List[int]]) -> List[List[int]]:
    return audio_data[::2]


def slow_down_audio(audio_data: List[List[int]]) -> List[List[int]]:
    new_pairs: int = (len(audio_data)-1)*2
    for i in range(1, new_pairs, 2):
        channel_one = (audio_data[i-1][0] + audio_data[i][0]) // 2
        channel_two = (audio_data[i-1][1] + audio_data[i][1]) // 2
        audio_data[i:i] = [[channel_one, channel_two]]
    return audio_data
