import soundfile as sf
from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none
import time
import torch
import argparse
import os

def generate_audio(lang, tag, vocoder_tag, text):
    text2speech = Text2Speech.from_pretrained(
        model_tag=str_or_none(tag),
        vocoder_tag=str_or_none(vocoder_tag),
        # Only for FastSpeech & FastSpeech2 & VITS
        speed_control_alpha=1.0
    )
  
    #text = 'One random thought I have is that its amazing how much technology has advanced over the years and how it has transformed the way we live our lives. From smartphones to social media to self-driving cars, the possibilities seem endless, and it makes me wonder what other incredible innovations we will see in the future.'
    
    # synthesis
    with torch.no_grad():
        start = time.time()
        wav = text2speech(text)["wav"]
    rtf = (time.time() - start) / (len(wav) / text2speech.fs)
    print(f"RTF = {rtf:5f}")

    # save audio to file
    filename = "/cnvrg/audio.wav"
    sf.write(filename, wav.view(-1).cpu().numpy(), text2speech.fs)
    
def argument_parser():
    '''
    parser arguments

    '''
    #########parser arguments#############
    parser = argparse.ArgumentParser(description="""Preprocessor""")
    parser.add_argument(
        "--text",
        action="store",
        dest="text",
        required=True,
        default="/input/s3_connector/voice_processing/speech.txt",
        help="""text""",
    )

    return parser.parse_args()

def main():
    '''
    main function
    '''
    # arguments
    args = argument_parser()
    
    extension = os.path.splitext(args.text)[-1]
    if extension == '.txt':
        with open(args.text, 'r') as file:l
            text = file.read()
    else:
        text = args.text
    
    lang = 'English'
    tag = 'kan-bayashi/ljspeech_fastspeech2'
    vocoder_tag = "parallel_wavegan/ljspeech_parallel_wavegan.v1"
    
    generate_audio(lang, tag, vocoder_tag, text)

if __name__ == '__main__':
    main()
