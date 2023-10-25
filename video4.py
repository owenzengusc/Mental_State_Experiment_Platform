import vlc
import time

def on_end_reached(event):
    print('Finished')

filepath = "./videos/starwar.mp4"
player = vlc.MediaPlayer(filepath)

# Set up an event manager and listen for the "MediaEndReached" event
event_manager = player.event_manager()
event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, on_end_reached)

player.play()

# Keep the script running to allow the video to play
while not player.is_playing():
    time.sleep(1)
