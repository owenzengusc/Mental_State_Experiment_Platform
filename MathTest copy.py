import tkinter as tk
from tkinter import ttk
import random
import csv
import time

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
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        
        self.question_label = tk.Label(self.root, font=("Arial", 140), bg="black", fg="white")
        self.question_label.pack(pady=50, expand=True)
        
        # Create a style object
        style = ttk.Style()

        # Configure the font for TButton style
        style.configure('TButton', font=('Arial', 40))  # Increase 20 to your desired font size


        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=20)
        
        self.option_buttons = []
        
        for i in range(4):
            btn = ttk.Button(self.buttons_frame, text="")
            btn.pack(side=tk.LEFT, padx=10)
            btn.bind('<Button>', lambda event, idx=i: self.check_answer(idx)) 
            btn.config (state=tk.DISABLED)
            self.option_buttons.append(btn)
            
        self.start_time = time.time()
        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(self.start_time))
        self.write_header_to_csv()
        self.countdown(COUNTDOWN)
        self.callback = callback

    def countdown(self, count):
        if count > 0:
            self.question_label.config(text=str(count))
            self.root.after(1000, self.countdown, count-1)
        else:
            self.question_label.config(text="")
            self.generate_question()
            self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"Time: {self.remaining_time}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def generate_question(self):
        if self.remaining_time <= 0:
            return

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
        
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=str(options[i]), state=tk.NORMAL)

        self.answered = False
        if self.current_timer_id:
            self.root.after_cancel(self.current_timer_id)
        self.current_timer_id = self.root.after(QUESTION_DISPLAY_TIME * 1000, self.hide_question)

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
        self.answered = True
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
        self.generate_question()


    def hide_question(self):
        if not self.answered:
            self.total_questions += 1
            self.miss_count += 1
            self.write_miss_to_csv()
            self.generate_question()

    def end_game(self):
        # Cancel any scheduled tasks
        if self.current_timer_id:
            self.root.after_cancel(self.current_timer_id)
        self.answered = True
        self.question_label.config(text="Game Over!")
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        self.write_summary_to_csv()
        # close the window after 2s
        self.root.after(2000, self.root.destroy) 
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
        # Center the window
    window_width = 1800  # Set to your desired width
    window_height = 1000  # Set to your desired height

        
    # Fix the window size
    root.minsize(window_width, window_height)  # Set to your desired width and height
    root.maxsize(1960, 1080)  # Set to your desired width and height

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    app = MathTest(root, "testUser")
    root.mainloop()