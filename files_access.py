"""
Run http server of file store:: python -m http.server 1212
"""

import requests
import io


def return_spectrogram(file_name):

    resp = requests.get(f"http://localhost:1212/display_spectrograms/{file_name}")
    img_bytes = resp.content

    return img_bytes


def return_audio(file_name):

    resp = requests.get(f"http://localhost:1212/audio/{file_name}")
    wav_bytes = resp.content

    return wav_bytes


def return_np_encoding(file_name):

    resp = requests.get(f"http://localhost:1212/encodings/{file_name}")
    enc_bytes = io.BytesIO(resp.content)

    return enc_bytes


if __name__ == "__main__":
    return_audio("blues00000")
