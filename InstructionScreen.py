import tkinter as tk

class InstructionScreen:
    def __init__(self, root, test_type, callback=None):
        self.root = root
        self.callback = callback
        
        # Styling
        self.bg_color = "#CCE2CB"  # Dark background color
        self.fg_color = "Black"  # Light foreground color
        self.btn_color = "#97C1A9"  # Button color
        self.font_large = ("Arial", 55)
        self.font_medium = ("Arial", 45)
        
        self.root.title(test_type+" Instructions")
        self.root.configure(bg=self.bg_color)
        
        # Title
        self.title_label = tk.Label(root, text=test_type+" Instructions", font=self.font_large, bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=20)
        
        # Instructions based on test type
        if test_type == "MathTest":
            description_text = (
                "You will be presented with a series of math expressions.\n"
                "Your task is to solve them as quickly as possible.\n"
                "RIGHT Click on the correct answer from the given options.\n"
                "The test will last for a fixed duration."
            )
            example_text = "For example, if the expression is '5 + 3', you should select '8'."
        elif test_type == "StroopTest":
            description_text = (
                "Words will be displayed in various colors.\n"
                "Your task is to select the COLOR of the word, not the word itself.\n"
                "Click on the correct color on the keyboard as quickly as possible.\n"
                "The test will last for a fixed duration."
            )
            example_text = "For example, for the word "
        elif test_type == "VideoFeedback":
            description_text = (
                "You will be presented with a series of videos.\n"
                "After each video, you will be asked to rate your happiness level.\n"
                "Use the scale provided to indicate how the video made you feel.\n"
                "Please be as honest and accurate as possible in your ratings."
            )
            example_text = ""
        elif test_type == "ColdPressureTest":
            description_text = (
                "You will be asked to put your hand in iced water for a fixed duration.\n"
                "Please follow the instructions provided during the test.\n"
                "The test will last for a fixed duration."
            )
            example_text = ""
        
        self.description_label = tk.Label(root, text=description_text, font=self.font_medium, bg=self.bg_color, fg=self.fg_color, justify=tk.LEFT)
        self.description_label.pack(pady=20)
        
        if test_type == "StroopTest":
            self.example_frame = tk.Frame(root, bg=self.bg_color)
            self.example_frame.pack(pady=5)
            
            self.example_label = tk.Label(self.example_frame, text=example_text, font=self.font_medium, bg=self.bg_color, fg=self.fg_color, justify=tk.LEFT)
            self.example_label.pack(side=tk.LEFT)
            
            self.example_word_label = tk.Label(self.example_frame, text="RED", font=self.font_medium, bg=self.bg_color, fg="blue")
            self.example_word_label.pack(side=tk.LEFT)
            
            self.example_continue_label = tk.Label(self.example_frame, text=" you should select 'Blue'.", font=self.font_medium, bg=self.bg_color, fg=self.fg_color, justify=tk.LEFT)
            self.example_continue_label.pack(side=tk.LEFT)
        
        # Start button
        self.start_button = tk.Button(root, text="Start", font=self.font_medium, bg=self.btn_color, fg="Black", command=self.start_test)
        self.start_button.pack(pady=20)

    def start_test(self):
        if self.callback:
            self.callback()
        try:
            self.root.destroy()
        except tk.TclError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    test_type = input("Enter test type (MathTest/StroopTest/VideoFeedback): ")
    app = InstructionScreen(root, test_type)
    root.mainloop()
