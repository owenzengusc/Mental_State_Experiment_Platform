import tkinter as tk
from tkinter import ttk
import csv
import time
import threading
from PIL import Image, ImageTk

# Total game time in seconds (3 minutes = 180 seconds)
TOTAL_GAME_TIME = 10*10

# Time to wait before the game starts
COUNTDOWN_TIME = 5

# Path to the folder where the data will be stored
PATH = './data/'

class ImageTest:
    def __init__(self, root, username, callback=None):
        # Create a window
        self.root = root
        self.root.title("Image Test")
        self.root.configure(bg="black")
        # Initialize the game variables
        self.username = username
        self.start_time = time.time()
        # Create a style object
        style = ttk.Style()

        # This will set all ttk.Button widgets to the 'flat' relief style
        style.configure('TButton',font=('Arial', 31), relief='flat', padding=6)
        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        self.path_to_file = PATH+'imageTest_'+username+'.csv'
        self.correct_count = 0
        self.wrong_count = 0
        self.miss_count = 0
        self.total_questions = 0
        self.remaining_time = TOTAL_GAME_TIME
        self.answered = True  # Set to True initially to avoid the automatic miss at the start
        # Create the widgets
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        # Create the time label on the top left
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        # Create the question label in the middle
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(pady=100, expand=True)
        # Create the buttons frame at the bottom
        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=20)
        # Start the countdown before the game begins
        self.countdown(COUNTDOWN_TIME)
        self.callback = callback 
        self.question_timer_thread = None  # Add this line to create a placeholder for the thread
        
        # Initialize image list (you need to populate this with your image paths)
        self.image_list = ["images/flower1.jpeg", "images/flower2.jpeg", "images/flower3.jpeg", 
                           "images/flower4.jpeg", "images/flower5.jpeg", "images/flower6.jpeg",
                           "images/flower7.jpeg", "images/flower8.jpeg", "images/flower9.jpeg",
                           "images/flower10.jpeg"]
        self.current_image_index = 0

    def load_image(self, image_path):
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to avoid garbage collection

    # Start the game after the countdown
    def countdown(self, count):
        if count > 0:
            self.label.config(text=str(count), fg="white")
            self.root.after(1000, self.countdown, count-1)
        else:
            self.label.config(text="", fg="black")  # Clear the countdown number
            self.start_game()  # Start the game after countdown

    # Start the game
    def start_game(self):
        self.write_header_to_csv()
        self.update_timer()
        self.start_question_timer_thread()
        self.play_music_thread()

        # Load and display the first image
        self.load_image(self.image_list[self.current_image_index])

        # Bind keys to their respective answers
        self.root.bind('1', lambda event: self.check_answer("Disturbed"))
        self.root.bind('2', lambda event: self.check_answer("Neutral"))
        self.root.bind('3', lambda event: self.check_answer("Pleased"))

    def check_answer(self, user_choice):
        # Your existing answer checking logic here
        self.write_data_to_csv(user_choice)
        
        # Move to the next image
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.load_image(self.image_list[self.current_image_index])

    def start_question_timer_thread(self):
        self.question_timer_thread = threading.Thread(target=self.question_timer_logic)
        self.question_timer_thread.daemon = True
        self.question_timer_thread.start()

    def question_timer_logic(self):
        # Implement your question timer logic here
        pass

    # Thread to play music when the game starts
    def play_music(self):
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("clock.mp3")
        pygame.mixer.music.play(6)

    def play_music_thread(self):
        self.play_music_thread = threading.Thread(target=self.play_music)
        self.play_music_thread.daemon = True
        self.play_music_thread.start()

    # Update the timer
    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"Time: {self.remaining_time}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    # Game over
    def end_game(self):
        self.label.config(text="Test Over", fg="white")
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        self.write_summary_to_csv()
        # stop the music
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.stop()
        self.root.after(2000, self.root.destroy) 
        if self.callback:
            self.callback()
        
    # Write the header to the CSV file      
    def write_header_to_csv(self):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Relative Time", "Image", "User Choice", "Result", self.username])
    
    # Write the data to the CSV file
    def write_data_to_csv(self, user_choice):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)  # Convert to milliseconds
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, self.image_list[self.current_image_index], user_choice, "RECORDED"])

    # Write the summary to the CSV file's first two rows and after the last row
    def write_summary_to_csv(self):
        # Read the entire CSV file into memory
        with open(self.path_to_file, 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            # Insert the summary rows at the top
            lines.insert(0, ["Start Time", "Total Questions", "Total Game Time"])
            lines.insert(1, [self.start_time_header, self.total_questions, TOTAL_GAME_TIME])
    
        # Write the modified content back to the CSV file
        with open(self.path_to_file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            writer.writerow(["Start Time", "Total Questions", "Total Game Time"])
            writer.writerow([self.start_time_header, self.total_questions, TOTAL_GAME_TIME])

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

    app = ImageTest(root, username="testUserImage")
    root.mainloop()