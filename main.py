# Mental State Experiment Platform
# Authors: Owen Zeng, Kaiden Ko
# https://github.com/owenzengusc/Mental_State_Experiment_Platform

from window import *
from user import *
from StroopTest import *
from MathTest import *
from ImageTest import *  # TODO 1: Import the ImageTest class
from ColdPressorTest import *
from FeedbackScreen import FeedbackScreen
from InstructionScreen import InstructionScreen
from video import VideoTest
from RelaxationScreen import show_relaxation_screen
from datetime import datetime
from window_utils import set_responsive_geometry, get_responsive_window_size
import json
import csv
import os

# Constants adjusted to be relative rather than absolute
# These will be used as fallbacks if responsive sizing fails
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
TEST_WINDOW_WIDTH = 1960
TEST_WINDOW_HEIGHT = 1080
AVERAGE_TEST_DURATION = 5

FONT = "Open Sans"

# Custom Button class to override default styling behavior
class CustomButton(tk.Button):
    def __init__(self, master=None, **kw):
        tk.Button.__init__(self, master, **kw)
        self._default_bg = kw.get('bg', '#CCCCCC')
        self._active_bg = kw.get('activebackground', '#0062CC')
        self._orig_fg = kw.get('fg', 'white')
        self._disabled = True if kw.get('state') == 'disabled' else False
        
        # Override the default appearance
        if not self._disabled:
            self.config(bg=self._default_bg)
        
        # Bind events to maintain custom appearance
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        if not self._disabled:
            self.config(bg=self._active_bg)
    
    def _on_leave(self, event):
        if not self._disabled:
            self.config(bg=self._default_bg)
    
    def set_state(self, state, bg_color=None):
        if state == "normal":
            self._disabled = False
            if bg_color:
                self._default_bg = bg_color
            self.config(state="normal", bg=self._default_bg)
        else:
            self._disabled = True
            self.config(state="disabled", bg="#CCCCCC")

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

def store_user_info(name, age, gender):
    """Store user information in a CSV file"""
    # Create the data directory if it doesn't exist
    os.makedirs('./data', exist_ok=True)
    
    user_data_path = './data/participants.csv'
    
    # Check if the file exists and write headers if it's new
    file_exists = os.path.isfile(user_data_path)
    
    with open(user_data_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Age', 'Gender', 'Timestamp'])
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([name, age, gender, timestamp])

def show_instruction_screen(test_name):
    instruction_window = create_new_window(test_name, window_type="test")
    if test_name == "StroopTest":
        app = InstructionScreen(instruction_window, "StroopTest", instruction_window.destroy)
    elif test_name == "MathTest":
        app = InstructionScreen(instruction_window, "MathTest", instruction_window.destroy)
    elif test_name == "ColdPressorTest":
        app = InstructionScreen(instruction_window, "ColdPressorTest", instruction_window.destroy)
    # TODO 3: Add the ImageTest Test
    elif test_name == "ImageTest":
        app = InstructionScreen(instruction_window, "ImageTest", instruction_window.destroy)
    elif test_name == "VideoTest":
        app = InstructionScreen(instruction_window, "VideoTest", instruction_window.destroy)
    instruction_window.mainloop()

def execute_sequence(selected_tests, ppl):
    test_sequence = load_test_sequence()
    already_relaxed = False
    
    # Tests mapping
    tests_mapping = {
        "Stroop Test": "StroopTest",
        "Mental Arithmetic Task": "MathTest",
        "Cold Pressor Test": "CPT",
        "Visual Stimulation": "ImageTest",
        "Affective Videos": "VideoTest"
    }
    
    # Extract the actual test identifiers from selected tests
    test_identifiers = []
    for test_name, selected in selected_tests.items():
        if selected.get() and test_name in tests_mapping:  # Use .get() to get the value of BooleanVar
            test_identifiers.append(tests_mapping[test_name])
    
    # Start with relaxation for all test sequences
    if test_identifiers:
        relaxation_start_time = datetime.now()
        log_event('First Relaxation Start', relaxation_start_time, None, None, username=ppl.name)
        show_relaxation_screen(duration=180)  # 3 minutes
        relaxation_end_time = datetime.now()
        duration = int((relaxation_end_time - relaxation_start_time).total_seconds() * 1000)  # Duration in milliseconds
        log_event('First Relaxation End', relaxation_start_time, relaxation_end_time, duration, username=ppl.name)
        already_relaxed = True
    
    # Run each selected test
    for test_id in test_identifiers:
        test_start_time = datetime.now()
        
        # Handle StroopTest
        if test_id == "StroopTest":
            show_instruction_screen("StroopTest")
            log_event("StroopTest Start", test_start_time, None, None, username=ppl.name)
            
            stroop_test_window = tk.Tk()
            set_responsive_geometry(stroop_test_window, "test")
            app = StroopTest(stroop_test_window, ppl.name)
            stroop_test_window.mainloop()
            
            test_end_time = datetime.now()
            duration = int((test_end_time - test_start_time).total_seconds() * 1000)
            log_event("StroopTest End", test_start_time, test_end_time, duration, username=ppl.name)
            
        # Handle MathTest
        elif test_id == "MathTest":
            show_instruction_screen("MathTest")
            log_event("MathTest Start", test_start_time, None, None, username=ppl.name)
            
            math_test_window = tk.Tk()
            set_responsive_geometry(math_test_window, "test")
            app = MathTest(math_test_window, ppl.name)
            math_test_window.mainloop()
            
            test_end_time = datetime.now()
            duration = int((test_end_time - test_start_time).total_seconds() * 1000)
            log_event("MathTest End", test_start_time, test_end_time, duration, username=ppl.name)
            
        # Handle ImageTest
        elif test_id == "ImageTest":
            show_instruction_screen("ImageTest")
            log_event("ImageTest Start", test_start_time, None, None, username=ppl.name)
            
            image_test_window = tk.Tk()
            set_responsive_geometry(image_test_window, "test")
            app = ImageTest(image_test_window, ppl.name)
            image_test_window.mainloop()
            
            test_end_time = datetime.now()
            duration = int((test_end_time - test_start_time).total_seconds() * 1000)
            log_event("ImageTest End", test_start_time, test_end_time, duration, username=ppl.name)
            
        # Handle Videos
        elif test_id == "VideoTest":
            show_instruction_screen("VideoTest")
            video_start_time = datetime.now()
            log_event('Video Feedback Start', video_start_time, None, None, username=ppl.name)
            
            video_window = tk.Tk()
            set_responsive_geometry(video_window, "test")
            app = VideoTest(video_window, ppl.name)
            video_window.mainloop()
            
            video_end_time = datetime.now()
            duration = int((video_end_time - video_start_time).total_seconds() * 1000)
            log_event('Video Feedback End', video_start_time, video_end_time, duration, username=ppl.name)
        
        # Handle Cold Pressor Test
        elif test_id == "CPT":
            show_instruction_screen("ColdPressorTest")
            cpt_start_time = datetime.now()
            log_event('Cold Pressor Test Start', cpt_start_time, None, None, username=ppl.name)
            
            show_cold_pressure_test(username=ppl.name)
            
            cpt_end_time = datetime.now()
            duration = int((cpt_end_time - cpt_start_time).total_seconds() * 1000)
            log_event('Cold Pressor Test End', cpt_start_time, cpt_end_time, duration, username=ppl.name)
    
    # Add final relaxation period before feedback
    relaxation_start_time = datetime.now()
    log_event('Final Relaxation Start', relaxation_start_time, None, None, username=ppl.name)
    show_relaxation_screen(duration=180)  # 3 minutes
    relaxation_end_time = datetime.now()
    duration = int((relaxation_end_time - relaxation_start_time).total_seconds() * 1000)  # Duration in milliseconds
    log_event('Final Relaxation End', relaxation_start_time, relaxation_end_time, duration, username=ppl.name)
    
    # Final feedback screen
    feedback_window = tk.Tk()
    set_responsive_geometry(feedback_window, "main")
    app = FeedbackScreen(feedback_window, ppl.name)
    feedback_window.mainloop()
    
    # Record the end of the program
    program_end_time = datetime.now()
    duration = int((program_end_time - program_start_time).total_seconds() * 1000)
    log_event('Program End', program_start_time, program_end_time, duration, username=ppl.name)

def main():
    pre_window = create_new_window("Cognitive Experiments", window_type="main")
    
    # Get the actual window dimensions now that it's sized responsively
    window_width = pre_window.winfo_width()
    window_height = pre_window.winfo_height()
    if window_width <= 1:  # Window not fully initialized yet
        window_width, window_height = get_responsive_window_size("main")
    
    canvas_main = tk.Canvas(pre_window, width=window_width, height=window_height, bg="white")
    canvas_main.pack(fill="both", expand=True)

    # Title
    label_title = tk.Label(pre_window, text="Cognitive Experiments", font=("SF Pro Display", 48, "bold"), bg="white", fg="#007AFF")
    canvas_main.create_window(window_width//2, 60, window=label_title)

    # Directions
    directions1 = tk.Label(pre_window, text="Select the experiments you would like to participate in.", font=("SF Pro Text", 15), bg="white", fg="#3a3d42")
    canvas_main.create_window(window_width//2, 115, window=directions1)
    directions2 = tk.Label(pre_window, text="Your responses will be recorded. The session duration will vary based on your selection.", font=("SF Pro Text", 15), bg="white", fg="#3a3d42")
    canvas_main.create_window(window_width//2, 140, window=directions2)

    # Create a main content frame to organize everything
    main_content = tk.Frame(pre_window, bg="white")
    canvas_main.create_window(window_width//2, window_height//2, window=main_content)
    
    # Test selection frame - left side
    test_selection_frame = tk.Frame(main_content, bg="white")
    test_selection_frame.grid(row=0, column=0, padx=(0, 20), sticky="n")
    
    # User information frame - right side
    user_info_frame = tk.Frame(main_content, bg="white")
    user_info_frame.grid(row=0, column=1, padx=(20, 0), sticky="n")
    
    # Test selection label
    test_selection_label = tk.Label(test_selection_frame, text="Select Tests:", font=("SF Pro Text", 18, "bold"), bg="white", fg="#007AFF")
    test_selection_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
    
    # Dictionary to store checkboxes states
    checkbox_vars = {
        "Stroop Test": tk.BooleanVar(),
        "Mental Arithmetic Task": tk.BooleanVar(),
        "Cold Pressor Test": tk.BooleanVar(),
        "Visual Stimulation": tk.BooleanVar(),
        "Affective Videos": tk.BooleanVar()
    }
    
    # Create preset variables
    stress_test_var = tk.BooleanVar()
    all_tests_var = tk.BooleanVar()
    
    # Function to handle stress test checkbox
    def toggle_stress_test():
        if stress_test_var.get():
            checkbox_vars["Stroop Test"].set(True)
            checkbox_vars["Mental Arithmetic Task"].set(True)
        else:
            # Only uncheck if All Tests is not checked
            if not all_tests_var.get():
                checkbox_vars["Stroop Test"].set(False)
                checkbox_vars["Mental Arithmetic Task"].set(False)
        update_start_button()
                
    # Function to handle all tests checkbox
    def toggle_all_tests():
        for var in checkbox_vars.values():
            var.set(all_tests_var.get())
        # Also set stress test checkbox if all tests are checked
        stress_test_var.set(all_tests_var.get())
        update_start_button()
    
    # Function to update preset checkboxes based on individual selections
    def update_presets():
        # Check if all tests are selected
        all_selected = all(var.get() for var in checkbox_vars.values())
        if all_selected and not all_tests_var.get():
            all_tests_var.set(True)
        elif not all_selected and all_tests_var.get():
            all_tests_var.set(False)
            
        # Check if stress test conditions are met
        stress_conditions_met = checkbox_vars["Stroop Test"].get() and checkbox_vars["Mental Arithmetic Task"].get()
        if stress_conditions_met and not stress_test_var.get():
            stress_test_var.set(True)
        elif not stress_conditions_met and stress_test_var.get():
            stress_test_var.set(False)
        
        update_start_button()
    
    # Create checkboxes for individual tests
    row = 1
    for test_name, var in checkbox_vars.items():
        cb = tk.Checkbutton(
            test_selection_frame, 
            text=test_name, 
            variable=var, 
            font=("SF Pro Text", 14),
            bg="white",
            fg="#3a3d42",
            selectcolor="#E5F1FE",
            command=update_presets,
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=5
        )
        cb.grid(row=row, column=0, sticky="w", pady=5)
        row += 1
    
    # Add a separator
    separator = tk.Frame(test_selection_frame, height=1, width=300, bg="#E5E5EA")
    separator.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
    row += 1
    
    # Create preset checkboxes
    preset_label = tk.Label(test_selection_frame, text="Presets:", font=("SF Pro Text", 16, "bold"), bg="white", fg="#007AFF")
    preset_label.grid(row=row, column=0, sticky="w", pady=(5, 5))
    row += 1
    
    # Stress Test preset
    stress_cb = tk.Checkbutton(
        test_selection_frame, 
        text="Stress Test [Stroop + Arithmetic]", 
        variable=stress_test_var, 
        font=("SF Pro Text", 14),
        bg="white",
        fg="#3a3d42",
        selectcolor="#E5F1FE",
        command=toggle_stress_test,
        borderwidth=0,
        highlightthickness=0,
        padx=10,
        pady=5
    )
    stress_cb.grid(row=row, column=0, sticky="w", pady=5)
    row += 1
    
    # All Tests preset
    all_cb = tk.Checkbutton(
        test_selection_frame, 
        text="All Tests", 
        variable=all_tests_var, 
        font=("SF Pro Text", 14),
        bg="white",
        fg="#3a3d42",
        selectcolor="#E5F1FE",
        command=toggle_all_tests,
        borderwidth=0,
        highlightthickness=0,
        padx=10,
        pady=5
    )
    all_cb.grid(row=row, column=0, sticky="w", pady=5)
    
    # User Information section
    label_user_info = tk.Label(user_info_frame, text="User Information", font=("SF Pro Text", 18, "bold"), bg="white", fg="#007AFF")
    label_user_info.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
    
    # Name
    label_enter_name = tk.Label(user_info_frame, text="Name:", font=("SF Pro Text", 14), bg="white", fg="#3a3d42")
    label_enter_name.grid(row=1, column=0, sticky="e", pady=5, padx=5)
    
    entry_name = tk.Entry(user_info_frame, font=("SF Pro Text", 14), bg="#F2F2F7", fg="#3a3d42", highlightthickness=0, borderwidth=0, relief="flat")
    entry_name.grid(row=1, column=1, sticky="w", pady=5, padx=5)
    entry_name.config(width=20)
    
    # Age
    label_enter_age = tk.Label(user_info_frame, text="Age:", font=("SF Pro Text", 14), bg="white", fg="#3a3d42")
    label_enter_age.grid(row=2, column=0, sticky="e", pady=5, padx=5)
    
    entry_age = tk.Entry(user_info_frame, font=("SF Pro Text", 14), bg="#F2F2F7", fg="#3a3d42", highlightthickness=0, borderwidth=0, relief="flat")
    entry_age.grid(row=2, column=1, sticky="w", pady=5, padx=5)
    entry_age.config(width=20)
    
    # Gender
    label_enter_gender = tk.Label(user_info_frame, text="Gender:", font=("SF Pro Text", 14), bg="white", fg="#3a3d42")
    label_enter_gender.grid(row=3, column=0, sticky="e", pady=5, padx=5)
    
    entry_gender = tk.Entry(user_info_frame, font=("SF Pro Text", 14), bg="#F2F2F7", fg="#3a3d42", highlightthickness=0, borderwidth=0, relief="flat")
    entry_gender.grid(row=3, column=1, sticky="w", pady=5, padx=5)
    entry_gender.config(width=20)
    
    # Create a custom styled button class for better control
    # Start button with Apple-style appearance (initially disabled)
    start_button = CustomButton(
        pre_window,
        text="Start",
        font=("SF Pro Text", 16, "bold"),
        bg="#CCCCCC",  # Initially gray
        fg="white",
        activebackground="#0062CC",
        activeforeground="white",
        borderwidth=0,
        padx=30,
        pady=10,
        relief="flat",
        command=lambda: get_user_name(pre_window, entry_name, entry_age, entry_gender, canvas_main, checkbox_vars),
        state="disabled"  # Initially disabled
    )
    canvas_main.create_window(window_width//2, int(window_height * 0.85), window=start_button)
    
    # Function to update start button state
    def update_start_button():
        # Check if all fields are filled and at least one test is selected
        name_filled = len(entry_name.get().strip()) > 0
        age_filled = len(entry_age.get().strip()) > 0
        gender_filled = len(entry_gender.get().strip()) > 0
        any_test_selected = any(var.get() for var in checkbox_vars.values())
        
        if name_filled and age_filled and gender_filled and any_test_selected:
            # Use the custom method which properly handles all styling
            start_button.set_state("normal", "#007AFF")
        else:
            # Use the custom method to disable
            start_button.set_state("disabled")
    
    # Bind entry field changes to update button state
    entry_name.bind("<KeyRelease>", lambda e: update_start_button())
    entry_age.bind("<KeyRelease>", lambda e: update_start_button())
    entry_gender.bind("<KeyRelease>", lambda e: update_start_button())
    
    ppl = Participant()
    
    def get_user_name(windw, name_entry, age_entry, gender_entry, canvas, selected_tests):
        # Get user information
        user_name = name_entry.get().strip()
        user_age = age_entry.get().strip()
        user_gender = gender_entry.get().strip()
        
        # Store user information
        store_user_info(user_name, user_age, user_gender)
        
        # Update participant object
        ppl.name = user_name
        try:
            ppl.age = int(user_age)
        except ValueError:
            ppl.age = 0  # Default if conversion fails
        
        # Start program timing
        global program_start_time
        program_start_time = datetime.now()
        log_event('Program Start', program_start_time, None, None, username=ppl.name)
        
        # Close current window and proceed with test sequence
        windw.destroy()
        execute_sequence(selected_tests, ppl)

    while True:
        if ppl.name != "New_User":
            break
        pre_window.update()

if __name__ == "__main__":
    main()
