import tkinter as tk
from tkinter import ttk
import time
import imageio
from PIL import Image, ImageTk
import csv

# Total game time in seconds (3 minutes = 180 seconds)
TOTAL_GAME_TIME = 180

# Time to wait before the game starts
COUNTDOWN_TIME = 5

# Path to the folder where the data will be stored
PATH = './data/'

class VideoTest:
    def __init__(self, root, username, callback=None):
        # Create a window
        self.root = root
        self.root.title("Video Test")
        self.root.configure(bg="white")

        # Initialize the variables
        self.username = username
        self.start_time = time.time()
        self.callback = callback
        self.video_reader = None  # Placeholder for video reader
        self.video_path = "videos/1.mp4"  # Your video path

        # UI Elements
        self.top_frame = tk.Frame(self.root, bg="white")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=0)

        self.label = tk.Label(self.root, bg="white")  # Use for displaying video
        self.label.pack(pady=50, expand=True)

        self.buttons_frame = tk.Frame(self.root, bg="white")
        self.buttons_frame.pack(pady=5)

        # Start countdown
        self.countdown(COUNTDOWN_TIME)  # Adjust countdown time if needed

    def load_video(self, video_path):
        """ Load and play a video in the Tkinter window """
        self.video_reader = imageio.get_reader(video_path)  # Open video file
        self.update_frame()  # Start displaying video frames

    def update_frame(self):
        """ Continuously update the video frame in the Tkinter window """
        try:
            frame = self.video_reader.get_next_data()  # Get the next frame
            image = Image.fromarray(frame)  # Convert to PIL Image

            # Resize the image (adjust the size as needed)
            resized_image = image.resize((1280, 720), Image.LANCZOS)  # Resize to 1024x768
            photo = ImageTk.PhotoImage(resized_image)  # Convert to Tkinter-compatible format

            self.label.config(image=photo)  # Update the label to show the new frame
            self.label.image = photo  # Keep a reference to avoid garbage collection

            # Schedule the next frame update
            self.root.after(30, self.update_frame)  # Updates every 30 ms (approx. 30 FPS)
        except Exception as e:
            print(f"Video playback finished or error: {e}")
            self.show_slider()  # Show slider when video finishes

    def countdown(self, count):
        """ Countdown function before the game starts """
        if count > 0:
            self.label.config(text=f"{count}", fg="black", font=("Open Sans", 160))
            self.root.after(1000, self.countdown, count-1)
        else:
            self.label.config(text="", fg="black", font=("Open Sans", 40))  # Clear the countdown
            self.start_game()  # Start the game after countdown

    def start_game(self):
        """ Start the game after countdown """
        self.load_video(self.video_path)  # Load and play the video
        self.write_header_to_csv()
        self.update_timer()
        self.start_question_timer_thread()
        self.play_music_thread()

    def write_header_to_csv(self):
        """ Write header to the CSV file """
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Relative Time", "Image", "User Choice", "Result", self.username])

    def show_slider(self):
        """ Show slider after the video ends """
        # Update text with 50px font size and position the second part underneath
        self.label.config(image='', 
                        text="Please rate your arousal level:\nUnhappy(-10), Neutral(0), Happy(10)", 
                        fg="black", font=("Open Sans", 50))  # Set font size to 50px

        # Remove video-related widgets
        self.video_reader = None

        # Create slider - adjusting the length to 70% of the window width
        slider_length = int(self.root.winfo_width() * 0.7)  # 70% of the window width
        slider = tk.Scale(self.root, from_=-10, to=10, orient="horizontal", length=slider_length, sliderlength=20, tickinterval=5, showvalue=1)
        slider.pack(pady=20)  # Set the gap between the text and the slider to 20px (one-third of 60px)

        # Button to get slider value (optional)
        def show_value():
            print(f"Slider value: {slider.get()}")

        submit_button = tk.Button(self.root, text="Submit", command=show_value)
        submit_button.pack(pady=10)


# Main
if __name__ == "__main__":
    root = tk.Tk()

    # Get user's window width and height
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    root.geometry(f"{window_width}x{window_height}")

    app = VideoTest(root, username="testUserVideo")
    root.mainloop()
