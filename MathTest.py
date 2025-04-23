import tkinter as tk
from tkinter import ttk
import random
import csv
import time
import threading

# Total game time in seconds
TOTAL_GAME_TIME = 60*3

# Time each question will be displayed in seconds
QUESTION_DISPLAY_TIME = 7

# Define your constants outside the class
MAX_NUM_OPERATIONS = 3  # Maximum number of operations
MIN_NUM_OPERATIONS = 1  # Minimum number of operations
DIFFICULTY_INCREMENT = 1  # How much to increment the difficulty by
TIME_THRESHOLD = 20  # Set your time threshold here

# Possibility of including parentheses in the expression
PARENTHESIS_PROBABILITY = 0.7

# Countdown before game start
COUNTDOWN = 5

# Path to the folder where the data will be stored
PATH = './data/'

class MathTest:
    def __init__(self, root, username, callback=None):
        self.root = root
        self.root.title("Math Test")
        self.root.configure(bg="black")
        
        # Thread control flag
        self.running = True
        
        # Add proper window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.username = username
        self.path_to_file = PATH+'mathTest_'+username+'.csv'
        self.correct_count = 0
        self.wrong_count = 0
        self.miss_count = 0
        self.total_questions = 0
        self.remaining_time = TOTAL_GAME_TIME
        self.question_start_time = 0
        self.min_num_operations = MIN_NUM_OPERATIONS
        self.max_num_operations = MIN_NUM_OPERATIONS
        self.prev_correct_option_idx = None
        self.answered = True
        self.current_timer_id = None
        
        # Top frame for timer
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Time label
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white", font=("SF Pro Display", 18))
        self.time_label.pack(side=tk.LEFT)
        
        # Question label
        self.question_label = tk.Label(self.root, font=("SF Pro Display", 140), bg="black", fg="white")
        self.question_label.pack(pady=50, expand=True)
        
        # Button colors
        self.btn_bg = "#E9E9E9"
        self.btn_fg = "black"
        self.btn_active_bg = "#CCCCCC"
        self.btn_selected_bg = "#97C1A9"
        
        # Buttons frame - initialize but don't pack yet
        self.buttons_frame = tk.Frame(self.root, bg="black")
        
        # Create option buttons using native tk buttons
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame, 
                text="   ",  # Initialize with space to maintain size
                font=("SF Pro Display", 36),
                bg=self.btn_bg,
                fg=self.btn_fg,
                activebackground=self.btn_active_bg,
                activeforeground=self.btn_fg,
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=10,
                width=6,
                command=lambda idx=i: self.check_answer(idx)
            )
            self.option_buttons.append(btn)
        
        self.start_time = time.time()
        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(self.start_time))
        self.write_header_to_csv()
        
        # Audio state tracking
        self.music_playing = False
        self.pygame_initialized = False
        
        self.countdown(COUNTDOWN)
        self.callback = callback

    def on_closing(self):
        """Handle window closing event properly"""
        self.running = False  # Set flag to stop threads
        
        # Stop any music
        self.stop_music()
        
        # Cancel any pending timers
        if self.current_timer_id:
            try:
                self.root.after_cancel(self.current_timer_id)
            except Exception:
                pass
        
        # Allow time for threads to notice the flag change
        time.sleep(0.1)
        
        # Close the window
        try:
            self.root.destroy()
        except tk.TclError:
            pass  # Window might already be destroyed
            
        # Call the callback if provided
        if self.callback:
            self.callback()

    def countdown(self, count):
        if not self.running:
            return
            
        if count > 0:
            try:
                self.question_label.config(text=str(count))
                self.root.after(1000, self.countdown, count-1)
            except tk.TclError:
                pass  # Window might be destroyed
        else:
            try:
                self.question_label.config(text="")
                # Now that countdown is done, show the buttons frame
                self.buttons_frame.pack(pady=20)
                self.play_music_thread()
                self.generate_question()
                self.update_timer()
            except tk.TclError:
                pass  # Window might be destroyed
    
    def play_music(self):
        try:
            import pygame
            if not self.pygame_initialized:
                pygame.mixer.init()
                self.pygame_initialized = True
            pygame.mixer.music.load("clock.mp3")
            pygame.mixer.music.play(-1)  # Play indefinitely until stopped
            self.music_playing = True
        except Exception as e:
            print(f"Error playing music: {e}")
    
    def stop_music(self):
        try:
            if self.music_playing:
                import pygame
                if self.pygame_initialized:
                    pygame.mixer.music.stop()
                    self.music_playing = False
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def play_music_thread(self):
        self.play_music_thread = threading.Thread(target=self.play_music)
        self.play_music_thread.daemon = True
        self.play_music_thread.start()
        
    def update_timer(self):
        if not self.running:
            return
            
        if self.remaining_time > 0:
            try:
                self.remaining_time -= 1
                self.time_label.config(text=f"Time: {self.remaining_time}")
                self.root.after(1000, self.update_timer)
            except tk.TclError:
                pass  # Window might be destroyed
        else:
            self.end_game()

    def generate_question(self):
        if not self.running or self.remaining_time <= 0:
            return

        try:
            self.question_start_time = time.time()
            self.expression, self.answer = self.create_math_expression()
            self.question_label.config(text=self.expression)
            
            options = [self.answer]
            while len(options) < 4:
                option = random.randint(1, 100)
                if option not in options:
                    options.append(option)
            
            while True:
                random.shuffle(options)
                self.correct_option_idx = options.index(self.answer)
                if self.correct_option_idx != self.prev_correct_option_idx:
                    break

            self.prev_correct_option_idx = self.correct_option_idx
            
            # Configure all buttons first before showing them
            for i, btn in enumerate(self.option_buttons):
                btn.config(text=str(options[i]), bg=self.btn_bg, fg=self.btn_fg)
                # Pack each button if not already packed
                if not btn.winfo_ismapped():
                    btn.pack(side=tk.LEFT, padx=15)
            
            self.buttons_frame.update()  # Force update of the frame

            self.answered = False
            if self.current_timer_id:
                self.root.after_cancel(self.current_timer_id)
            self.current_timer_id = self.root.after(QUESTION_DISPLAY_TIME * 1000, self.hide_question)
        except tk.TclError:
            pass  # Window might be destroyed

    def create_math_expression(self):
        while True:
            answer = random.randint(1, 99)
            operators = ['+', '-', '*', '/']
            num_ops = random.randint(self.min_num_operations, self.max_num_operations)
            ops = random.choices(operators, k=num_ops)

            # Adjust the number generation based on the number of operations
            if num_ops == 3:
                # Choose a position for the two-digit number
                two_digit_pos = random.randint(0, num_ops)
                nums = [random.randint(10, 99) if i == two_digit_pos else random.randint(1, 9) for i in range(num_ops + 1)]
            elif num_ops == 2:
                # Logic for 2 operations
                one_digit_pos = random.randint(0, num_ops)
                nums = [random.randint(1, 9) if i == one_digit_pos else random.randint(10, 99) for i in range(num_ops + 1)]
            else:
                nums = [random.randint(1, 99) for _ in range(num_ops + 1)]

            expression_parts = [str(nums[0])]
            for i in range(num_ops):
                if ops[i] == '/':
                    # Additional logic for division to ensure feasible calculations
                    nums[i] = nums[i] * nums[i+1]
                elif ops[i] == '*':
                    # Additional logic for multiplication, if needed
                    pass
                expression_parts.extend([ops[i], str(nums[i+1])])
            expression = " ".join(expression_parts)
            expression_without_parentheses = expression

            # Decide whether to include parentheses
            include_parentheses = random.random() < PARENTHESIS_PROBABILITY
            if include_parentheses and num_ops > 1:
                left_paren_idx = random.randint(0, num_ops - 1) * 2
                right_paren_idx = random.randint(left_paren_idx // 2 + 1, num_ops) * 2
                expression_parts.insert(left_paren_idx, "(")
                expression_parts.insert(right_paren_idx + 2, ")")
                expression_with_parentheses = " ".join(expression_parts)
                try:
                    if eval(expression_with_parentheses) != eval(expression_without_parentheses):
                        expression = expression_with_parentheses
                except:
                    pass
            try:
                if eval(expression) == answer:
                    return expression, answer
            except:
                pass

    def check_answer(self, idx):
        if not self.running:
            return
            
        # Prevent multiple clicks
        if not self.answered:
            self.answered = True
            
            try:
                # Highlight the selected button
                for i, btn in enumerate(self.option_buttons):
                    if i == idx:
                        # Highlight selected button
                        btn.config(bg=self.btn_selected_bg)
                    else:
                        # Reset other buttons
                        btn.config(bg=self.btn_bg)
                
                self.root.update()  # Force update to show the highlight
                self.root.after(200)  # Short delay to show the selection
                
                self.total_questions += 1
                if idx == self.correct_option_idx:
                    self.correct_count += 1
                    self.write_correct_to_csv()
                    # Increase difficulty
                    if self.max_num_operations < MAX_NUM_OPERATIONS:
                        self.max_num_operations += DIFFICULTY_INCREMENT
                else:
                    self.wrong_count += 1
                    self.write_wrong_to_csv(idx)
                
                # Instead of hiding buttons, keep them visible but set to empty
                for btn in self.option_buttons:
                    btn.config(text="", bg=self.btn_bg)
                    
                # Generate the next question
                self.generate_question()
            except tk.TclError:
                pass  # Window might be destroyed

    def hide_question(self):
        if not self.running:
            return
            
        try:
            if not self.answered:
                self.total_questions += 1
                self.miss_count += 1
                self.write_miss_to_csv()
                
                # Instead of hiding buttons, keep them visible but set to empty
                for btn in self.option_buttons:
                    btn.config(text="", bg=self.btn_bg)
                    
                self.generate_question()
        except tk.TclError:
            pass  # Window might be destroyed

    def end_game(self):
        if not self.running:
            return
            
        # Cancel any scheduled tasks
        if self.current_timer_id:
            self.root.after_cancel(self.current_timer_id)
            
        self.running = False
        self.answered = True
        
        try:
            self.question_label.config(text="Game Over!")
            
            # Keep buttons visible but empty for consistent layout
            for btn in self.option_buttons:
                btn.config(text="", state=tk.DISABLED)
        except tk.TclError:
            pass  # Window might be destroyed
            
        self.write_summary_to_csv()
        
        # stop the music
        self.stop_music()
        
        # close the window after 2s
        try:
            self.root.after(2000, self.root.destroy) 
        except tk.TclError:
            pass  # Window might be destroyed
            
        if self.callback:
            self.callback()

    def write_header_to_csv(self):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Relative Time (ms)", "Expression", "Answer", "Selected Option", "Correctness", self.username])

    def write_correct_to_csv(self):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.expression, self.answer, self.answer, "CORRECT"])

    def write_wrong_to_csv(self, idx):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.expression, self.answer, self.option_buttons[idx].cget("text"), "WRONG"])

    def write_miss_to_csv(self):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.expression, self.answer, "MISS", "MISS"])

    def write_data_to_csv(self, user_choice_idx):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        user_choice = self.option_buttons[user_choice_idx].cget("text")
        relative_time = int((time.time() - self.start_time) * 1000)  # Convert to milliseconds
        result = "Correct" if user_choice == str(self.answer) else "Incorrect"
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.expression, self.answer, user_choice, result, self.username])

    def write_summary_to_csv(self):
        # Read the entire CSV file into memory
        with open(self.path_to_file, 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            # Insert the summary rows at the top
            lines.insert(0, ["Start Time", "Total Questions", "Total Correct", "Total Wrong", "Total Miss", "Min Operation", "Max Operation", "Question Display Time (s)", self.username])
            lines.insert(1, [self.start_time_header, self.total_questions, self.correct_count, self.wrong_count, self.miss_count, MIN_NUM_OPERATIONS, MAX_NUM_OPERATIONS, QUESTION_DISPLAY_TIME])
    
        # Write the modified content back to the CSV file
        with open(self.path_to_file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            writer.writerow(["Start Time", "Total Questions", "Total Correct", "Total Wrong", "Total Miss", "Min Operation", "Max Operation", "Question Display Time (s)", self.username])
            writer.writerow([self.start_time_header, self.total_questions, self.correct_count, self.wrong_count, self.miss_count, MIN_NUM_OPERATIONS, MAX_NUM_OPERATIONS, QUESTION_DISPLAY_TIME])

if __name__ == "__main__":
    root = tk.Tk()
    
    # Get responsive window size (85% of screen)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.85)
    window_height = int(screen_height * 0.85)
    
    # Ensure window size is reasonable
    window_width = min(window_width, 1920)
    window_height = min(window_height, 1080)
    
    # Set minimum size constraints
    window_width = max(window_width, 1200)
    window_height = max(window_height, 800)
    
    # Apply the window geometry
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    # Set reasonable min/max sizes
    root.minsize(min(window_width, 1000), min(window_height, 700))
    root.maxsize(screen_width, screen_height)
    
    app = MathTest(root, "testUser")
    root.mainloop()