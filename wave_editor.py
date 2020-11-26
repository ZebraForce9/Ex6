from wave_helper import *
from typing import List
import copy


def get_audio_data(filename: str) -> List[List[int]]:
    return load_wave(filename)[1]


def reverse_audio(audio_data: List[List[int]]) -> List[List[int]]:
    return audio_data[::-1]


def speed_up_audio(audio_data: List[List[int]]) -> List[List[int]]:
    return audio_data[::2]


def slow_down_audio(audio_data: List[List[int]]) -> List[List[int]]:
    new_pairs: int = (len(audio_data)-1)*2
    for i in range(1, new_pairs, 2):
        channel_1: int = int((audio_data[i - 1][0] + audio_data[i][0]) / 2)
        channel_2: int = int((audio_data[i - 1][1] + audio_data[i][1]) / 2)
        audio_data[i:i] = [[channel_1, channel_2]]
    return audio_data


def filter_audio(audio_data: List[List[int]]) -> List[List[int]]:
    new_audio_data = copy.deepcopy(audio_data)
    for i, pair in enumerate(audio_data):
        if i == 0:
            channel_1 = int((pair[0] + audio_data[i + 1][0]) / 2)
            channel_2 = int((pair[1] + audio_data[i + 1][1]) / 2)
            new_audio_data[i] = [channel_1, channel_2]
        elif i == len(audio_data)-1:
            channel_1 = int((pair[0] + audio_data[i - 1][0]) / 2)
            channel_2 = int((pair[1] + audio_data[i - 1][1]) / 2)
            new_audio_data[i] = [channel_1, channel_2]
        else:
            channel_1 = int((pair[0] + audio_data[i - 1][0] + audio_data[i + 1][0]) / 3)
            channel_2 = int((pair[1] + audio_data[i - 1][1] + audio_data[i + 1][1]) / 3)
            new_audio_data[i] = [channel_1, channel_2]
    return new_audio_data
