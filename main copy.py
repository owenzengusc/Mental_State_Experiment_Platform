# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_TEST_Interface.git
from window import *
from user import *
from StroopTest import *
from MathTest import *
from ImageTest import *  # TODO 1: Import the ImageTest class
from ColdPressorTest import *
from FeedbackScreen import FeedbackScreen
from InstructionScreen import InstructionScreen
from video import VideoFeedbackApp
from RelaxationScreen import show_relaxation_screen
from datetime import datetime
import json

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
TEST_WINDOW_WIDTH = 1960
TEST_WINDOW_HEIGHT = 1080
AVERAGE_TEST_DURATION = 5

FONT = "Open Sans"

def load_test_sequence():
    with open('./test/test.json', 'r') as file:
        data = json.load(file)
        return data["Test_List"]

def log_event(event_name, start_time, end_time, duration, username='New_User'):
    log_data_path = f'./data/log_{username}.csv'

    # Convert start_time and end_time to strings with milliseconds only if they are not None
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] if start_time else ''
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] if end_time else ''


    # Check if the file exists and write headers if it's new
    try:
        with open(log_data_path, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Event', 'Start Time', 'End Time', 'Duration (milliseconds)'])
    except FileExistsError:
        pass  # File already exists, append to it without writing headers

    # Write the event data
    with open(log_data_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([event_name, start_time_str, end_time_str, duration])



def show_instruction_screen(test_name):
    instruction_window = create_new_window(test_name, TEST_WINDOW_WIDTH, TEST_WINDOW_HEIGHT)
    if test_name == "StroopTest":
        app = InstructionScreen(instruction_window, "StroopTest", instruction_window.destroy)
    elif test_name == "MathTest":
        app = InstructionScreen(instruction_window, "MathTest", instruction_window.destroy)
    elif test_name == "ColdPressorTest":
        app = InstructionScreen(instruction_window, "ColdPressorTest", instruction_window.destroy)
    # TODO 3: Add the ImageTest Test
    elif test_name == "ImageTest":
        app = InstructionScreen(instruction_window, "ImageTest", instruction_window.destroy)
    instruction_window.mainloop()

def execute_sequence(choice, ppl):
    test_sequence = load_test_sequence()
    already_relaxed = False

    if choice == "StroopTest":
        # record the start of the relaxation screen
        relaxation_start_time = datetime.now()
        log_event('First Relaxation Start', relaxation_start_time, None, None, username=ppl.name)
        show_relaxation_screen(duration=10)  # 3 minutes
        relaxation_end_time = datetime.now()
        duration = int((relaxation_end_time - relaxation_start_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event('First Relaxation End', relaxation_start_time, relaxation_end_time, duration, username=ppl.name)
        already_relaxed = True

        test_start_time = datetime.now()
        # Show instruction screen and wait for it to close
        show_instruction_screen("StroopTest")  # FIXED
        # Log the start of the test
        log_event("StroopTest Start", test_start_time, None, None, username=ppl.name)  # FIXED
        
        print("Initializing StroopTest window...")
        stroop_test_window = tk.Tk()
        stroop_test_window.geometry(f"{TEST_WINDOW_WIDTH}x{TEST_WINDOW_HEIGHT}+{(stroop_test_window.winfo_screenwidth() - TEST_WINDOW_WIDTH) // 2}+{(stroop_test_window.winfo_screenheight() - TEST_WINDOW_HEIGHT) // 2}")
        
        print("Creating StroopTest app...")
        app = StroopTest(stroop_test_window, ppl.name)
        print("Running mainloop...")
        stroop_test_window.mainloop()
        print("StroopTest mainloop ended.")

        # End test
        test_end_time = datetime.now()
        duration = int((test_end_time - test_start_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event("StroopTest End", test_start_time, test_end_time, duration, username=ppl.name)  # FIXED


    if choice in ["Tests", "Tests+Videos", "Tests+Videos+CPT"]:
        # record the start of the relaxation screen
        relaxation_start_time = datetime.now()
        log_event('First Relaxation Start', relaxation_start_time, None, None, username=ppl.name)
        show_relaxation_screen(duration=180)  # 3 minutes
        relaxation_end_time = datetime.now()
        duration = int((relaxation_end_time - relaxation_start_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event('First Relaxation End', relaxation_start_time, relaxation_end_time, duration, username=ppl.name)
        already_relaxed = True
        for test in test_sequence:
            test_start_time = datetime.now()
            # Show instruction screen and wait for it to close
            show_instruction_screen(test)
            # Log the start of the test
            log_event(f"{test} Start", test_start_time, None, None, username=ppl.name)
            

            if test == "StroopTest":
                stroop_test_window = tk.Tk()
                stroop_test_window.geometry(f"{TEST_WINDOW_WIDTH}x{TEST_WINDOW_HEIGHT}+{(stroop_test_window.winfo_screenwidth() - TEST_WINDOW_WIDTH) // 2}+{(stroop_test_window.winfo_screenheight() - TEST_WINDOW_HEIGHT) // 2}")
                app = StroopTest(stroop_test_window, ppl.name)
                stroop_test_window.mainloop()

            elif test == "MathTest":
                math_test_window = tk.Tk()
                math_test_window.geometry(f"{TEST_WINDOW_WIDTH}x{TEST_WINDOW_HEIGHT}+{(math_test_window.winfo_screenwidth() - TEST_WINDOW_WIDTH) // 2}+{(math_test_window.winfo_screenheight() - TEST_WINDOW_HEIGHT) // 2}")
                app = MathTest(math_test_window, ppl.name)
                math_test_window.mainloop()

            # TODO 2: Add the ImageTest Test
            elif test == "ImageTest":
                image_test_window = tk.Tk()
                image_test_window.geometry(f"{TEST_WINDOW_WIDTH}x{TEST_WINDOW_HEIGHT}+{(image_test_window.winfo_screenwidth() - TEST_WINDOW_WIDTH) // 2}+{(image_test_window.winfo_screenheight() - TEST_WINDOW_HEIGHT) // 2}")
                app = ImageTest(image_test_window, ppl.name)
                image_test_window.mainloop()
            
            test_end_time = datetime.now()
            duration = int((test_end_time - test_start_time).total_seconds() * 1000)  # Duration in milliseconds
            log_event(f"{test} End", test_start_time, test_end_time, duration, username=ppl.name)
            
            


    if choice in ["Videos", "Tests+Videos", "Tests+Videos+CPT"]:
        if not already_relaxed:
            relaxation_start_time = datetime.now()
            log_event('First Relaxation Start', relaxation_start_time, None, None, username=ppl.name)
            show_relaxation_screen(duration=180)  # 3 minutes
            relaxation_end_time = datetime.now()
            duration = int((relaxation_end_time - relaxation_start_time).total_seconds() * 1000)  # Duration in milliseconds
            log_event('First Relaxation End', relaxation_start_time, relaxation_end_time, duration, username=ppl.name)
        video_window = tk.Tk()
        # record the start of the video feedback
        video_start_time = datetime.now()
        log_event('Video Feedback Start', video_start_time, None, None, username=ppl.name)
        app = VideoFeedbackApp(video_window, ppl.name)
        video_window.mainloop()
        print('Video Feedback Ended')
        video_end_time = datetime.now()
        duration = int((video_end_time - video_start_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event('Video Feedback End', video_start_time, video_end_time, duration, username=ppl.name)

    
    if choice in ["Tests+Videos+CPT", "CPT"]:
        
        show_instruction_screen("ColdPressorTest")
        # record the start of the Cold Pressor test
        cpt_start_time = datetime.now()
        log_event('Cold Pressor Test Start', cpt_start_time, None, None, username=ppl.name)
        show_cold_pressure_test(username=ppl.name)
        cpt_end_time = datetime.now()
        duration = int((cpt_end_time - cpt_start_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event('Cold Pressor Test End', cpt_start_time, cpt_end_time, duration, username=ppl.name)
    else:
        # record the start of the relaxation screen
        relaxation_start_time = datetime.now()
        log_event('Final Relaxation Start', relaxation_start_time, None, None, username=ppl.name)
        show_relaxation_screen(duration=180)
        relaxation_end_time = datetime.now()
        duration = int((relaxation_end_time - relaxation_end_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event('Final Relaxation End', relaxation_start_time, relaxation_end_time, duration, username=ppl.name)
    


    feedback_window = tk.Tk()
    app = FeedbackScreen(feedback_window, ppl.name)
    feedback_window.mainloop()
    # record the end of the program
    program_end_time = datetime.now()
    duration = int((program_end_time - program_start_time).total_seconds() * 1000)  # Duration in milliseconds
    log_event('Program End', program_start_time, program_end_time, duration, username=ppl.name)

def main():
    pre_window = create_new_window("Cognitive Experiments", 800, 600)
    canvas_main = tk.Canvas(pre_window, width=800, height=600, bg="white")
    canvas_main.pack(fill="both", expand=True)

    #title
    label_title = tk.Label(pre_window, text="Cognitive Experiments", font=("Open Sans", 48), bg="white",fg="#9ba8ee")
    canvas_main.create_window(400, 175, window=label_title)

    #directions
    directions1 = tk.Label(pre_window, text="Throughout the following experiements you will be asked to participate in various tasks and", font=("Open Sans", 15), bg="white",fg="#3a3d42")
    canvas_main.create_window(400, 235, window=directions1)
    directions2 = tk.Label(pre_window, text="your responses will be recorded. The whole session will approximately take 30 minutes.", font=("Open Sans", 15), bg="white",fg="#3a3d42")
    canvas_main.create_window(400, 260, window=directions2)
    directions3 = tk.Label(pre_window, text="Please notify the test taker if you are facing any difficulties.", font=("Open Sans", 15), bg="white",fg="#3a3d42")
    canvas_main.create_window(400, 285, window=directions3)


    label_user_info = tk.Label(pre_window, text="User Information:", font=("Open Sans", 26), bg="white",fg="#9ba8ee")
    canvas_main.create_window(400, 330, window=label_user_info)

    #name
    label_enter_name = tk.Label(pre_window, text="Name:", font=("Open Sans", 16), bg="white",fg="#3a3d42")
    canvas_main.create_window(310, 365, window=label_enter_name)

    entry_name = tk.Entry(pre_window, font=("Open Sans", 12), bg="light gray", fg="#3a3d42", highlightthickness=0, borderwidth=1)
    canvas_main.create_window(430, 365, window=entry_name)

    #age
    label_enter_age = tk.Label(pre_window, text="Age:", font=("Open Sans", 16), bg="white",fg="#3a3d42")
    canvas_main.create_window(315, 400, window=label_enter_age)

    entry_age = tk.Entry(pre_window, font=("Open Sans", 12), bg="light gray", fg="#3a3d42", highlightthickness=0, borderwidth=1)
    canvas_main.create_window(430, 400, window=entry_age)

    #gender
    label_enter_gender = tk.Label(pre_window, text="Gender:", font=("Open Sans", 16), bg="white",fg="#3a3d42")
    canvas_main.create_window(305, 435, window=label_enter_gender)

    entry_gender = tk.Entry(pre_window, font=("Open Sans", 12), bg="light gray", fg="#3a3d42", highlightthickness=0, borderwidth=1)
    canvas_main.create_window(430, 435, window=entry_gender)


    # Dropdown menu for user choice
    user_choice = tk.StringVar(pre_window)
    user_choice.set("Select Test")  # default value
    choices = ["Stroop Test", "Mental Arithmetic Task", "Cold Pressor Test", "Visual Stimulation", "Affective Videos", "Stress Test[Stroop+Arithmetic]", "Continuous Experiments[All]"]

    dropdown_menu = tk.OptionMenu(pre_window, user_choice, *choices)

    # Configure the dropdown menu
    dropdown_menu.config(
        bg="gray",          # Background color of the button
        fg="#3a3d42",             # Text color
        activeforeground="#3a3d42",  # Text color when clicked (matches fg)
        font=("Open Sans", 14),
        highlightthickness=0,     # Remove the border
        relief="flat"             # Remove the 3D effect
    )

    # Configure the dropdown menu items
    dropdown_menu["menu"].config(
        bg="white",               # Background color of the dropdown list
        fg="#3a3d42",             # Text color of the dropdown list
        activebackground="gray",  # Background color of selected item
        activeforeground="#3a3d42"     # Text color of selected item
    )

    # Place the dropdown menu on the canvas
    canvas_main.create_window(70, 100, window=dropdown_menu)
    #og 690, 40



    start_button = tk.Button(text="Start", font=("Open Sans", 36), bg="light gray",fg="#3a3d42", border=0, borderwidth=1, relief="flat", command=lambda: get_user_name(pre_window, entry_name, canvas_main, user_choice.get()))
    canvas_main.create_window(400, 500, window=start_button)

    # def create_rounded_button(x1, y1, x2, y2, radius, text):
    #     # Create rounded corners using lines
    #     button = canvas_main.create_rectangle(
    #         x1 + radius, y1, x2 - radius, y2, 
    #         outline="black", fill="lightgray", width=2
    #     )
    #     # Create the rounded corners
    #     canvas_main.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, outline="black", fill="lightgray")
    #     canvas_main.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, outline="black", fill="lightgray")
    #     canvas_main.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, outline="black", fill="lightgray")
    #     canvas_main.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, outline="black", fill="lightgray")
        
    #     # Create the text in the button
    #     text_id = canvas_main.create_text(
    #         (x1 + x2) / 2, (y1 + y2) / 2,
    #         text=text, font=("Open Sans", 20), fill="black"
    #     )
        
    #     # Bind the click event to the button
    #     canvas_main.tag_bind(button, "<Button-1>", lambda e: start(e))
    #     canvas_main.tag_bind(text_id, "<Button-1>", lambda e: start(e))

    # # Create a rounded "Start" button
    # create_rounded_button(300, 470, 500, 530, 20, "Start")



    ppl = Participant()
    def get_user_name(windw, enntry, canvas, choice):
        user_name = enntry.get()
        ppl.name = user_name
        global program_start_time
        program_start_time = datetime.now()
        log_event('Program Start', program_start_time, None,None, username=ppl.name)
        windw.destroy()
        # # record the start of the relaxation screen
        # relaxation_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # log_event('First Relaxation Start', relaxation_start_time, '', '', username=ppl.name)
        # show_relaxation_screen(duration=180)  # 3 minutes
        # relaxation_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # # Calculate the duration in seconds
        # duration = (time.mktime(time.strptime(relaxation_end_time, '%Y-%m-%d %H:%M:%S')) - 
        #             time.mktime(time.strptime(relaxation_start_time, '%Y-%m-%d %H:%M:%S')))
        # log_event('First Relaxation End', '', relaxation_end_time, duration, username=ppl.name)
        
        execute_sequence(choice, ppl)

    while True:
        if ppl.name != "New_User":
            break
        pre_window.update()

if __name__ == "__main__":
    main()
