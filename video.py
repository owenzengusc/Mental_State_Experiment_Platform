# pip install moviepy
# pip install pygame

# Import everything needed to edit video clips
from moviepy.editor import *
import pygame

# Loading video
clip = VideoFileClip("./videos/starwar.mp4")

# Initialize Pygame and set it to fullscreen
pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

# Previewing the clip
clip.preview()

# Quitting Pygame when done
pygame.quit()
