# Newgrounds Audio Downloader ![(Python 3+)](https://img.shields.io/badge/Python-3+-blue.svg) ![Windows XP+](https://img.shields.io/badge/Windows-XP+-brightgreen.svg)

Well, usually there's a download button on the audio page, but what to do if direct downloads are not allowed by the creator even though you love this song too much?

You just use **this**.

## Requirements

- ![(Python 3+)](https://img.shields.io/badge/Python-3+-blue.svg)
- `requests` library
- `bs4` library
- `click` library

Or you just use the [`NGAudioDownloader.exe`](NGAudioDownloader.exe) so all you need is ![Windows XP+](https://img.shields.io/badge/Windows-XP+-brightgreen.svg).

## Usage

```
$ NGAudioDownloader.py [OPTIONS] <Newgrounds song ID>

  ===== Newgrounds Audio Downloader by H1K0 =====

Options:
  -d, --dist PATH  Where to save the songs (default: ./Downloads)
  --help           Show this message and exit.
```