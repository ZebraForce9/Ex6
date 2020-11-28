from wave_helper import *
from typing import List, Tuple
import os


MODIFY = "1"
COMPOSE = "2"
EXIT = "3"
MAIN_MENU_OPTIONS = "123"
MAX_AUDIO = 32767
MIN_AUDIO = -32768
MODIFICATION_MESSAGE = ("\nSelect which modification you would like to preform:\n"
                        "1.Reverse audio\n"
                        "2.Negate audio\n"
                        "3.Increase playing speed\n"
                        "4.Decrease playing speed\n"
                        "5.Increase volume\n"
                        "6.Decrease volume\n"
                        "7.Low pass filter\n"
                        "8.Exit to Main Menu\n")


def main() -> None:
    """
    Show the main menu to the user.

    Returns:
        None
    """

    while True:
        user_input = input("\nChoose category:\n1.Modify existing wav file\n"
                           "2.Compose a tune\n3.Exit program\n")

        if user_input not in MAIN_MENU_OPTIONS:
            print("Your input is not valid, choose again.\n")
            continue

        if user_input == MODIFY:
            sample_rate, audio_data = receive_audio_file()
            while True:
                option_choice = int(input(MODIFICATION_MESSAGE))
                if option_choice == 8:  # todo: added
                    wave_filename = input("Enter file name in which you want to save your data: ")
                    save_wave(sample_rate, audio_data, wave_filename)
                    break
                else:
                    audio_data = audio_modification(audio_data, option_choice)

        if user_input == COMPOSE:
            print("Feature not supported yet.\n")

        if user_input == EXIT:
            return


def receive_audio_file() -> Tuple[int, List[List[int]]]:
    """
    Get the file path of the wav file from user, check if it exists, and returns the sample rate and audio data.

    Returns:

    """

    while True:
        wav_file: str = input("Enter a wav file path: ")
        if not os.path.isfile(wav_file):
            print("The file does not exist, try again.\n")
        else:
            return extract_audio(wav_file)


def audio_modification(audio_data: List[List[int]], option_choice: int):
    """
    Modify audio data according to user input.

    Args:
        audio_data: A list of audio samples in two channels.
        option_choice: The choice of the user.

    Returns:
        The modified list.
    """

    if option_choice == 1:
        return reverse_audio(audio_data)
    if option_choice == 2:
        return negate_audio(audio_data)
    if option_choice == 3:
        return speed_up_audio(audio_data)
    if option_choice == 4:
        return slow_down_audio(audio_data)
    if option_choice == 5:
        return increase_volume(audio_data)
    if option_choice == 6:
        return decrease_volume(audio_data)
    if option_choice == 7:
        return low_pass_filter(audio_data)
    else:
        print("Your choice is not valid.")
        return audio_data  # todo: necessary?


def extract_audio(filename: str) -> Tuple[int, List[List[int]]]:
    """
    Get the audio samples from a wav file.

    Args:
        filename: The path to the wav file.

    Returns:
        A tuple containing the sample rate and a list of the audio samples in two channels.
    """
    return load_wave(filename)[0], load_wave(filename)[1]


def reverse_audio(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Reverse audio data.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    return audio_data[::-1]


def speed_up_audio(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Speed up audio data.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    return audio_data[::2]


def slow_down_audio(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Slow down audio data.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    new_pairs: int = (len(audio_data)-1)*2
    for i in range(1, new_pairs, 2):
        channel_1: int = int((audio_data[i - 1][0] + audio_data[i][0]) / 2)
        channel_2: int = int((audio_data[i - 1][1] + audio_data[i][1]) / 2)
        audio_data[i:i] = [[channel_1, channel_2]]
    return audio_data


def adjust_audio_range(num: int) -> int:
    """
    Check if a number fits the audio range. Return it if it is, return the max/min of the audio range if not.

    Args:
        num: A value of a sample we check.

    Returns:
        The number if it's in the range, max/min value if not.
    """

    if num > MAX_AUDIO:
        return MAX_AUDIO
    if num < MIN_AUDIO:
        return MIN_AUDIO
    else:
        return num


def negate_audio(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Changes the sample values in the audio data to their opposite number.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    new_audio_data: List[List[int]] = []

    for sample in audio_data:
        new_sample = []
        for num in sample:
            new_num = - num
            new_sample.append(adjust_audio_range(new_num))
        new_audio_data.append(new_sample)
    return new_audio_data


def increase_volume(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Increase all the samples by 1.2.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    new_audio_data: List[List[int]] = []

    for sample in audio_data:
        new_sample = []
        for num in sample:
            new_num = num * 1.2
            new_sample.append(adjust_audio_range(int(new_num)))
        new_audio_data.append(new_sample)

    return new_audio_data


def decrease_volume(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Decrease all the samples by 1.2.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    new_audio_data = []

    for sample in audio_data:
        new_sample = []
        for num in sample:
            new_num = num / 1.2
            new_sample.append(adjust_audio_range(int(new_num)))
        new_audio_data.append(new_sample)

    return new_audio_data


def low_pass_filter(audio_data: List[List[int]]) -> List[List[int]]:
    """
    Use a low pass filter on the audio data.

    Args:
        audio_data: A list of audio samples in two channels.

    Returns:
        The modified list.
    """
    new_audio_data: List[List[int]] = []
    for i, pair in enumerate(audio_data):
        if i == 0:
            channel_1: int = int((pair[0] + audio_data[i + 1][0]) / 2)
            channel_2: int = int((pair[1] + audio_data[i + 1][1]) / 2)
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


if __name__ == '__main__':
    main()