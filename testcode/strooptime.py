import tkinter as tk
import random

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
TOTAL_GAME_TIME = 10

# Question frequency (number of questions per second). Value should be between 0 and 1.
QUESTION_FREQUENCY = 1  # 1 question every second

class StroopTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Stroop Test")
        self.root.configure(bg="black")
        
        self.correct_count = 0
        self.wrong_count = 0
        self.miss_count = 0
        self.previous_display_color = None
        self.previous_word = None
        self.remaining_time = TOTAL_GAME_TIME
        self.answered = True  # Set to True initially to avoid the automatic miss at the start
        
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(self.top_frame, text="Correct: 0   Wrong: 0   Miss: 0", anchor='e', bg="black", fg="white")
        self.score_label.pack(side=tk.RIGHT)
        
        self.label = tk.Label(self.root, font=("Arial", 50), bg="black")
        self.label.pack(pady=100, expand=True)
        
        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=20)
        
        for color_name in colors:
            btn = tk.Button(self.buttons_frame, text=color_name, bg=colors[color_name], command=lambda cn=color_name: self.check_answer(cn))
            btn.pack(side=tk.LEFT, padx=10)
        
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
            self.miss_count += 1
            self.update_score()
            self.label.config(text="", fg="black")  # Hide the question
            self.root.update()
        self.answered = False
        self.generate_question()
        self.root.after(int(1000 / QUESTION_FREQUENCY), self.question_timer)  # Adjusted for questions per second

    def end_game(self):
        self.label.config(text="Game Over", fg="white")
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)

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
            if colors[chosen_color] == self.label.cget("fg"):
                self.correct_count += 1
            else:
                self.wrong_count += 1
            self.update_score()
            self.answered = True
            self.label.config(text="", fg="black")  # Hide the question after answering
            self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = StroopTest(root)
    root.mainloop()
