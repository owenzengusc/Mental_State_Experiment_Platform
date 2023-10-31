import tkinter as tk
import os
import pygame
from InstructionScreen import InstructionScreen
from FeedbackScreen import FeedbackScreen
import csv
import time

PATH = './data/'

class VideoFeedbackApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.video_dir = './videos'
        self.video_files = os.listdir(self.video_dir)
        self.current_video_index = 0
        self.path_to_file = PATH + 'videoFeedback_' + username + '.csv'
        self.start_time = time.time()
        self.start_time_header = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(self.start_time))
        self.write_header_to_csv()

        # Initialize UI elements but keep them hidden
        self.init_ui()
        # Show instruction screen
        self.show_instruction_screen()

    def init_ui(self):
        # Create labels and happiness scale here and initially hide them
        self.root.title("Video Feedback")
        self.root.geometry("800x600")  # Set the size of the root window
        # Center the root window on the screen
        self.root.geometry(f"800x600+{(self.root.winfo_screenwidth() - 800) // 2}+{(self.root.winfo_screenheight() - 600) // 2}")
        self.happiness_scale = tk.Scale(self.root, from_=-10, to=10, orient=tk.HORIZONTAL, label="Happiness Level")
        self.happiness_scale.set(0)  # Set the initial value to 0 (neutral)
        self.happiness_scale.pack()
        tk.Label(self.root, text="Unhappy (-10), Neutral (0), Happy (10)").pack()
        self.next_button = tk.Button(self.root, text="Next", command=self.next_video)
        self.next_button.pack()
        self.root.withdraw()  # Hide the root window

    def show_instruction_screen(self):
        self.instruction_root = tk.Toplevel(self.root)
        # Center the instruction window on the screen
        self.instruction_root.geometry(f"800x600+{(self.instruction_root.winfo_screenwidth() - 800) // 2}+{(self.instruction_root.winfo_screenheight() - 600) // 2}")
        InstructionScreen(self.instruction_root, "VideoFeedback", self.start_test)

    def start_test(self):
        self.instruction_root.destroy()  # Destroy the instruction screen
        self.play_next_video()

    def collect_feedback(self):
        #print("Collecting feedback...")
        # Show the happiness scale and next button
        self.root.deiconify()  # Show the root window

    def play_video(self, video_path):
        pygame.init()  # Initialize Pygame here
        self.root.withdraw()  # Hide the root window
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(video_path)
        #clipresized = clip.resize(height=700)
        #clipresized.preview()
        # show the clip in fullscreen
        clip.preview(fullscreen=True)
        #clip.preview()
        pygame.quit()  # Quit Pygame after the video ends
        self.collect_feedback()  # Collect feedback after the video ends

    def play_next_video(self):
        if self.current_video_index < len(self.video_files):
            video_path = os.path.join(self.video_dir, self.video_files[self.current_video_index])
            self.play_video(video_path)
        else:
            self.show_feedback_screen()

    def next_video(self):
        happiness_level = self.happiness_scale.get()
        video_name = self.video_files[self.current_video_index]
        #print(f"User: {self.username}, Video: {video_name}, Happiness Level: {happiness_level}")
        self.write_data_to_csv(video_name, happiness_level)
        self.current_video_index += 1
        self.play_next_video()

    def show_feedback_screen(self):
        self.root.destroy()  # Destroy the root window
        self.root = tk.Tk() # Create a new root window
        FeedbackScreen(self.root, self.username, self.root.destroy)

    def write_header_to_csv(self):
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Relative Time (ms)", "Video Name", "Happiness Level", self.username])

    def write_data_to_csv(self, video_name, happiness_level):
        current_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        relative_time = int((time.time() - self.start_time) * 1000)
        with open(self.path_to_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, relative_time, video_name, happiness_level, self.username])

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFeedbackApp(root, "testUser")
    root.mainloop()
