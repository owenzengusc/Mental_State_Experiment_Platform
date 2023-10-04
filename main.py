# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git
from window import *
from user import *
from StroopTest import *
from MathTest import *

TEST = "stroop"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
start_stroop_test = 0


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
    
    label_enter_name = tk.Label(pre_window, text="Please enter your name:")
    canvas_main.create_window(200, 100, window=label_enter_name)
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
    
    
    def play_video(f):
        from moviepy.editor import VideoFileClip
        video = VideoFileClip("./videos/" + f + ".mp4")
        video = video.subclip(0, 10)
        #video.resize(2)
        video.preview(fps = 60,fullscreen = False)
        
    
    load_btn = tk.Button(test_window, text="Load Video", font = ("calibri", 12 ,"bold"), command = lambda: play_video("test"))
    load_btn.pack(ipadx=12, ipady=4, anchor="nw")
    #test_window.mainloop()
    test_window.destroy()
    
    if TEST == "stroop":
        stroop_instruction_window = create_new_window("Stroop", WINDOW_WIDTH, WINDOW_HEIGHT)
        canvas_stroop = tk.Canvas(stroop_instruction_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        canvas_stroop.pack()
        #text = Label(stroop_instruction_window, text="Just do it", bg="red", fg="yellow")
        test_name = Label(stroop_instruction_window, text="Stroop Test", bg="red", fg="Yellow", font = ("calibri", 20 ,"bold"))
        #place the text in the center of the window
        test_name.place(x=WINDOW_WIDTH/2-40,y=60)
        test_instruction = Label(stroop_instruction_window, text="In this experiment you are required to select the color of the word, not what the word says.", fg="black")
        test_instruction.place(x=12,y=120)
        test_example = Label(stroop_instruction_window, text="For example, if the word is:", fg="black")
        test_example.place(x=12,y=150)
        test_example_word = Label(stroop_instruction_window, text="RED", fg="blue")
        test_example_word.place(x=12,y=180)
        test_example_continue = Label(stroop_instruction_window, text="You should select Blue by clicking on the Blue button", fg="black")
        test_example_continue.place(x=12,y=210)
        
        def start_stroop_test():
            nonlocal start_stroop_test
            start_stroop_test = 1
        
        start_stroop = tk.Button(stroop_instruction_window, text="Start", font = ("calibri", 12 ,"bold"), command =start_stroop_test)
        #start_stroop.place(x=WINDOW_WIDTH/2-40,y=300)
        canvas_stroop.create_window(WINDOW_WIDTH/2, WINDOW_HEIGHT-600, window=start_stroop)
        #start_stroop.pack()
        
        while True:
            if start_stroop_test == 1:
                print("start stroop test")
                stroop_instruction_window.destroy()
                stroop_test_window = tk.Tk()
                app = StroopTest(stroop_test_window,ppl.name)
                stroop_test_window.mainloop()
                break
            stroop_instruction_window.update()
        
        
        
    

    #pre_window.mainloop()

if __name__ == "__main__":
    main()

    
    

