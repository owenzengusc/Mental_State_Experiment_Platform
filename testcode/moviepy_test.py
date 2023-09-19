from moviepy.editor import *
#video = VideoFileClip("./videos/sample-mp4-file.mp4")
video = VideoFileClip("./videos/test.mp4")
video = video.subclip(0, 10)
#video.resize(2)
video.preview(fps = 60,fullscreen = True)