"""
Run http server of file store:: python -m http.server 1212
"""

import requests
import io


def return_signed_url(name):
    """
    returns signed url after request to Cloud Function. URL valid for 1 min.
    :param name: header passed in request. pass entire path to file from root of Bucket.
    :return: signed url for file
    """

    params = {"name": name}
    resp = requests.get("https://asia-south1-feature-music-selection.cloudfunctions.net/request_file", params=params)

    return resp.content


def return_spectrogram(file_name):

    # resp = requests.get(f"http://localhost:1212/display_spectrograms/{file_name}")
    url = return_signed_url(f"display_spectrograms/{file_name}")
    resp = requests.get(url, verify=True)
    img_bytes = resp.content

    return img_bytes


def return_audio(file_name):

    # resp = requests.get(f"http://localhost:1212/audio/{file_name}")
    url = return_signed_url(f"audio/{file_name}")
    resp = requests.get(url, verify=True)
    wav_bytes = resp.content

    return wav_bytes


def return_np_encoding(file_name):

    # resp = requests.get(f"http://localhost:1212/encodings/{file_name}")
    url = return_signed_url(f"encodings/{file_name}")
    resp = requests.get(url, verify=True)
    enc_bytes = io.BytesIO(resp.content)

    return enc_bytes


if __name__ == "__main__":
    return_signed_url("display_spectrograms/blues00005.png")
