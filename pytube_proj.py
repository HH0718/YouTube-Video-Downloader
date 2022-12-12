from pytube import YouTube
import ffmpeg
import os


def vid_only():
    for stream in yt.streams.filter(only_video=True, adaptive=True, file_extension="mp4"):
        res_avail.add((stream.resolution))
    r = ", ".join(res_avail)
    print(f"Available resolutions:  {r}")

    res_choose = input("Input your desired resolution: ")
    print("Downloading . . .")
    vid_download = yt.streams.filter(res=res_choose.lower()).first().download(filename=yt.title + " VIDEO ONLY.mp4")


   
def aud_only():
    aud_download = yt.streams.get_audio_only()
    aud_download.download(filename=yt.title + " AUDIO ONLY.mp4")


def convert_to_mp3():
    audio_stream_mp3 = yt.title + " AUDIO ONLY.mp3"
    video = ffmpeg.input(yt.title + " AUDIO ONLY.mp4")
    audio = video.audio
    stream = ffmpeg.output(audio, audio_stream_mp3)
    ffmpeg.run(stream)

    os.remove(yt.title + " AUDIO ONLY.mp4")

def vid_and_aud():
    vid = ffmpeg.input(yt.title + " VIDEO ONLY.mp4")
    aud = ffmpeg.input(yt.title + " AUDIO ONLY.mp4")


    ffmpeg.output(aud, vid, 'out.mp4').run()

    os.remove(yt.title + " AUDIO ONLY.mp4")
    os.remove(yt.title + " VIDEO ONLY.mp4")



link = input("Input youtube link: ")
yt = YouTube(link)
res_avail = set()
stream_type = int(input("Types: \n1. Video only \n2. Audio only \n3. Video with audio \nEnter the number of the type you want to download: "))

if stream_type == 1:
    vid_only()
   

elif stream_type == 2:
    aud_only()
    convert_to_mp3()

elif stream_type == 3:
    vid_only()
    aud_only()
    vid_and_aud()
    
else:
    print("Invalid input")


print(yt.title + "\nHas been successfully downloaded.")
