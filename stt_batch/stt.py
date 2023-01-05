'''Voice Processing using whisper'''
import warnings
import os
import argparse
from pytube import YouTube
import iso639
import whisper
warnings.filterwarnings(action='ignore')
cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")


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
    destination = '.'
    print(destination)
    # download the file
    out_file = video.download(output_path=destination, filename = 'audio.wav')
    # result of success
    print(yt_.title + " has been successfully downloaded.")

    return out_file

def get_audio_file(speech):
    '''
    get the audio file
    Returns
    -------
    audio_file : return audio file either from the youtube link or the s3 link

    '''
    if 'https://www.youtube.com' in speech:
        print('Downloading youtube link')
        audio_file = yt_vid_to_audio(speech)
    else:
        audio_file = speech
    print(audio_file)

    return audio_file

def speech_to_text(audio_file, model_size, language):
    '''
    convert speech to text

    Parameters
    ----------
    audio_file : speech to text audio file

    Returns
    -------
    result : text output from the model

    '''
    model = whisper.load_model(model_size)
    language = iso639.to_iso639_1(language)
    result = model.transcribe(audio_file, task='transcribe', fp16=False, language=language)
    # print the recognized text
    print(result['text'])

    return result

def save_text_file(result):
    '''
    save the text file

    Parameters
    ----------
    result : final text file from the audio input

    Returns
    -------
    Save the text file

    '''
    path = os.path.join(cnvrg_workdir,'speech_to_text.txt')
    with open(path, 'w') as file_:
        file_.write(result['text'])

def argument_parser():
    '''
    parser arguments

    '''
    #########parser arguments#############
    parser = argparse.ArgumentParser(description="""Preprocessor""")
    parser.add_argument(
        "--speech",
        action="store",
        dest="speech",
        default="/input/s3_connector/voice_processing/audio.mp4",
        required=True,
        help="""audio file""",
    )
    parser.add_argument(
        "--language",
        action="store",
        dest="language",
        default="english",
        required=True,
        help="""audio file""",
    )
    parser.add_argument(
        "--model_size",
        action="store",
        dest="model_size",
        default="medium",
        required=True,
        help="""size of the model to be used""",
    )

    return parser.parse_args()

def main():
    '''
    main function
    '''
    # arguments
    args = argument_parser()

    # get audio file
    audio_file = get_audio_file(args.speech)

    #modelling and text results
    result = speech_to_text(audio_file, args.model_size, args.language)

    #s ave the text from the audio file into a txt file
    save_text_file(result)

if __name__ == '__main__':
    main()
