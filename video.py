# from tkinter import filedialog
# #pip install tkvideoplayer
# from tkVideoPlayer import TkinterVideo
import sys
# import pygame
import os
sys.path.append('videos')
# pygame.mixer.init()

if __name__ == '__main__':
    video = VideoFileClip("./videos/test.mp4")
    video = video.subclip(0, 10)
    #video.resize(2)
    video.preview(fps = 60,fullscreen = True)