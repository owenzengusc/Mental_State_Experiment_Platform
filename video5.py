import pygame
from moviepy.editor import VideoFileClip
pygame.init ()
clip = VideoFileClip("./videos/starwar.mp4")
clipresized = clip.resize (height=700)
clipresized.preview ()
print("Hello World")
pygame.quit ()

