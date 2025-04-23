import tkinter as tk
from tkinter import ttk
import csv
import time
import threading
from PIL import Image, ImageTk
import os

# Total game time in seconds (3 minutes = 180 seconds)
TOTAL_GAME_TIME = 10*10

# Time to wait before the game starts
COUNTDOWN_TIME = 5

# Path to the folder where the data will be stored
PATH = './data/'

class ImageTest:
    def __init__(self, root, username, callback=None, use_buttons=True):
        # Create a window
        self.root = root
        self.root.title("Image Test")
        self.root.configure(bg="white")  # Changed to white bg
        # Initialize the game variables
        self.username = username
        self.start_time = time.time()
        self.use_buttons = use_buttons  # Flag to control answer input method
        self.running = True  # Flag to track if the application is still running
        
        # Set up closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create a style object
        style = ttk.Style()

        # This will set all ttk.Button widgets to the 'flat' relief style
        style.configure('TButton', font=('Arial', 40), relief='flat', padding=10)  # Increased font size
        
        # Button colors from MathTest
        self.btn_bg = "#E9E9E9"
        self.btn_fg = "black"
        self.btn_active_bg = "#CCCCCC"
        self.btn_selected_bg = "#97C1A9"
        
        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        self.path_to_file = PATH+'imageTest_'+username+'.csv'
        self.disgusted_count = 0
        self.neutral_count = 0
        self.pleased_count = 0
        self.miss_count = 0
        self.total_questions = 0
        self.image_count = 0  # Add this line to keep track of shown images
        self.remaining_time = TOTAL_GAME_TIME
        self.answered = True  # Set to True initially to avoid the automatic miss at the start
        # Create the widgets
        self.top_frame = tk.Frame(self.root, bg="white")  # Changed to white bg
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        # Create the time label on the top left
        self.time_label = tk.Label(self.top_frame, text=f"Time: {self.remaining_time}", anchor='w', bg="white", fg="black", font=("Arial", 18))  # Changed bg to white
        self.time_label.pack(side=tk.LEFT)
        # Create the question label in the middle
        self.label = tk.Label(self.root, bg="white", wraplength=800)  # Changed bg to white
        self.label.pack(pady=50, expand=True)
        # Create the buttons frame at the bottom
        self.buttons_frame = tk.Frame(self.root, bg="white")  # Changed bg to white
        self.buttons_frame.pack(pady=20)
        
        # Create answer buttons (initially hidden)
        self.create_answer_buttons()
        
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

        self.image_list = []  # To store paths of all images
        self.current_image_index = 0

        # Collect all image paths
        for folder in image_folders:
            for filename in os.listdir(folder):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    file_path = os.path.join(folder, filename)
                    self.image_list.append(file_path)
                    
        # Initialize pygame for audio
        try:
            import pygame
            pygame.mixer.init()
        except Exception as e:
            print(f"Error initializing pygame: {e}")

    def create_answer_buttons(self):
        # Remove any existing buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
            
        if self.use_buttons:
            # Create buttons using native tk buttons instead of ttk, matching MathTest style
            self.disturbed_btn = tk.Button(
                self.buttons_frame, 
                text="Disturbed",
                font=("SF Pro Display", 36),
                bg=self.btn_bg,
                fg=self.btn_fg,
                activebackground=self.btn_active_bg,
                activeforeground=self.btn_fg,
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=10,
                width=12,
                command=lambda: self.check_answer("Disturbed")
            )
            self.disturbed_btn.pack(side=tk.LEFT, padx=15)
            
            self.neutral_btn = tk.Button(
                self.buttons_frame, 
                text="Neutral",
                font=("SF Pro Display", 36),
                bg=self.btn_bg,
                fg=self.btn_fg,
                activebackground=self.btn_active_bg,
                activeforeground=self.btn_fg,
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=10,
                width=12,
                command=lambda: self.check_answer("Neutral")
            )
            self.neutral_btn.pack(side=tk.LEFT, padx=15)
            
            self.pleased_btn = tk.Button(
                self.buttons_frame, 
                text="Pleased",
                font=("SF Pro Display", 36),
                bg=self.btn_bg,
                fg=self.btn_fg,
                activebackground=self.btn_active_bg,
                activeforeground=self.btn_fg,
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=10,
                width=12,
                command=lambda: self.check_answer("Pleased")
            )
            self.pleased_btn.pack(side=tk.LEFT, padx=15)
            
    def load_image(self, image_path):
        image = Image.open(image_path)
        # Resize the image to make it bigger (adjust the size as needed)
        image = image.resize((800, 600), Image.LANCZOS)  # Increased size
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to avoid garbage 

    # Start the game after the countdown
    def countdown(self, count):
        # Initialize buttons but don't show the frame until countdown is complete
        self.create_answer_buttons()
        self.buttons_frame.pack_forget()  # Hide buttons during countdown
        
        if count > 0:
            instructions = "Image Test:\n\nA series of images will be displayed.\n\n"
            if self.use_buttons:
                instructions += "Record your reaction by clicking the buttons below or pressing:\n1 (disgusted), 2 (neutral), 3 (pleased) on your keyboard.\n\n"
            else:
                instructions += "Record your reaction to the images by pressing:\n1 (disgusted), 2 (neutral), 3 (pleased) on your keyboard.\n\n"
            instructions += "Starting in: "
            self.label.config(text=f"{instructions}{count}", fg="black", font=("Arial", 24), bg="white")  # Increased font size & white bg
            self.root.after(1000, self.countdown, count-1)
        else:
            self.label.config(text="", fg="black", bg="white")  # Changed bg to white
            self.start_game()  # Start the game after countdown

    # Start the game
    def start_game(self):
        self.write_header_to_csv()
        self.update_timer()
        self.start_question_timer_thread()
        # self.play_music_thread()

        # Load and display the first image
        self.load_image(self.image_list[self.current_image_index])
        self.current_image_index += 1  # Increment the image count

        # Bind keys to their respective answers
        self.root.bind('1', lambda event: self.check_answer("Disturbed"))
        self.root.bind('2', lambda event: self.check_answer("Neutral"))
        self.root.bind('3', lambda event: self.check_answer("Pleased"))
        
        # Show buttons after countdown is complete
        if self.use_buttons:
            self.buttons_frame.pack(pady=20)

    def check_answer(self, user_choice):
        if not self.running:
            return
            
        # Highlight the selected button
        if self.use_buttons:
            if user_choice == "Disturbed":
                self.disturbed_btn.config(bg=self.btn_selected_bg)
                self.neutral_btn.config(bg=self.btn_bg)
                self.pleased_btn.config(bg=self.btn_bg)
            elif user_choice == "Neutral":
                self.disturbed_btn.config(bg=self.btn_bg)
                self.neutral_btn.config(bg=self.btn_selected_bg)
                self.pleased_btn.config(bg=self.btn_bg)
            elif user_choice == "Pleased":
                self.disturbed_btn.config(bg=self.btn_bg)
                self.neutral_btn.config(bg=self.btn_bg)
                self.pleased_btn.config(bg=self.btn_selected_bg)
            
            # Force update to show selection
            self.root.update()
            # Short delay to show the highlight
            self.root.after(200)
        
        # Your existing answer checking logic here
        self.write_data_to_csv(user_choice)
        
        # Reset button colors after a short delay
        if self.use_buttons:
            self.disturbed_btn.config(bg=self.btn_bg)
            self.neutral_btn.config(bg=self.btn_bg)
            self.pleased_btn.config(bg=self.btn_bg)
        
        if self.image_count < len(self.image_list):
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.load_image(self.image_list[self.current_image_index])
            self.image_count += 1
        else:
            self.end_game()  # End the game if all images have been shown

    def start_question_timer_thread(self):
        self.question_timer_thread = threading.Thread(target=self.question_timer_logic)
        self.question_timer_thread.daemon = True
        self.question_timer_thread.start()

    def question_timer_logic(self):
        # Implement your question timer logic here
        pass

    # # Thread to play music when the game starts
    # def play_music(self):
    #     if not self.running:
    #         return
            
    #     try:
    #         import pygame
    #         pygame.mixer.music.load("clock.mp3")
    #         pygame.mixer.music.play(6)
    #     except Exception as e:
    #         print(f"Error playing music: {e}")

    # def play_music_thread(self):
    #     self.play_music_thread = threading.Thread(target=self.play_music)
    #     self.play_music_thread.daemon = True
    #     self.play_music_thread.start()

    # Update the timer
    def update_timer(self):
        if not self.running:
            return
            
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"Time: {self.remaining_time}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    # Game over
    def end_game(self):
        if not self.running:
            return
            
        self.label.config(text="Test Over", fg="black", font=("Arial", 24))
        # Disable buttons
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)
        self.write_summary_to_csv()
        
        # Stop the music
        self.stop_music()
            
        # Set running to false and close after a delay
        self.running = False
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

    def on_closing(self):
        """Handle the window closing event"""
        self.running = False
        self.stop_music()
        # Write summary before closing if any images were shown
        if self.image_count > 0:
            try:
                self.write_summary_to_csv()
            except Exception as e:
                print(f"Error writing summary: {e}")
        
        # Call callback if provided
        if self.callback:
            self.callback()
            
        # Destroy the window
        self.root.destroy()
        
    def stop_music(self):
        """Stop the music playback"""
        try:
            import pygame
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping music: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.configure(bg="white")  # Set background to white
        
        # Center the window
        window_width = 1800  # Set to your desired width
        window_height = 1000  # Set to your desired height
            
        # Fix the window size
        root.minsize(window_width, window_height)  # Set to your desired width and height
        root.maxsize(2560, 1600)  # Set to your desired width and height

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Set use_buttons=True to enable button-based answer selection
        app = ImageTest(root, username="testUserImage", use_buttons=True)
        root.mainloop()
    except Exception as e:
        print(f"Error in Image Test: {e}")
        import traceback
        traceback.print_exc()
        # Try to clean up if possible
        try:
            import pygame
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except:
            pass