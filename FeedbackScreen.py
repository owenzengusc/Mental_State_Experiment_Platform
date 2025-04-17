# FeedbackScreen.py
import tkinter as tk
import csv

PATH = './data/'

class FeedbackScreen:
    def __init__(self, root, username, callback=None):
        self.root = root
        self.username = username
        self.path_to_file = PATH + 'feedback.csv'
        # Define missing attributes
        self.bg_color = "white"
        self.font_large = ("Open Sans", 48)
        
        #get user's window width and height
        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()

        root.geometry(f"{window_width}x{window_height}")

        self.root.title("Feedback Screen")
        self.root.configure(bg=self.bg_color)
        
        # Title
        self.title_label = tk.Label(root, text="Feedback Screen", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
        self.title_label.pack(pady=70, anchor=tk.CENTER)

        self.label = tk.Label(root, text="Please rate the experiment from 1-5 and provide your feedback:", font=("Opens Sans", 40))
        self.label.pack(pady=10)
        
        self.rating_var = tk.IntVar()
        for i in range(1, 6):
            rb = tk.Radiobutton(root, text=str(i), variable=self.rating_var, value=i, font=("Open Sans", 30))
            rb.pack(side=tk.LEFT, padx=5)
        
        self.feedback_entry = tk.Text(root, height=5, width=40)
        self.feedback_entry.pack(pady=10)
        
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_feedback, font=("Open Sans", 30))
        self.submit_button.pack(pady=10)
        
        self.callback = callback

    def submit_feedback(self):
        rating = self.rating_var.get()
        feedback = self.feedback_entry.get("1.0", tk.END).strip()
        
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, rating, feedback])
        
        if self.callback:
            self.callback()
        self.root.destroy()  # Close the feedback screen after submitting

if __name__ == "__main__":
    root = tk.Tk()
    username = input("Enter your name: ")
    app = FeedbackScreen(root, username)
    root.mainloop()
