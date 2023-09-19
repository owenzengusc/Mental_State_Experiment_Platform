# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git

from window import *
from user import *
from video import *


def main():
    pre_window = create_new_window("EEG_Sensor_Interface", 800, 600)
    # create new canvas
    canvas_main = tk.Canvas(pre_window, width=800, height=600)
    canvas_main.pack()

    # create new entry box
    entry_name = tk.Entry(pre_window) 
    #
    canvas_main.create_window(200, 140, window=entry_name)
    
    ppl = Participant()
    def get_user_name(windw, enntry, canvas):
        user_name = enntry.get()
        user_name_lable = tk.Label(windw, text=user_name)
        canvas.create_window(200, 230, window=user_name_lable)
        ppl.name = user_name
    
    # button1 is a button that calls get_user_name() when clicked
    button1 = tk.Button(text='Enter', command= lambda: get_user_name(pre_window, entry_name, canvas_main))
   
    canvas_main.create_window(200, 180, window=button1)
    while True:
        # wait for user to enter name
        if ppl.name != "New_User":
            print(ppl.name)
            break
        pre_window.update()
        
    pre_window.destroy()
        
    test_window = create_new_window("Test", 900, 700)
    #canvas_test = tk.Canvas(test_window, width=900, height=700)
    #canvas_test.pack()
    
    frame = tk.Frame(test_window)
    frame.pack()
    
    lower_frame = tk.Frame(test_window, bg='lightgray')
    lower_frame.pack(fill = "both", side= BOTTOM)
 
    vid_player = TkinterVideo(test_window, scaled=True)
    vid_player.pack(expand = True, fill = "both")

 
    def get_audio(file):
        from moviepy.editor import VideoFileClip
        # Load the MP4 file
        video = VideoFileClip("./videos/" +file + ".mp4")
        # Extract the audio
        audio = video.audio
        # Save the audio as an MP3 file
        audio.write_audiofile("./videos/" +file + ".mp3")
  
    def play_video(file):
        if not file + ".mp3" in os.listdir("./videos"):
            get_audio(file)
        if file + ".mp3" in os.listdir("./videos"):
            vid_player.load("./videos/" + file + ".mp4")
            pygame.mixer.music.load("./videos/" + file + ".mp3")
            vid_player.play()
            pygame.mixer.music.play()
            
    
    
    
    load_btn = tk.Button(test_window, text="Load Video", font = ("calibri", 12 ,"bold"), command = lambda: play_video("test"))
    load_btn.pack(ipadx=12, ipady=4, anchor="nw")
    
    test_window.mainloop()
    #pre_window.mainloop()

if __name__ == "__main__":
    main()

    
    

