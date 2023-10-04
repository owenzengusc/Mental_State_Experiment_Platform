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

class StroopTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Stroop Test")
        self.root.configure(bg="black")
        
        self.correct_count = 0
        self.wrong_count = 0
        self.previous_display_color = None
        self.previous_word = None
        
        self.score_label = tk.Label(self.root, text="Correct: 0   Wrong: 0", anchor='e', bg="black", fg="white")
        self.score_label.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.label = tk.Label(self.root, font=("Arial", 50), bg="black")
        self.label.pack(pady=100)
        
        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=20)
        
        for color_name in colors:
            btn = tk.Button(self.buttons_frame, text=color_name, bg=colors[color_name], command=lambda cn=color_name: self.check_answer(cn))
            btn.pack(side=tk.LEFT, padx=10)
        
        self.generate_question()

    def update_score(self):
        self.score_label.config(text=f"Correct: {self.correct_count}   Wrong: {self.wrong_count}")

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
        if colors[chosen_color] == self.label.cget("fg"):
            self.correct_count += 1
        else:
            self.wrong_count += 1
        self.update_score()
        self.generate_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = StroopTest(root)
    root.mainloop()
