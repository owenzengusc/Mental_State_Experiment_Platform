import tkinter as tk

class InstructionScreen:
    def __init__(self, root, test_type, callback=None):
        self.root = root
        self.callback = callback
        
        # Styling
        self.bg_color = "white"  # Dark background color
        self.fg_color = "#3a3d42"  # Light foreground color
        self.btn_color = "#97C1A9"  # Button color
        self.font_large = ("Open Sans", 120)
        self.font_medium = ("Open Sans", 45)
        
        
        # Instructions based on test type
        if test_type == "MathTest":
        # Title
            self.root.title("Mental Arithmetic Task Instructions")
            self.root.configure(bg=self.bg_color)
            self.title_label = tk.Label(root, text="Mental Arithmetic Task \n" + "Instructions", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
            self.title_label.pack(pady=70, anchor=tk.CENTER)
            description_text = (
                "You will be presented with a series of math expressions.\n"
                "Your task is to solve them as quickly as possible.\n"
                "RIGHT Click on the correct answer from the given options.\n"
                "The test will last for 180 seconds."
            )
            example_text = "For example, if the expression is '5 + 3', you should select '8'."
        elif test_type == "StroopTest":
            self.root.title("Stroop Test")
            self.root.configure(bg=self.bg_color)
            self.title_label = tk.Label(root, text="Stroop Test Instructions", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
            self.title_label.pack(pady=70, anchor=tk.CENTER)
            description_text = (
                "From this test, words will be displayed in various colors.\n"
                "Your task is to select the COLOR of the word, not the word itself.\n"
                "The colors correspond to the keys on the keyboard.\n"
                "Key 'G' is Green, 'R' is Red, 'Y' is Yellow, 'B' is blue \n"
                "Press the correct key as soon as possible."
            )
            example_text = "For example, for the word "
        elif test_type == "VideoFeedback":
            self.title_label = tk.Label(root, text=test_type+" Instructions", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
            self.title_label.pack(pady=70, anchor=tk.CENTER)
            description_text = (
                "You will be presented with a series of videos.\n"
                "After each video, you will be asked to rate your happiness level.\n"
                "Use the scale provided to indicate how the video made you feel.\n"
                "Please be as honest and accurate as possible in your ratings."
            )
            example_text = ""
        elif test_type == "ColdPressorTest":
            self.root.title("Cold Pressor Test")
            self.root.configure(bg=self.bg_color)
            self.title_label = tk.Label(root, text="Cold Pressor Test \n"+"Instructions", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
            self.title_label.pack(pady=70, anchor=tk.CENTER)
            description_text = (
                "For this task you will be asked to put your right hand in provided water.\n"
                "for 3 minutes followed by a relaxation period. Please follow the .\n"
                "next instructions."
            )
            example_text = ""

        # TODO 4: Add instructions for ImageTest
        elif test_type == "ImageTest":
            self.root.title("Visual Stimulation Test")
            self.root.configure(bg=self.bg_color)
            self.title_label = tk.Label(root, text="Visual Stimulation Test \n" + " Instructions", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
            self.title_label.pack(pady=70, anchor=tk.CENTER)
            description_text = (
                "You will be presented with a series of images.\n"
                "After each image, you will be asked to express your reaction.\n"
                "Use the options: Disturbed, Neutral, and Pleased.\n"
                "Please be as honest and accurate as possible in your ratings."
            )
            example_text = ""
        
        self.description_label = tk.Label(root, text=description_text, font=self.font_medium, bg=self.bg_color, fg=self.fg_color, justify=tk.CENTER)
        self.description_label.pack(pady=20, anchor=tk.CENTER)
        
        if test_type == "StroopTest":

            self.title_label = tk.Label(root, text="Stroop Test Instructions", font=self.font_large, bg=self.bg_color, fg="#9ba8ee")
            self.title_label.pack(pady=70, anchor=tk.CENTER)

            self.example_frame = tk.Frame(root, bg=self.bg_color)
            self.example_frame.pack(pady=5, anchor=tk.CENTER)
            
            self.example_label = tk.Label(self.example_frame, text=example_text, font=self.font_medium, bg=self.bg_color, fg=self.fg_color, justify=tk.CENTER)
            self.example_label.pack(side=tk.LEFT)
            
            self.example_word_label = tk.Label(self.example_frame, text="RED", font=self.font_medium, bg=self.bg_color, fg="blue")
            self.example_word_label.pack(side=tk.LEFT)
            
            self.example_continue_label = tk.Label(self.example_frame, text=" you should press 'R' on the keyboard.", font=self.font_medium, bg=self.bg_color, fg=self.fg_color, justify=tk.CENTER)
            self.example_continue_label.pack(side=tk.LEFT)
        
        # Start button
        self.start_button = tk.Button(root, text="Start", font=self.font_medium, bg=self.btn_color, fg="Black", command=self.start_test)
        self.start_button.pack(pady=20, anchor=tk.CENTER)

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