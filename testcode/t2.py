import cv2
import os
from ffpyplayer.player import MediaPlayer
import time

def PlayVideoFile(f):
    file = os.path.join("./videos", f)
    video = cv2.VideoCapture(file)
    player = MediaPlayer(file)
    
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_time = 1.0 / fps

    last_audio_time = None
    last_video_time = None

    while True:
        ret, frame = video.read()
        audio_frame, val = player.get_frame()

        if not ret:
            print("End of video")
            break

        if val != 'eof' and audio_frame is not None:
            audio_img, audio_time = audio_frame

            if last_audio_time is None:
                last_audio_time = audio_time

            if last_video_time is None:
                last_video_time = time.time()

            audio_elapsed = audio_time - last_audio_time
            video_elapsed = time.time() - last_video_time

            # If audio is ahead of video
            if audio_elapsed > video_elapsed + frame_time:
                time.sleep(audio_elapsed - video_elapsed)
            # If video is ahead of audio, you might want to skip a video frame or adjust as needed

            last_audio_time = audio_time
            last_video_time = time.time()

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    PlayVideoFile("test.mp4")
