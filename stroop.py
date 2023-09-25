import tkinter as tk
import random
import csv
import time
import os

# Define the colors and their names
colors = {
    "Red": "red",
    "Blue": "blue",
    "Green": "green",
    "Yellow": "yellow",
    "Purple": "purple",
    "Orange": "orange"
}

# Total game time in seconds (3 minutes = 180 seconds)
TOTAL_GAME_TIME = 5

# Initial question frequency (number of questions per second). Value should be between 0 and 1.
QUESTION_FREQUENCY = 1  # 1 question every second

# Rate at which the question frequency increases after each question
INCREASE_RATE = 0.1

# Maximum question frequency the game can reach
MAX_QUESTION_FREQUENCY = 2  # 2 questions every second

COUNTDOWN_TIME = 5

PATH = './data/'
class StroopTest:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Stroop Test")
        self.root.configure(bg="black")
        
        self.username = username
        self.start_time = time.time()
        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        self.path_to_file = PATH+'stroopTest_'+username+'.csv'
        self.correct_count = 0
        self.wrong_count = 0
        self.miss_count = 0
        self.total_questions = 0
        self.previous_display_color = None
        self.previous_word = None
        self.remaining_time = TOTAL_GAME_TIME
        self.answered = True  # Set to True initially to avoid the automatic miss at the start
        self.current_frequency = QUESTION_FREQUENCY
        
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        
        self.speed_label = tk.Label(self.top_frame, text=f"Speed: {self.current_frequency:.2f} Q/s", anchor='center', bg="black", fg="white")
        self.speed_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.score_label = tk.Label(self.top_frame, text="Correct: 0   Wrong: 0   Miss: 0", anchor='e', bg="black", fg="white")
        self.score_label.pack(side=tk.RIGHT)
        
        self.label = tk.Label(self.root, font=("Arial", 50), bg="black")
        self.label.pack(pady=100, expand=True)
        
        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=20)
        
        for color_name in colors:
            btn = tk.Button(self.buttons_frame, text=color_name, bg=colors[color_name], command=lambda cn=color_name: self.check_answer(cn))
            btn.pack(side=tk.LEFT, padx=10)
            
        # Start the countdown before the game begins
        self.countdown(COUNTDOWN_TIME) 
        
    def countdown(self, count):
        if count > 0:
            self.label.config(text=str(count), fg="white")
            self.root.after(1000, self.countdown, count-1)
        else:
            self.label.config(text="", fg="black")  # Clear the countdown number
            self.start_game()  # Start the game after countdown


    def start_game(self):
        self.write_header_to_csv()
        self.update_timer()
        self.question_timer()

        

    def update_score(self):
        self.score_label.config(text=f"Correct: {self.correct_count}   Wrong: {self.wrong_count}   Miss: {self.miss_count}")

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"Time: {self.remaining_time}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()
            
    def question_timer(self):
        if self.remaining_time <= 0:
            return
        if not self.answered:
            self.total_questions += 1  
            self.miss_count += 1
            self.update_score()
            self.write_miss_to_csv()  # Record the miss
            self.label.config(text="", fg="black")  # Hide the question
            self.root.update()
        self.answered = False
        self.generate_question()
        self.root.after(int(1000 / self.current_frequency), self.question_timer)  # Adjusted for current frequency
        # Increase the frequency for the next question, but don't exceed the maximum
        self.current_frequency = min(self.current_frequency + INCREASE_RATE, MAX_QUESTION_FREQUENCY)
        self.speed_label.config(text=f"Speed: {self.current_frequency:.2f} Q/s")

    def end_game(self):
        self.label.config(text="Game Over", fg="white")
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        self.write_summary_to_csv()

    def generate_question(self):
        self.word, self.color = random.choice(list(colors.items()))
        display_color = random.choice(list(colors.values()))
        
        # Ensure that two consecutive words don't have the same display color or the same word
        while display_color == self.color or display_color == self.previous_display_color or self.word == self.previous_word:
            self.word, self.color = random.choice(list(colors.items()))
            display_color = random.choice(list(colors.values()))
        
        self.previous_display_color = display_color
        self.previous_word = self.word
        self.label.config(text=self.word, fg=display_color)

    def check_answer(self, chosen_color):
        if not self.answered:
            self.total_questions += 1
            if colors[chosen_color] == self.label.cget("fg"):
                self.correct_count += 1
            else:
                self.wrong_count += 1
            self.update_score()
            self.write_data_to_csv(chosen_color)
            self.answered = True
            self.label.config(text="", fg="black")  # Hide the question after answering
            self.root.update()
            
            
    def write_header_to_csv(self):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Relative Time", "Word", "Color", "User Choice", self.username])

    def write_data_to_csv(self, user_choice):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)  # Convert to milliseconds
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.word, self.color, user_choice])

    def write_miss_to_csv(self):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)  # Convert to milliseconds
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.word, self.color, "MISS"])

    def write_summary_to_csv(self):
        # Read the entire CSV file into memory
        with open(self.path_to_file, 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            # Insert the summary rows at the top
            lines.insert(0, ["Start Time", "Total Questions", "Total Correct", "Total Wrong", "Total Miss", "Total Game Time", "Starting Frequency", "Increase Rate", "End Frequency"])
            lines.insert(1, [self.start_time_header, self.total_questions, self.correct_count, self.wrong_count, self.miss_count, TOTAL_GAME_TIME, QUESTION_FREQUENCY, INCREASE_RATE, self.current_frequency])
    
        # Write the modified content back to the CSV file
        with open(self.path_to_file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            writer.writerow(["Start Time", "Total Questions", "Total Correct", "Total Wrong", "Total Miss", "Total Game Time", "Starting Frequency", "Increase Rate", "End Frequency"])
            writer.writerow([self.start_time_header, self.total_questions, self.correct_count, self.wrong_count, self.miss_count, TOTAL_GAME_TIME, QUESTION_FREQUENCY, INCREASE_RATE, self.current_frequency])

if __name__ == "__main__":
    root = tk.Tk()
    username = input("Enter your name: ")
    app = StroopTest(root, username)
    root.mainloop()