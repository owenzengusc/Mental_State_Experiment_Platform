import tkinter as tk
from tkinter import ttk
import random
import csv
import time


# Total game time in seconds
TOTAL_GAME_TIME = 60*5

# Define your constants outside the class
MAX_NUM_OPERATIONS = 7  # Maximum number of operations
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
        self.total_questions = 0
        self.remaining_time = TOTAL_GAME_TIME
        self.question_start_time = 0  # Initialize the question start time
        self.min_num_operations = MIN_NUM_OPERATIONS  # Initial value
        self.max_num_operations = MIN_NUM_OPERATIONS  # Initial value
        self.prev_correct_option_idx = None
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        
        self.question_label = tk.Label(self.root, font=("Arial", 30), bg="black", fg="white")
        self.question_label.pack(pady=50, expand=True)
        
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
        
        self.question_start_time = time.time()  # Record the time the question is displayed
        self.expression, self.answer = self.create_math_expression()
        self.question_label.config(text=self.expression)
        
        options = [self.answer]
        while len(options) < 4:
            option = random.randint(1, 100)
            if option not in options:
                options.append(option)
        
        # Shuffle the options until the correct answer is in a different position
        while True:
            random.shuffle(options)
            self.correct_option_idx = options.index(self.answer)  # Get the index of the correct answer after shuffling
            if self.correct_option_idx != self.prev_correct_option_idx:  # Check if it's different from the previous correct answer position
                break  # If it is, break out of the loop
        
        self.prev_correct_option_idx = self.correct_option_idx  # Update the previous correct answer position
        
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=str(options[i]), state=tk.NORMAL)

    def create_math_expression(self):
        while True:
            answer = random.randint(1, 99)
            operators = ['+', '-', '*', '/']
            num_ops = random.randint(self.min_num_operations, self.max_num_operations)
            ops = random.choices(operators, k=num_ops)
            nums = [random.randint(1, 99) for _ in range(num_ops+1)]

            expression_parts = [str(nums[0])]
            for i in range(num_ops):
                if ops[i] == '/':
                    if answer == 1:
                        nums[i+1] = 2
                    else:
                        nums[i+1] = random.randint(2, min(99, answer))
                    nums[i] = nums[i+1] * random.randint(1, 99)
                elif ops[i] == '*':
                    if nums[i] == 1:
                        nums[i] = random.randint(2, 99)
                    elif nums[i+1] == 1:
                        nums[i+1] = random.randint(2, 99)
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
        self.total_questions += 1
        answer_time = time.time() - self.question_start_time  # Calculate the time taken to answer
        correct = idx == self.correct_option_idx  # Check if the answer is correct
        self.adjust_difficulty(answer_time, correct)  # Adjust the difficulty based on answer time and correctness
        if correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1
        self.update_score()
        self.write_data_to_csv(idx)
        self.generate_question()
        
    def adjust_difficulty(self, answer_time, correct):
        if correct and answer_time < TIME_THRESHOLD:  # If answer is correct and within time threshold
            self.max_num_operations = min(self.max_num_operations + DIFFICULTY_INCREMENT, MAX_NUM_OPERATIONS)
            self.min_num_operations = self.max_num_operations-1

    def update_score(self):
        pass

    def end_game(self):
        self.question_label.config(text="Game Over")
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        self.write_summary_to_csv()
        self.root.after(2000, self.root.destroy) 
        if self.callback:
            self.callback()

    def write_data_to_csv(self, user_choice_idx):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        user_choice = self.option_buttons[user_choice_idx].cget("text")
        relative_time = int((time.time() - self.start_time) * 1000)  # Convert to milliseconds
        result = "Correct" if user_choice == str(self.answer) else "Incorrect"
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.expression, self.answer, user_choice, result])

    def write_summary_to_csv(self):
        # Read the entire CSV file into memory
        with open(self.path_to_file, 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            # Insert the summary rows at the top
            lines.insert(0, ["Start Time", "Total Questions", "Total Correct", "Total Wrong", "Min Operation", "Max Operation",self.username])
            lines.insert(1, [self.start_time_header, self.total_questions, self.correct_count, self.wrong_count, MIN_NUM_OPERATIONS, MAX_NUM_OPERATIONS])
    
        # Write the modified content back to the CSV file
        with open(self.path_to_file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            writer.writerow(["Start Time", "Total Questions", "Total Correct", "Total Wrong", "Min Operation", "Max Operation", self.username])
            writer.writerow([self.start_time_header, self.total_questions, self.correct_count, self.wrong_count, MIN_NUM_OPERATIONS, MAX_NUM_OPERATIONS])

    def write_header_to_csv(self):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date Time", "Relative Time", "Expression", "Answer", "User Choice", "Result", self.username])
           
if __name__ == "__main__":
    root = tk.Tk()
    
    # Fix the window size
    root.minsize(800, 600)  # Set to your desired width and height
    root.maxsize(800, 600)  # Set to your desired width and height

    # Center the window
    window_width = 800  # Set to your desired width
    window_height = 600  # Set to your desired height

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))

    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    username = input("Enter your name: ")
    app = MathTest(root, username)
    root.mainloop()
