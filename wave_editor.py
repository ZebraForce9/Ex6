from wave_helper import *
from typing import List


MODIFY = "1"
COMPOSE = "2"
EXIT = "3"
MAIN_MENU_OPTIONS = "123"
MAX_AUDIO = 32767
MIN_AUDIO = -32768
MODIFICATION_MESSAGE = ("Selects which modification you would like to preform:\n"
                        "1.Reverse audio\n"
                        "2.Negate audio\n"
                        "3.Increase playing speed\n"
                        "4.Decrease playing speed\n"
                        "5.Increase volume\n"
                        "6.Decrease volume\n"
                        "7.Low pass filter\n"
                        "8.Exit to Main Menu\n")



def main():
    """The main function that presents the menu to the user,
    and shows the different options."""

    while True:
        user_input = input("Choose category:\n1.Modify existing wav file\n"
                           "2.Compose a tune\n3.Exit program\n")

        if user_input not in MAIN_MENU_OPTIONS:
            print("Your input is not valid, Choose again")
            continue
        if user_input == MODIFY:
            option_choice = int(input(MODIFICATION_MESSAGE))
            pass

        if user_input == COMPOSE:
            pass

        if user_input == EXIT:
            pass


def sound_negation(audio_list):
    """Receives an audio list, changes the sample values to their opposite number"""
    new_audio_list = []

    for sample in audio_list:
        new_sample = []
        for num in sample:
            new_num = - num
            new_sample.append(adjust_audio_range(new_num))
        new_audio_list.append(new_sample)
    return new_audio_list


def adjust_audio_range(num):
    """Checks if a number fits the audio range, returns the number if it is,
    if not, returns the max/min of the audio range"""

    if num > MAX_AUDIO:
        return MAX_AUDIO
    if num < MIN_AUDIO:
        return MIN_AUDIO
    else:
        return num


def increase_volume(audio_list):
    """Increases all the samples by 1.2"""
    new_sound_list = []

    for sample in audio_list:
        new_sample = []
        for num in sample:
            new_num = num * 1.2
            new_sample.append(adjust_audio_range(int(new_num)))
        new_sound_list.append(new_sample)

    return new_sound_list


def decrease_volume(audio_list):
    """Increases all the samples by 1.2"""
    new_sound_list = []

    for sample in audio_list:
        new_sample = []
        for num in sample:
            new_num = num / 1.2
            new_sample.append(adjust_audio_range(int(new_num)))
        new_sound_list.append(new_sample)

    return new_sound_list


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


def low_pass_filter(audio_data: List[List[int]]) -> List[List[int]]:
    new_audio_data = []
    for i, pair in enumerate(audio_data):
        if i == 0:
            channel_1 = int((pair[0] + audio_data[i + 1][0]) / 2)
            channel_2 = int((pair[1] + audio_data[i + 1][1]) / 2)
            new_audio_data.append([channel_1, channel_2])
        elif i == len(audio_data)-1:
            channel_1 = int((pair[0] + audio_data[i - 1][0]) / 2)
            channel_2 = int((pair[1] + audio_data[i - 1][1]) / 2)
            new_audio_data.append([channel_1, channel_2])
        else:
            channel_1 = int((pair[0] + audio_data[i - 1][0] + audio_data[i + 1][0]) / 3)
            channel_2 = int((pair[1] + audio_data[i - 1][1] + audio_data[i + 1][1]) / 3)
            new_audio_data.append([channel_1, channel_2])
    return new_audio_data
