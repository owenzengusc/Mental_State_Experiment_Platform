# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git
from window import *
from user import *
from StroopTest import *
from MathTest import *
from FeedbackScreen import FeedbackScreen
from InstructionScreen import InstructionScreen
import json

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
TEST_WINDOW_WIDTH = 900
TEST_WINDOW_HEIGHT = 700
# INSTRUCTION_WINDOW_WIDTH = 800
# INSTRUCTION_WINDOW_HEIGHT = 600
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
    instruction_window.mainloop()

def main():
    # Improved "Enter Name" screen layout
    pre_window = create_new_window("EEG_Sensor_Interface", 800, 600)
    canvas_main = tk.Canvas(pre_window, width=800, height=600, bg="lightgray")
    canvas_main.pack(fill="both", expand=True)

    label_enter_name = tk.Label(pre_window, text="Please enter your name:", font=("calibri", 14), bg="lightgray")
    canvas_main.create_window(400, 250, window=label_enter_name)

    entry_name = tk.Entry(pre_window, font=("calibri", 12))
    canvas_main.create_window(400, 280, window=entry_name)

    button1 = tk.Button(text='Enter', font=("calibri", 12), command=lambda: get_user_name(pre_window, entry_name, canvas_main))
    canvas_main.create_window(400, 320, window=button1)

    ppl = Participant()
    def get_user_name(windw, enntry, canvas):
        user_name = enntry.get()
        ppl.name = user_name
        windw.destroy()

    while True:
        if ppl.name != "New_User":
            break
        pre_window.update()

    # Welcome screen
    welcome_window = create_new_window("Welcome", 800, 600)
    canvas_welcome = tk.Canvas(welcome_window, width=800, height=600, bg="lightgray")
    canvas_welcome.pack(fill="both", expand=True)

    welcome_label = tk.Label(welcome_window, text=f"Welcome, {ppl.name}!", font=("calibri", 20, "bold"), bg="lightgray")
    canvas_welcome.create_window(400, 250, window=welcome_label)

    test_sequence = load_test_sequence()
    num_tests = len(test_sequence)
    total_duration = num_tests * AVERAGE_TEST_DURATION

    test_info_label = tk.Label(welcome_window, text=f"You will be taking {num_tests} tests today: {', '.join(test_sequence)}.\nThis will take approximately {total_duration} minutes.", font=("calibri", 14), bg="lightgray")
    canvas_welcome.create_window(400, 300, window=test_info_label)

    continue_button = tk.Button(welcome_window, text="Continue", font=("calibri", 12), command=welcome_window.destroy)
    canvas_welcome.create_window(400, 350, window=continue_button)
    welcome_window.mainloop()

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

    feedback_window = tk.Tk()
    app = FeedbackScreen(feedback_window, ppl.name)
    feedback_window.mainloop()

if __name__ == "__main__":
    main()
