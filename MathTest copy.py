import tkinter as tk
import random
import csv
import math

# Total game time in seconds
TOTAL_GAME_TIME = 60

# Path to the folder where the data will be stored
PATH = './data/'

class MathTest:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Math Test")
        self.root.configure(bg="black")
        
        self.username = username
        self.path_to_file = PATH+'mathTest_'+username+'.csv'
        self.correct_count = 0
        self.wrong_count = 0
        self.total_questions = 0
        self.remaining_time = TOTAL_GAME_TIME
        
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(self.top_frame, text="Correct: 0   Wrong: 0", anchor='e', bg="black", fg="white")
        self.score_label.pack(side=tk.RIGHT)
        
        self.question_label = tk.Label(self.root, font=("Arial", 30), bg="black", fg="white")
        self.question_label.pack(pady=50, expand=True)
        
        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=20)
        
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text="", command=lambda idx=i: self.check_answer(idx))
            btn.pack(side=tk.LEFT, padx=10)
            self.option_buttons.append(btn)
        
        self.countdown(3)
        
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
        self.expression, self.answer = self.create_math_expression()
        self.question_label.config(text=self.expression)
        
        options = [self.answer]
        while len(options) < 4:
            option = random.randint(1, 100)  # Adjusted the range to 100
            if option not in options:
                options.append(option)
        random.shuffle(options)
        
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=str(options[i]), state=tk.NORMAL)
            if options[i] == self.answer:
                self.correct_option_idx = i

    def create_math_expression(self):
        while True:
            answer = random.randint(1, 99)
            operators = ['+', '-', '*', '/']
            op1 = random.choice(operators)
            op2 = random.choice(operators)
            
            num1 = random.randint(1, 99)
            num2 = random.randint(1, 99)
            num3 = random.randint(1, 99)
            
            if op1 == '/':
                num2 = random.randint(2, 99)
                num1 = num2 * random.randint(1, 99)  # Ensure the result is an integer
                answer = num1 // num2
            elif op1 == '*':
                if num1 == 1:
                    num1 = random.randint(2, 99)
                elif num2 == 1:
                    num2 = random.randint(2, 99)
            if op2 == '/':
                num3 = random.randint(2, 99)
                num2 = num3 * random.randint(1, 99)  # Ensure the result is an integer
                answer = num2 // num3
            elif op2 == '*':
                if num2 == 1:
                    num2 = random.randint(2, 99)
                elif num3 == 1:
                    num3 = random.randint(2, 99)
            
            expression = f"{num1} {op1} {num2} {op2} {num3}"
            if max(num1, num2, num3) <= 99 and ('*' in expression or '/' in expression):
                try:
                    if eval(expression) == answer:
                        return expression, answer
                except ZeroDivisionError:
                    pass

    def check_answer(self, idx):
        self.total_questions += 1
        if idx == self.correct_option_idx:
            self.correct_count += 1
        else:
            self.wrong_count += 1
        self.update_score()
        self.write_data_to_csv(idx)
        self.generate_question()

    def update_score(self):
        self.score_label.config(text=f"Correct: {self.correct_count}   Wrong: {self.wrong_count}")

    def end_game(self):
        self.question_label.config(text="Game Over")
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        self.write_summary_to_csv()

    def write_data_to_csv(self, user_choice):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.expression, self.answer, user_choice])

    def write_summary_to_csv(self):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Total Questions", "Total Correct", "Total Wrong"])
            writer.writerow([self.total_questions, self.correct_count, self.wrong_count])

if __name__ == "__main__":
    root = tk.Tk()
    username = input("Enter your name: ")
    app = MathTest(root, username)
    root.mainloop()