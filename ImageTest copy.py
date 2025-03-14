import tkinter as tk
from tkinter import ttk
import csv
import time
import threading
from PIL import Image, ImageTk
import os
from PIL import Image, ImageTk  # Import Pillow for image resizing

# Total game time in seconds (3 minutes = 180 seconds)
TOTAL_GAME_TIME = 180

# Time to wait before the game starts
COUNTDOWN_TIME = 5

# Path to the folder where the data will be stored
PATH = './data/'

class ImageTest:
    def __init__(self, root, username, callback=None):
        # Create a window
        self.root = root
        self.root.title("Image Test")
        self.root.configure(bg="white")
        # Initialize the game variables
        self.username = username
        self.start_time = time.time()
        # Create a style object
        style = ttk.Style()

        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        self.path_to_file = PATH+'imageTest_'+username+'.csv'
        self.disgusted_count = 0
        self.neutral_count = 0
        self.pleased_count = 0
        self.total_questions = 0
        self.image_count = 0  # Add this line to keep track of shown images
        self.remaining_time = TOTAL_GAME_TIME
        self.answered = True  # Set to True initially to avoid the automatic miss at the start
        # Create the widgets
        self.top_frame = tk.Frame(self.root, bg="white")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=0)
        # Create the time label on the top left
        self.time_label = tk.Label(self.top_frame, font=("Open Sans", 24), text=f"Time: {self.remaining_time}", anchor='w', bg="white", fg="black")
        self.time_label.pack(side=tk.LEFT)
        # Create the question label in the middle
        self.label = tk.Label(self.root, bg="white", wraplength=800)  # Increased wraplength for instructions
        self.label.pack(pady=50, expand=True)
        # Create the buttons frame at the bottom
        self.buttons_frame = tk.Frame(self.root, bg="white")
        self.buttons_frame.pack(pady=5)
        # Start the countdown before the game begins
        self.countdown(COUNTDOWN_TIME)
        self.callback = callback 
        self.question_timer_thread = None  # Add this line to create a placeholder for the thread
        
        # Initialize image list (you need to populate this with your image paths)
        
        image_folders = [
            "images/osfstorage-archive/Checking",
            "images/osfstorage-archive/Symmetry",
            "images/osfstorage-archive/Washing",
        ]

        self.option_buttons = ["a", "b", "c"]
        self.images = []  # Initialize the list to store image references

        self.image_list = []  # To store paths of all images
        self.current_image_index = 0

        # Collect all image paths
        # Collect all image paths
        for folder in image_folders:
            for filename in os.listdir(folder):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    file_path = os.path.join(folder, filename)
                    self.image_list.append(file_path)

        # Create a style object
        style = ttk.Style()

        # Configure the font for TButton style
        style.configure('TButton', font=('Open Sans', 35))  # Increase 20 to your desired font size


        self.buttons_frame = tk.Frame(self.root, bg="white")
        self.buttons_frame.pack(pady=0)
        
        for i, emoji in enumerate(os.listdir('emojis/')):
            image_path = os.path.join('emojis', emoji)
            
            # Open the image using Pillow
            original_image = Image.open(image_path)
            
            # Resize the image to 30x30 pixels
            resized_image = original_image.resize((130, 130), Image.Resampling.LANCZOS)
            
            # Convert the resized image to a Tkinter-compatible PhotoImage
            image = ImageTk.PhotoImage(resized_image)
            
            # Keep a reference to avoid garbage collection
            self.images.append(image)

            # Create a label with the resized image
            label = tk.Label(self.buttons_frame, image=image, bg="white", bd=0)
            label.pack(side=tk.LEFT, padx=100)
            
            # Bind click events to the label
            label.bind('<Button-1>', lambda event, idx=i: self.check_answer(idx))



    def load_image(self, image_path):
        image = Image.open(image_path)
        # Resize the image to make it bigger (adjust the size as needed)
        image = image.resize((800, 600), Image.LANCZOS)  # Increased size
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to avoid garbage 

    # Start the game after the countdown
    def countdown(self, count):
        if count > 0:
            self.label.config(text=f"{count}", fg="black", font=("Open Sans", 160))
            self.root.after(1000, self.countdown, count-1)
        else:
            self.label.config(text="", fg="black", font=("Open Sans", 40))  # Clear the countdown number
            self.start_game()  # Start the game after countdown

    # Start the game
    def start_game(self):
        self.write_header_to_csv()
        self.update_timer()
        self.start_question_timer_thread()
        self.play_music_thread()

        # Load and display the first image
        self.load_image(self.image_list[self.current_image_index])
        self.current_image_index += 1  # Increment the image count

    def check_answer(self, user_choice):
        # Your existing answer checking logic here
        self.write_data_to_csv(user_choice)
        
        if(self.image_count < len(self.image_list)):
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.load_image(self.image_list[self.current_image_index])
            self.image_count += 1
        else:
            self.end_game()  # End the game if all images have been sho

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

    #get user's window width and height
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    root.geometry(f"{window_width}x{window_height}")

    app = ImageTest(root, username="testUserImage")
    root.mainloop()