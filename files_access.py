"""
Run http server of file store:: python -m http.server 1212
"""

import requests


def return_spectrogram(file_name):

    resp = requests.get(f"http://localhost:1212/spectrograms/{file_name}.png")
    img_bytes = resp.content

    return img_bytes


def return_audio(file_name):

    resp = requests.get(f"http://localhost:1212/audio/{file_name}.wav")
    wav_bytes = resp.content

    return wav_bytes


if __name__ == "__main__":
    return_audio("blues00000")
