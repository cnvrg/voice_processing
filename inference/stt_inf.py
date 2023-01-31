# Copyright (c) 2023 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

'''voice processing inference'''
import os
import pathlib
import requests
from pytube import YouTube
import iso639
import whisper

def yt_vid_to_audio(url):
    '''
    download the audio file either from youtube or s3

    Parameters
    ----------
    url : URL to the youtube video to be converted and used as an audio input

    Returns
    -------
    out_file : converted youtube vid to audio file

    '''
    # url input from user
    yt_ = YouTube(str(url))
    # extract only audio
    video = yt_.streams.filter(only_audio=True).first()

    # check for destination to save file
    destination = str(pathlib.Path(__file__).parent.resolve())
    print(destination)
    # download the file
    out_file = video.download(output_path=destination, filename = 'audio.wav')

    return out_file

def download_test_file(url_):
    """
    Downloads the model files if they are not already present or
    pulled as artifacts from a previous train task
    """
    current_dir = str(pathlib.Path(__file__).parent.resolve())
    if not os.path.exists(current_dir + f'/{url_}') and not os.path.exists('/input/cnn/' + url_):
        print(f'Downloading file: {url_}')
        response = requests.get(url_)
        file = url_.split("/")[-1]
        path_ = os.path.join(current_dir, file)
        with open(path_, "wb") as file_:
            file_.write(response.content)


def predict(audio_file):
    '''

    Parameters
    ----------
    audio_file : audio file containing speech

    Returns
    -------
    text extracted from the sudio file
    '''
### SCALE TEST DATA ###
    print('Running Stand Alone Endpoint')
    script_dir = pathlib.Path(__file__).parent.resolve()
    audio_f = str(audio_file['file'])
    lang = str(audio_file['language'])
    model_size = str(audio_file['model_size'])

    if 'www.youtube.com' in audio_f:
        audio_file = yt_vid_to_audio(audio_f)
        name = 'audio.wav'
    else:
        download_test_file(audio_f)
        name = audio_f.rsplit("/", maxsplit=1)[-1]

    file_name = os.path.join(script_dir,name)
    dic = {}

    model = whisper.load_model(model_size)

    result = model.transcribe(file_name, task='transcribe', fp16=False,
                              language=iso639.to_iso639_1(lang))
    # print the recognized text
    dic = result['text']
    return dic

print(predict({'file':'https://libhub-readme.s3.us-west-2.amazonaws.com/voice_processing/french.mp4',
                'language':'english',
                'model_size':'large'}))