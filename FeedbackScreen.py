# FeedbackScreen.py
import tkinter as tk
from tkinter import ttk
import csv
from window_utils import set_responsive_geometry

PATH = './data/'

class FeedbackScreen:
    def __init__(self, root, username, callback=None):
        self.root = root
        self.username = username
        self.path_to_file = PATH + 'feedback.csv'
        
        # Define colors and fonts for consistent design
        self.bg_color = "white"
        self.accent_color = "#4A6FFF"  # Modern blue accent
        self.text_color = "#333333"    # Dark gray for text
        self.font_title = ("SF Pro Display", 42, "bold")
        self.font_text = ("SF Pro Display", 32)
        self.font_button = ("SF Pro Display", 28)
        
        # Configure the window
        set_responsive_geometry(root, "main")
        self.root.title("Feedback")
        self.root.configure(bg=self.bg_color)
        
        # Main container frame
        self.main_frame = tk.Frame(root, bg=self.bg_color, padx=50, pady=50)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with accent color
        self.title_label = tk.Label(
            self.main_frame, 
            text="Your Feedback", 
            font=self.font_title, 
            bg=self.bg_color, 
            fg=self.accent_color
        )
        self.title_label.pack(pady=(0, 40), anchor=tk.CENTER)

        # Instructions with proper spacing
        self.label = tk.Label(
            self.main_frame, 
            text="How would you rate your experience?", 
            font=self.font_text, 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.label.pack(pady=(0, 30), anchor=tk.W)
        
        # Rating frame with modern styling
        self.rating_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.rating_frame.pack(fill=tk.X, pady=(0, 40))
        
        # Style for the rating buttons
        self.rating_var = tk.IntVar()
        self.rating_buttons = []
        
        # Create 5 rating buttons in a row
        for i in range(1, 6):
            btn_frame = tk.Frame(self.rating_frame, bg=self.bg_color)
            btn_frame.pack(side=tk.LEFT, padx=15, fill=tk.Y)
            
            # Rating button
            rating_btn = tk.Radiobutton(
                btn_frame,
                text=str(i),
                variable=self.rating_var,
                value=i,
                font=self.font_text,
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.bg_color,
                activebackground=self.bg_color,
                indicatoron=0,  # Make it look like a button
                width=3,
                height=1,
                bd=1,
                relief=tk.RAISED,
                command=lambda val=i: self.highlight_rating(val)
            )
            rating_btn.pack(fill=tk.BOTH)
            
            # Rating label
            label_text = ""
            if i == 1:
                label_text = "Poor"
            elif i == 3:
                label_text = "Average"
            elif i == 5:
                label_text = "Excellent"
                
            rating_label = tk.Label(
                btn_frame,
                text=label_text,
                font=("SF Pro Display", 14),
                bg=self.bg_color,
                fg=self.text_color
            )
            rating_label.pack()
            
            self.rating_buttons.append(rating_btn)
        
        # Comments label
        self.comments_label = tk.Label(
            self.main_frame, 
            text="Additional comments:", 
            font=self.font_text, 
            bg=self.bg_color, 
            fg=self.text_color,
            anchor=tk.W
        )
        self.comments_label.pack(fill=tk.X, pady=(0, 10), anchor=tk.W)
        
        # Text box with consistent styling
        self.feedback_entry = tk.Text(
            self.main_frame, 
            height=5, 
            width=40, 
            font=("SF Pro Display", 18),
            bg="#F8F8F8",  # Very light gray
            relief=tk.FLAT,
            padx=10,
            pady=10,
            bd=1,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground="#E0E0E0"  # Light gray border
        )
        self.feedback_entry.pack(fill=tk.X, pady=(0, 40))
        
        # Submit button with accent color
        self.submit_button = tk.Button(
            self.main_frame, 
            text="Submit Feedback", 
            command=self.submit_feedback, 
            font=self.font_button,
            bg=self.accent_color,
            fg="white",
            activebackground="#3D5FD9",  # Darker blue when clicked
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2"  # Hand cursor on hover
        )
        self.submit_button.pack(pady=(0, 20))
        
        self.callback = callback

    def highlight_rating(self, value):
        """Highlight the selected rating button"""
        for i, btn in enumerate(self.rating_buttons):
            if i+1 == value:
                btn.config(bg=self.accent_color, fg="white", activebackground=self.accent_color)
            else:
                btn.config(bg=self.bg_color, fg=self.text_color, activebackground=self.bg_color)

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
    # Apply responsive sizing for stand-alone execution
    from window_utils import set_responsive_geometry
    set_responsive_geometry(root, "main")
    
    username = input("Enter your name: ")
    app = FeedbackScreen(root, username)
    root.mainloop()
