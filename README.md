# Newgrounds Audio Downloader ![(Python 3+)](https://img.shields.io/badge/Python-3+-blue.svg) ![Windows XP+](https://img.shields.io/badge/Windows-XP+-brightgreen.svg)

Well, usually there's a download button on the audio page, but what to do if direct downloads are not allowed by the creator even though you love this song too much?

You just use **this**.

## Requirements

- ![(Python 3+)](https://img.shields.io/badge/Python-3+-blue.svg)
- `requests` library
- `bs4` library

Or you just use the [`NGAudioDownloader.exe`](NGAudioDownloader.exe) so all you need is ![Windows XP+](https://img.shields.io/badge/Windows-XP+-brightgreen.svg).

## Usage

Just run the code and enter the Newgrounds ID of the song you wanna download. That's all.

_Example:_

```
$ python .\NGAudioDownloader.py

Enter song id: 807461
Loading HTML...
Creating download link...
Downloading "Mysterious Planet"...
Mysterious Planet successfully downloaded.
```

Your downloads will appear in the `Downloads` folder.

## NOTE!

Please note that you can download the songs named with *latin symbols only*. I'll fix it later so just for now bear with what we have. :3