FROM python:3.7.9-alpine3.12
ADD . /app
WORKDIR /app
RUN apk add youtube-dl ffmpeg flac
RUN pip install -r requirements.txt
ENTRYPOINT ["python","./YoutubeTranscriber.py"]