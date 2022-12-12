from enum import Enum, auto
import validators
from pytube import YouTube
import ffmpeg
from pathlib import Path

DEFAULT_FILTER = {"only_video": True,
                  "adaptive": True,
                  "file_extension": "mp4"}


class StreamType(Enum):
    VIDEO = auto()
    AUDIO = auto()
    VIDEO_AUDIO = auto()


def input_url():
    valid_url = False
    while not valid_url:
        download_url = input("Please enter youtube URL: ")
        if download_url == "":
            download_url = "https://www.youtube.com/watch?v=SDpCzJw2xm4&t=1s"
        valid_url = validators.url(download_url)
        print("\n")
        if not valid_url:
            print("URL is not valid.")
            print(100 * "\n")
    return download_url


def input_stream_type() -> StreamType:
    valid_stream_type = False

    while not valid_stream_type:
        [print(f"{stream_type.name} = {stream_type.value}")
         for stream_type in list(StreamType)]

        try:
            stream_type = StreamType(
                int(input("Please enter Stream Type number: ")))
            valid_stream_type = True
            print("\n")

        except (ValueError, IndexError):
            print("Please enter a valid entry")
            print(100 * "\n")

    return stream_type


def download_video(youtube: YouTube):
    streams = [stream for stream in sorted(youtube.streams.filter(
        **DEFAULT_FILTER), key=lambda video: video.resolution[-1]) if stream.video_codec.startswith('avc1')]

    [print(i, stream.resolution) for i, stream in enumerate(streams, start=1)]

    selected_resolution = int(
        input('Please enter the resolution you want to download i.e "1": '))

    streams[selected_resolution - 1].download(filename=f"VIDEO_{youtube.title}.mp4")

def download_audio(youtube: YouTube):
    youtube.streams.get_audio_only().download(filename=f"AUDIO_{youtube.title}.mp4")

def post_process(youtube: YouTube):
    video = ffmpeg.input(filename=f"VIDEO_{youtube.title}.mp4")
    audio = ffmpeg.input(filename=f"AUDIO_{youtube.title}.mp4")

    ffmpeg.output(audio, video, f'./{youtube.title}.mp4').run()

    Path(f"VIDEO_{youtube.title}.mp4").unlink()
    Path(f"AUDIO_{youtube.title}.mp4").unlink()
    


def download_video_audio(youtube: YouTube):
    download_video(youtube)
    download_audio(youtube)
    post_process(youtube)


def download_init(url: str, stream_type: StreamType):
    youtube = YouTube(url)
    match stream_type:
        case StreamType.VIDEO:
            download_video(youtube)

        case StreamType.AUDIO:
            download_audio(youtube)

        case StreamType.VIDEO_AUDIO:
            download_video_audio(youtube)



def main() -> None:
    download_url = input_url()
    stream_type = input_stream_type()

    print(f"You selected {stream_type.name} download from {download_url}")
    download_init(download_url, stream_type)


if __name__ == "__main__":
    main()
