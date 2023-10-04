import vlc
#pip install python-vlc

import tkinter as tk

def start(file):
    # Initialize VLC player
    Instance = vlc.Instance()
    player = Instance.media_player_new()

    # Set the media to the player instance
    Media = Instance.media_new(file + ".mp4")
    Media.get_mrl()
    player.set_media(Media)

    # Create a new tkinter window
    root = tk.Tk()
    root.geometry("640x480")
    videoPlayer = tk.Frame(root, bg="black")
    videoPlayer.pack(fill=tk.BOTH, expand=tk.YES)
    player.set_hwnd(videoPlayer.winfo_id())

    # Play the video
    player.play()

    root.mainloop()

start("sample-mp4-file")
