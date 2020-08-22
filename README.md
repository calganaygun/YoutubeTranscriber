# YoutubeTranscriber
A Python script to search strings in YouTube videos.

Uses Google Cloud Speect-to-Text API to generate transcripts. You can use Google Cloud Free Tier credits.


## How to use?

1. Clone this repo.
2. Sign-in to [GCP](https://console.cloud.google.com/).
3. Go to [Speect-to-Text API](https://console.cloud.google.com/apis/api/speech.googleapis.com/overview)
   select project and enable this API.
1. Click "Credentials".
2. Click "Create Credentials".
3. Select "Service Account Key".
4. Under "Service Account" select "New service account".
5. Name service.
6.  Select Role: "Project" -> "Owner".
7.  Finish creating credential.
8.  Select your "Service Account" from list.
9.  Click "Add Key" button and select "Create New Key".
10. Leave "JSON" option selected.
11. Click "Create".
12. Save generated API key file to repo's main directory.
13. Rename file to "api-key.json" or, specify `GC_CREDENTIAL` env variable with your json file name
    while running docker image.
    
> This project uses parallel processing. You can use `NUM_OF_THREADS` env variable to specify number of
concurrent threads while running docker image. Unless you change program use *8* threads.

``` bash
# Build Docker image
docker build . -t calganaygun/youtube-transcriber:latest

# Run program and search or generate text
docker run -it calganaygun/youtube-transcriber:latest -v <YouTube Video ID> \
-w <Search string | getAll: prints all of video content> \
-l <Language code Example: 'tr-TR'>
````

## Examples

[![asciicast](https://asciinema.org/a/2JU2fJgAkEia8P6C9LYCyUcyO.svg)](https://asciinema.org/a/2JU2fJgAkEia8P6C9LYCyUcyO)

[![asciicast](https://asciinema.org/a/jC43dK5YmvSRMlzv6imSrQ7ZT.svg)](https://asciinema.org/a/jC43dK5YmvSRMlzv6imSrQ7ZT)
