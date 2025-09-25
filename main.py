from pytubefix import Playlist
from pytubefix.cli import on_progress
from pydub import AudioSegment
import logging
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="xTube downloader")
    parser.add_argument('-u', '--url', type=str,
                        required=True, help='URL to process')
    parser.add_argument('-o', '--output', type=str,
                        help='output path for mp3', default=os.getcwd())
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug mode')
    parser.add_argument('--example', action='store', type=str, help='Example store action')
    arguments = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO if not arguments.debug else logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    log = logging.getLogger(__name__)
    if arguments.output and not os.path.exists(arguments.output):
        os.makedirs(arguments.output)
    log.debug("Mode debugging is enabled.")
    playlist = Playlist(arguments.url)
    processing_playlist(playlist, arguments, log)

def processing_playlist(playlist: Playlist, arguments, log) -> list:
    """Process a YouTube playlist URL and download audio-only streams."""
    log.info(f"Playlist title: {playlist.title}")
    sum_size = 0
    for idx, video in enumerate(playlist.videos, start=1):
        log.info(f"[{idx}/{len(playlist)}] Processing video : {video.title}")
        dv = video.streams.get_audio_only()
        size_mb = dv.filesize / (1024 * 1024)
        sum_size += size_mb
        filename = dv.download("/tmp")
        log.debug(f"Downloaded video path : {filename}")
        log.debug(f"File size: {size_mb:.2f} MB")
        audio = AudioSegment.from_file(filename, format='m4a')
        mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
        mp3_filename = os.path.join(arguments.output, mp3_filename.rsplit('/', 1)[1])
        audio.export(mp3_filename, format='mp3')
        log.debug(f"Converted {filename} to {mp3_filename}")
    log.info(f"Total size of downloaded audio files: {sum_size:.2f} MB")

if __name__ == "__main__":
    main()
