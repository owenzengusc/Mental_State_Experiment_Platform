# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git
from window import *
from user import *
from StroopTest import *
from MathTest import *
from ColdPressureTest import *
from FeedbackScreen import FeedbackScreen
from InstructionScreen import InstructionScreen
from video import VideoFeedbackApp
from RelaxationScreen import show_relaxation_screen
import json

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
TEST_WINDOW_WIDTH = 1960
TEST_WINDOW_HEIGHT = 1080
AVERAGE_TEST_DURATION = 5

def load_test_sequence():
    with open('./test/test.json', 'r') as file:
        data = json.load(file)
        return data["Test_List"]

def show_instruction_screen(test_name):
    instruction_window = create_new_window(test_name, TEST_WINDOW_WIDTH, TEST_WINDOW_HEIGHT)
    if test_name == "StroopTest":
        app = InstructionScreen(instruction_window, "StroopTest", instruction_window.destroy)
    elif test_name == "MathTest":
        app = InstructionScreen(instruction_window, "MathTest", instruction_window.destroy)
    elif test_name == "ColdPressureTest":
        app = InstructionScreen(instruction_window, "ColdPressureTest", instruction_window.destroy)
    instruction_window.mainloop()

def execute_sequence(choice, ppl):

    test_sequence = load_test_sequence()
    if choice in ["Tests", "Tests+Videos", "Tests+Videos+CPT"]:
        for test in test_sequence:
            show_instruction_screen(test)

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


    if choice in ["Videos", "Tests+Videos", "Tests+Videos+CPT"]:
        video_window = tk.Tk()
        app = VideoFeedbackApp(video_window, ppl.name)
        video_window.mainloop()
    
    if choice in ["Tests+Videos+CPT"]:
        show_instruction_screen("ColdPressureTest")
        show_cold_pressure_test(username=ppl.name)
    else:
        show_relaxation_screen(duration=180)

    feedback_window = tk.Tk()
    app = FeedbackScreen(feedback_window, ppl.name)
    feedback_window.mainloop()

def main():
    pre_window = create_new_window("EEG_Sensor_Interface", 800, 600)
    canvas_main = tk.Canvas(pre_window, width=800, height=600, bg="lightgray")
    canvas_main.pack(fill="both", expand=True)

    label_enter_name = tk.Label(pre_window, text="Please enter your name:", font=("calibri", 20), bg="lightgray")
    canvas_main.create_window(400, 250, window=label_enter_name)

    entry_name = tk.Entry(pre_window, font=("calibri", 12))
    canvas_main.create_window(400, 280, window=entry_name)

    # Dropdown menu for user choice
    user_choice = tk.StringVar(pre_window)
    user_choice.set("Tests")  # default value
    choices = ["Tests", "Videos", "Tests+Videos", "Tests+Videos+CPT"]
    dropdown_menu = tk.OptionMenu(pre_window, user_choice, *choices)
    canvas_main.create_window(400, 310, window=dropdown_menu)

    button1 = tk.Button(text='Enter', font=("calibri", 18), command=lambda: get_user_name(pre_window, entry_name, canvas_main, user_choice.get()))
    canvas_main.create_window(400, 370, window=button1)

    ppl = Participant()
    def get_user_name(windw, enntry, canvas, choice):
        user_name = enntry.get()
        ppl.name = user_name
        windw.destroy()
        show_relaxation_screen(duration=180)  # 3 minutes
        execute_sequence(choice, ppl)

    while True:
        if ppl.name != "New_User":
            break
        pre_window.update()

if __name__ == "__main__":
    main()
