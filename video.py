import tkinter as tk
from tkinter import ttk
import time
import imageio
from PIL import Image, ImageTk
import csv

# Total game time in seconds (3 minutes = 180 seconds)
TOTAL_GAME_TIME = 180

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
        self.after_ids = []  # Store after IDs for proper cleanup

        # UI Elements
        self.top_frame = tk.Frame(self.root, bg="white")
        self.top_frame.pack(fill=tk.BOTH, padx=10, pady=0)

        self.label = tk.Label(self.root, bg="white")  # Use for displaying video
        self.label.pack(pady=50, expand=True)

        self.buttons_frame = tk.Frame(self.root, bg="white")
        self.buttons_frame.pack(pady=5)

        # Start the game immediately without countdown
        self.start_game()

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

            # Schedule the next frame update and store the after ID
            after_id = self.root.after(30, self.update_frame)  # Updates every 30 ms (approx. 30 FPS)
            self.after_ids.append(after_id)
        except Exception as e:
            print(f"Video playback finished or error: {e}")
            self.show_slider()  # Show slider when video finishes

    def start_game(self):
        """ Start the game immediately """
        self.load_video(self.video_path)  # Load and play the video
        try:
            self.write_header_to_csv()
            self.update_timer()
            self.start_question_timer_thread()
            self.play_music_thread()
        except AttributeError:
            # These methods might not be implemented or have issues
            pass

    def write_header_to_csv(self):
        """ Write header to the CSV file """
        try:
            with open(self.path_to_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Relative Time", "Image", "User Choice", "Result", self.username])
        except AttributeError:
            # path_to_file might not be defined
            pass

    def show_slider(self):
        """ Show slider after the video ends """
        self.label.config(image='', text="Select a value between 1 and 10:", fg="black", font=("Open Sans", 40))
        
        # Remove video-related widgets
        self.video_reader = None

        # Create slider
        slider = tk.Scale(self.root, from_=1, to=10, orient="horizontal", length=500)
        slider.pack(pady=20)

        # Button to get slider value (optional)
        def show_value():
            print(f"Slider value: {slider.get()}")

        submit_button = tk.Button(self.root, text="Submit", command=show_value)
        submit_button.pack(pady=10)
    
    def __del__(self):
        """Clean up after IDs when object is destroyed"""
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except:
                pass

# Main
if __name__ == "__main__":
    root = tk.Tk()

    # Get user's window width and height
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    root.geometry(f"{window_width}x{window_height}")

    app = VideoTest(root, username="testUserVideo")
    root.mainloop()
