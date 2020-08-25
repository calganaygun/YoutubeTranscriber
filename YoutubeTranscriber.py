import getopt
import os
import shutil
import subprocess
import sys
from multiprocessing.dummy import Pool

import speech_recognition as sr
from tqdm import tqdm

numOfThreads = int(os.getenv('NUM_OF_THREADS', '8'))
credentialsGC = os.getenv('GC_CREDENTIAL', 'api-key.json')

with open(credentialsGC) as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()


def getWavFile(id):
    # Run youte-dl to download Youtube video and translate to WAV
    print("Video is downloading...")
    os.system('youtube-dl -f bestaudio --extract-audio --audio-format wav --audio-quality 3 -o ./temp/{id}.webm https://www.youtube.com/watch?v={id} > /dev/null'.format(id=id))


def splitWaw(id):
    try:
        os.mkdir('temp/parts-' + id)
    except:
        pass
    # Run ffmpeg to split WAV file
    # This command generates 30 second pieces of WAV file
    print("Sound file splitting...")
    os.system('ffmpeg -i temp/{id}.wav -f segment -segment_time 30 -c copy ./temp/parts-{id}/out%06d.wav 2> /dev/null'.format(id=id))


def prepareTranscript(id, language):
    global langOfVideo
    langOfVideo = language

    # If the transcript of the video is already created, directly returns saved transcript
    if id in os.listdir('./transcripts'):
        with open('./transcripts/' + id, 'r', encoding='utf-8') as transcriptFile:
            return transcriptFile.read()
    
    getWavFile(id)
    splitWaw(id)
    files = sorted(os.listdir('temp/parts-' + id))
    global idofVideo
    idofVideo = id
    transcript = transcribeFiles(files)

    # Save generated transcript for next uses
    with open('transcripts/' + id, 'w', encoding='utf-8') as transcriptFile:
        transcriptFile.write(transcript)
    shutil.rmtree('./temp/parts-' + id)
    os.remove('./temp/'+id+'.wav')

    return transcript


def transcribe(data):
    try:
        global idofVideo
        idx, file = data
        name = 'temp/parts-'+idofVideo+'/' + file
        # Load audio file
        with sr.AudioFile(name) as source:
            audio = r.record(source)
        # Transcribe audio file
        text = r.recognize_google_cloud(
            audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language=langOfVideo)
        return {
            'idx': idx,
            'text': text
        }
    except sr.UnknownValueError: # Google Cloud STT API gives error if can not detect speech in the audio
        return {
            'idx': idx,
            'text': ''
        }


def transcribeFiles(files):
    print("Sound files is processing on Google Cloud STT API...")
    pool = Pool(numOfThreads)  # Number of concurrent threads
    all_text = pool.map(transcribe, enumerate(files))
    pool.close()
    pool.join()

    transcript = ''
    for t in sorted(all_text, key=lambda x: x['idx']):
        total_seconds = t['idx'] * 30
        # Cool shortcut from:
        # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
        # to get hours, minutes and seconds
        m, s = divmod(total_seconds, 60)
        h, m = divmod(m, 60)

        # Format time as h:m:s - 30 seconds of text
        transcript = transcript + \
            '{:0>2d}:{:0>2d}:{:0>2d} {}\n'.format(h, m, s, t['text'])
    return transcript


def main(argv):
    videoID = 'lSQ4vtkwW1Y'
    word = 'getAll'
    language = 'tr-TR'
    try:
        opts, _ = getopt.getopt(argv, 'hv:w:l:', ['video=', 'word='])
    except getopt.GetoptError:
        print(
            'YoutubeTranscriber.py -v <YouTube Video ID> -w <word or "getAll" for printing transcript> -l <language code standart: tr-TR>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print(
                'YoutubeTranscriber.py -v <YouTube Video ID> -w <word or "getAll" for printing transcript> -l <language code standart: tr-TR>')
            sys.exit()
        elif opt in ('-v', '--video'):
            videoID = arg
        elif opt in ('-w', '--word'):
            word = arg
        elif opt in ('-l', '--language'):
            language = arg

    if videoID != '':
        if word == 'getAll':
            print(prepareTranscript(videoID, language))
        elif word != '':
            count = 0
            for i in prepareTranscript(videoID, language).split('\n'):
                if word.lower() in i.lower():
                    print(i)
                    count += 1
            print('Transcript searched and {} result(s) found.'.format(count))
        else:
            print(
                'YoutubeTranscriber.py -v <YouTube Video ID> -w <word or "getAll" for printing transcript> -l <language code standart: tr-TR>')
            sys.exit(2)
    else:
        print(
            'YoutubeTranscriber.py -v <YouTube Video ID> -w <word or "getAll" for printing transcript> -l <language code standart: tr-TR>')
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])