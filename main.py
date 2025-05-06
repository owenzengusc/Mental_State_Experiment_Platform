# Mental State Experiment Platform
# Authors: Owen Zeng, Kaiden Ko
# https://github.com/owenzengusc/Mental_State_Experiment_Platform

from window import *
from user import *
from StroopTest import *
from MathTest import *
from ImageTest import * 
from ColdPressorTest import *
from FeedbackScreen import FeedbackScreen
from InstructionScreen import InstructionScreen
from video import VideoTest
from RelaxationScreen import show_relaxation_screen
from datetime import datetime
from window_utils import set_responsive_geometry, get_responsive_window_size
import tkinter as tk # Ensure tkinter is imported
from tkinter import messagebox # Add messagebox import
import json
import csv
import os
import logging # Add logging import
import sys # Add sys import for exception hook

# --- Setup Logging ---
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO, # Set to DEBUG for more verbose output
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler() # Also log to console
    ]
)

logger = logging.getLogger(__name__)

# Global exception handler
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log KeyboardInterrupt
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
# --- End Logging Setup ---

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
    try:
        logger.info("Loading test sequence from ./test/test.json")
        # Check if running as executable
        if getattr(sys, 'frozen', False):
            # If running as executable, use the path relative to sys._MEIPASS
            base_path = sys._MEIPASS
        else:
            # Otherwise, use the script's directory
            base_path = os.path.dirname(__file__)
        test_file_path = os.path.join(base_path, 'test', 'test.json')
        logger.info(f"Resolved test file path: {test_file_path}")
        with open(test_file_path, 'r') as file:
            data = json.load(file)
            logger.info("Test sequence loaded successfully.")
            return data["Test_List"]
    except FileNotFoundError:
        logger.error(f"Error: test.json not found at {test_file_path}. Please ensure the file exists.")
        # Optionally, return a default sequence or raise the error
        return [] # Return empty list or handle as appropriate
    except Exception as e:
        logger.exception(f"Failed to load or parse test sequence: {e}")
        return [] # Return empty list or handle as appropriate

def log_event(event_name, start_time, end_time, duration, username='New_User'):
    logger.info(f"CSV_LOG: Event='{event_name}', Start='{start_time}', End='{end_time}', Duration='{duration}', User='{username}'")
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
    logger.info(f"Storing user info: Name='{name}', Age='{age}', Gender='{gender}'")
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
    logger.info(f"Showing instruction screen for test: {test_name}")
    try:
        instruction_window = create_new_window(test_name, window_type="test")
        # Correct indentation for the if/elif block
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
    except Exception as e:
        logger.exception(f"Error showing instruction screen for {test_name}: {e}")
        # Optionally close the window or show an error message
        if 'instruction_window' in locals() and instruction_window.winfo_exists():
            instruction_window.destroy()

def execute_sequence(selected_tests, ppl):
    logger.info(f"Starting execute_sequence for user: {ppl.name}")
    logger.info(f"Selected tests: { {k: v.get() for k, v in selected_tests.items()} }")
    try:
        test_sequence = load_test_sequence()
        if not test_sequence:
            logger.warning("Test sequence is empty. Cannot proceed.")
            # Maybe show an error message to the user here?
            return
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
            logger.info(f"Starting test: {test_id}")
            test_start_time = datetime.now()
            try:
                # Handle StroopTest
                if test_id == "StroopTest":
                    show_instruction_screen("StroopTest")
                    log_event("StroopTest Start", test_start_time, None, None, username=ppl.name)
                    logger.info("Creating StroopTest window")
                    stroop_test_window = tk.Tk()
                    set_responsive_geometry(stroop_test_window, "test")
                    app = StroopTest(stroop_test_window, ppl.name)
                    logger.info("Running StroopTest mainloop")
                    stroop_test_window.mainloop()
                    logger.info("StroopTest mainloop finished")
                    test_end_time = datetime.now()
                    duration = int((test_end_time - test_start_time).total_seconds() * 1000)
                    log_event("StroopTest End", test_start_time, test_end_time, duration, username=ppl.name)
                    logger.info(f"StroopTest finished. Duration: {duration}ms")
                # Handle MathTest
                elif test_id == "MathTest":
                    show_instruction_screen("MathTest")
                    log_event("MathTest Start", test_start_time, None, None, username=ppl.name)
                    logger.info("Creating MathTest window")
                    math_test_window = tk.Tk()
                    set_responsive_geometry(math_test_window, "test")
                    app = MathTest(math_test_window, ppl.name)
                    logger.info("Running MathTest mainloop")
                    math_test_window.mainloop()
                    logger.info("MathTest mainloop finished")
                    test_end_time = datetime.now()
                    duration = int((test_end_time - test_start_time).total_seconds() * 1000)
                    log_event("MathTest End", test_start_time, test_end_time, duration, username=ppl.name)
                    logger.info(f"MathTest finished. Duration: {duration}ms")
                # Handle ImageTest
                elif test_id == "ImageTest":
                    show_instruction_screen("ImageTest")
                    log_event("ImageTest Start", test_start_time, None, None, username=ppl.name)
                    logger.info("Creating ImageTest window")
                    image_test_window = tk.Tk()
                    set_responsive_geometry(image_test_window, "test")
                    app = ImageTest(image_test_window, ppl.name)
                    logger.info("Running ImageTest mainloop")
                    image_test_window.mainloop()
                    logger.info("ImageTest mainloop finished")
                    test_end_time = datetime.now()
                    duration = int((test_end_time - test_start_time).total_seconds() * 1000)
                    log_event("ImageTest End", test_start_time, test_end_time, duration, username=ppl.name)
                    logger.info(f"ImageTest finished. Duration: {duration}ms")
                # Handle Videos
                elif test_id == "VideoTest":
                    show_instruction_screen("VideoTest")
                    video_start_time = datetime.now()
                    log_event('Video Feedback Start', video_start_time, None, None, username=ppl.name)
                    logger.info("Creating VideoTest window")
                    video_window = tk.Tk()
                    set_responsive_geometry(video_window, "test")
                    app = VideoTest(video_window, ppl.name)
                    logger.info("Running VideoTest mainloop")
                    video_window.mainloop()
                    logger.info("VideoTest mainloop finished")
                    video_end_time = datetime.now()
                    duration = int((video_end_time - video_start_time).total_seconds() * 1000)
                    log_event('Video Feedback End', video_start_time, video_end_time, duration, username=ppl.name)
                    logger.info(f"VideoTest finished. Duration: {duration}ms")
                # Handle Cold Pressor Test
                elif test_id == "CPT":
                    show_instruction_screen("ColdPressorTest")
                    cpt_start_time = datetime.now()
                    log_event('Cold Pressor Test Start', cpt_start_time, None, None, username=ppl.name)
                    logger.info("Showing Cold Pressor Test")
                    show_cold_pressure_test(username=ppl.name)
                    logger.info("Cold Pressor Test finished")
                    cpt_end_time = datetime.now()
                    duration = int((cpt_end_time - cpt_start_time).total_seconds() * 1000)
                    log_event('Cold Pressor Test End', cpt_start_time, cpt_end_time, duration, username=ppl.name)
                    logger.info(f"Cold Pressor Test finished. Duration: {duration}ms")
            except Exception as e:
                logger.exception(f"Error during execution of test {test_id}: {e}")
                # Decide if you want to continue with the next test or stop
                # continue # or break
        
        # Add final relaxation period before feedback
        logger.info("Starting final relaxation period")
        relaxation_start_time = datetime.now()
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
        # Calculate total program duration relative to a start time defined in main()
        # duration = int((program_end_time - program_start_time).total_seconds() * 1000)
        # log_event('Program End', program_start_time, program_end_time, duration, username=ppl.name)
        logger.info(f"execute_sequence finished for user: {ppl.name}")

    except Exception as e:
        logger.exception(f"An error occurred during execute_sequence for user {ppl.name}: {e}")
        # Optionally, display an error message to the user via Tkinter messagebox
        # messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def main():
    logger.info("Application starting")
    program_start_time = datetime.now() # Define program_start_time here
    os.makedirs('./data', exist_ok=True) # Ensure data directory exists
    log_event('Program Start', program_start_time, None, None) # Log program start
    
    # Define start_button and user info entries early so update_start_button can access them
    start_button = None
    name_entry = None
    age_entry = None
    gender_var = None
    checkbox_vars = {}

    # Function to update start button state (Moved earlier)
    def update_start_button():
        # Check if any test is selected
        any_test_selected = any(var.get() for var in checkbox_vars.values())
        # Check if user info is filled (ensure widgets exist before accessing .get())
        user_info_filled = False
        if name_entry and age_entry and gender_var:
             user_info_filled = name_entry.get().strip() and age_entry.get().strip() and gender_var.get() != "Select Gender"
        
        if start_button: # Ensure button exists
            if any_test_selected and user_info_filled:
                start_button.set_state("normal", bg_color="#007AFF")
            else:
                start_button.set_state("disabled")

    try:
        pre_window = create_new_window("Cognitive Experiments", window_type="main")
        logger.info("Main window created")
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
        
        # Dictionary to store checkboxes states (Initialize checkbox_vars here)
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
        name_entry = entry_name
        entry_name.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        entry_name.config(width=20)
        entry_name.bind("<KeyRelease>", lambda event: update_start_button()) # Bind after definition
        
        # Age
        label_enter_age = tk.Label(user_info_frame, text="Age:", font=("SF Pro Text", 14), bg="white", fg="#3a3d42")
        label_enter_age.grid(row=2, column=0, sticky="e", pady=5, padx=5)
        
        entry_age = tk.Entry(user_info_frame, font=("SF Pro Text", 14), bg="#F2F2F7", fg="#3a3d42", highlightthickness=0, borderwidth=0, relief="flat")
        age_entry = entry_age
        entry_age.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        entry_age.config(width=20)
        entry_age.bind("<KeyRelease>", lambda event: update_start_button()) # Bind after definition
        
        # Gender
        label_enter_gender = tk.Label(user_info_frame, text="Gender:", font=("SF Pro Text", 14), bg="white", fg="#3a3d42")
        label_enter_gender.grid(row=3, column=0, sticky="e", pady=5, padx=5)
        
        # Use Combobox for Gender for better UX
        gender_var = tk.StringVar(user_info_frame)
        gender_var.set("Select Gender") # default value
        gender_options = ["Select Gender", "Male", "Female", "Non-binary", "Prefer not to say"]
        gender_dropdown = tk.OptionMenu(user_info_frame, gender_var, *gender_options)
        gender_dropdown.config(font=("SF Pro Text", 14), bg="#F2F2F7", fg="#3a3d42", highlightthickness=0, borderwidth=0, relief="flat", width=17, anchor='w')
        gender_dropdown["menu"].config(font=("SF Pro Text", 14), bg="white")
        gender_dropdown.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        gender_var.trace_add("write", lambda *args: update_start_button()) # Bind after definition

        # Create a custom styled button class for better control
        # Start button with Apple-style appearance (initially disabled)
        start_button = CustomButton(
            main_content, # Place in main_content grid
            text="Start Experiment",
            font=("SF Pro Display", 18, "bold"),
            fg="white",
            bg="#CCCCCC", # Start disabled
            activebackground="#005ECC",
            borderwidth=0,
            padx=20,
            pady=10,
            relief="flat",
            command=lambda: start_experiment(), # Corrected command call
            state="disabled"  # Initially disabled
        )
        # canvas_main.create_window(window_width//2, int(window_height * 0.85), window=start_button) # Remove canvas placement
        start_button.grid(row=1, column=0, columnspan=2, pady=20) # Grid placement
        
        # Function to update start button state (REMOVE DUPLICATE DEFINITION)
        # def update_start_button():
        #     # Check if any test is selected
        #     any_test_selected = any(var.get() for var in checkbox_vars.values())
        #     # Check if user info is filled
        #     user_info_filled = name_entry.get().strip() and age_entry.get().strip() and gender_var.get() != "Select Gender"
        #     
        #     if any_test_selected and user_info_filled:
        #         start_button.set_state("normal", bg_color="#007AFF")
        #     else:
        #         start_button.set_state("disabled")
        
        # Bind update function to changes in user info fields (REMOVE DUPLICATE BINDINGS)
        # name_entry.bind("<KeyRelease>", lambda event: update_start_button())
        # age_entry.bind("<KeyRelease>", lambda event: update_start_button())
        # gender_var.trace_add("write", lambda *args: update_start_button())
    
        # Function to start the experiment
        def start_experiment():
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_var.get()
            
            logger.info(f"Start button clicked. Name: {name}, Age: {age}, Gender: {gender}")
            
            # Basic validation (could be more robust)
            if not name or not age or gender == "Select Gender":
                logger.warning("Attempted to start experiment with incomplete user info.")
                # Optionally show a message to the user
                # messagebox.showwarning("Incomplete Information", "Please fill in all participant details.")
                return
            
            try:
                # Validate age is a number
                int(age)
            except ValueError:
                logger.warning(f"Invalid age entered: {age}")
                # Optionally show a message to the user
                # messagebox.showerror("Invalid Input", "Please enter a valid number for age.")
                return
    
            # Store user info
            store_user_info(name, age, gender)
            
            # Create participant object
            ppl = Participant(name, age, gender)
            logger.info(f"Participant object created: {ppl}")
            
            # Close the pre-window
            logger.info("Closing pre-window")
            pre_window.destroy()
            
            # Execute the selected test sequence
            logger.info("Calling execute_sequence")
            try:
                execute_sequence(checkbox_vars, ppl)
                logger.info("execute_sequence completed successfully.")
            except Exception as e:
                logger.exception(f"Error occurred during execute_sequence call: {e}")
                # Optionally, inform the user that an error occurred during the tests
                # You might want a simple Tkinter window here if all others are closed
                error_window = tk.Tk()
                error_window.withdraw() # Hide the main window
                messagebox.showerror("Experiment Error", f"An error occurred during the experiment: {e}\n\nPlease check the app.log file for details.", parent=None)
                error_window.destroy()
    
        # Start button (REMOVE DUPLICATE DEFINITION)
        # start_button = CustomButton(
        #     main_content, 
        #     text="Start Experiment", 
        #     font=("SF Pro Display", 18, "bold"), 
        #     fg="white", 
        #     bg="#CCCCCC", # Start disabled
        #     activebackground="#005ECC", 
        #     command=start_experiment, 
        #     state="disabled",
        #     relief="flat",
        #     padx=20,
        #     pady=10
        # )
        # start_button.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Initial check for button state
        update_start_button()
        
        logger.info("Entering main loop for pre_window")
        pre_window.mainloop()
        logger.info("Exited main loop for pre_window")
    
    except Exception as e:
        logger.exception(f"An error occurred in the main function: {e}")
        # Attempt to show an error message if Tkinter is still usable
        try:
            error_window = tk.Tk()
            error_window.withdraw() # Hide the main window
            messagebox.showerror("Application Error", f"A critical error occurred: {e}\n\nPlease check the app.log file for details.", parent=None)
            error_window.destroy()
        except Exception as tk_error:
            logger.error(f"Could not display Tkinter error message: {tk_error}")
            
        finally:
            # Log program end time relative to start time
            program_end_time = datetime.now()
            total_duration = int((program_end_time - program_start_time).total_seconds() * 1000)
            log_event('Program End', program_start_time, program_end_time, total_duration)
            logger.info(f"Application finished. Total duration: {total_duration}ms")

if __name__ == "__main__":
    main()
