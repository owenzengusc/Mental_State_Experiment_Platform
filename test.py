import tkinter as tk
from tkvideo import tkvideo
import pygame
import os



def get_audio(file):
    from moviepy.editor import VideoFileClip

    # Load the MP4 file
    video = VideoFileClip(file + ".mp4")

    # Extract the audio
    audio = video.audio

    # Save the audio as an MP3 file
    audio.write_audiofile(file + ".mp3")


def start(file):
    if not file + ".mp3" in os.listdir("."):
        get_audio(file)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file + ".mp3")
    root = tk.Tk()
    root.geometry("640x480")

    videoPlayer = tk.Label(root)
    videoPlayer.pack()
    video = tkvideo(file + ".mp4", videoPlayer, loop=1, size=(640,480))
    video.play()
    pygame.mixer.music.play()
    root.mainloop()


start("sample-mp4-file")