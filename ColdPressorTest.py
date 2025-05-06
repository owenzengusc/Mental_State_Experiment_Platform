import tkinter as tk
import pygame
import csv
import time
from datetime import datetime

background_color = "white"

class ColdPressorTest:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Cold Pressor Test")
        
        # Thread control flag
        self.running = True
        
        # Add proper window close handler
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        pygame.mixer.init()
        self.username = username
        self.first_relaxation_duration = 180  # 3 minutes 180
        self.test_duration = 180 # 3 minutes 180
        self.post_test_relaxation_duration = 175  # 2 minutes 55 seconds 5 seconds for hand removal 175
        self.StartTime = None
        self.EndTime = None
        self.setup_gui()
        
        # Audio state tracking
        self.music_playing = False
        
    def on_closing(self):
        """Handle window closing event properly"""
        self.running = False
        
        # Stop any music
        self.stop_music()
        
        # Allow time for things to clean up
        time.sleep(0.1)
        
        # Close the window
        try:
            self.master.destroy()
        except tk.TclError:
            pass  # Window might already be destroyed
            
    def stop_music(self):
        """Stop any playing music"""
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except Exception as e:
            print(f"Error stopping music: {e}")
        
    def log_event(self, event_name, start_time, end_time, duration, username='New_User'):
        log_data_path = f'./data/log_{username}.csv'

        # Convert start_time and end_time to strings with milliseconds only if they are not None
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] if start_time else ''
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] if end_time else ''

        # Check if the file exists and write headers if it's new
        try:
            with open(log_data_path, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Event', 'Start Time', 'End Time', 'Duration (milliseconds)'])
        except FileExistsError:
            pass  # File already exists, append to it without writing headers

        # Write the event data
        with open(log_data_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([event_name, start_time_str, end_time_str, duration])
        
    def setup_gui(self):
        self.label = tk.Label(self.master, text="", font=("Arial", 50), fg="black")
        self.label.pack(pady=20)

        self.countdown_label = tk.Label(self.master, text="", font=("Arial", 70), fg="black")
        self.countdown_label.pack(pady=10)

    def start_initial_relaxation(self):
        if not self.running:
            return
            
        self.master.configure(bg=background_color)
        self.label.config(text="Please close your eyes and relax \n until next instruction", bg=background_color, fg="black")
        self.countdown_label.config(bg=background_color, fg="black")
        self.start_countdown(self.first_relaxation_duration, self.play_cpt_instruction)  # 3 minutes
        self.StartTime = datetime.now()
        # Record the event start time and duration
        self.log_event('CPT Initial Relaxation Start', self.StartTime, None, None, username=self.username)
        self.play_audio('relax.mp3')
        
    def play_cpt_instruction(self):
        if not self.running:
            return
            
        # log the end of the initial relaxation
        self.EndTime = datetime.now()
        duration = int((self.EndTime - self.StartTime).total_seconds() * 1000)  # Duration in milliseconds
        self.log_event('CPT Initial Relaxation End', self.StartTime, self.EndTime, duration, username=self.username)
        self.master.configure(bg="White")
        self.label.config(text="Please put and keep \n your hand in iced water now.", bg="White", fg="black")
        self.countdown_label.config(bg="White", fg="black")
        self.start_countdown(self.test_duration, self.end_instruction)  # 3 minutes for CPT
        self.StartTime = datetime.now()
        # Record the event start time and duration
        self.log_event('CPT Test Start', self.StartTime, None, None, username=self.username)
        self.play_audio('CPT.mp3')
        self.wait_and_play_next('clock.mp3')
        
    def end_instruction(self):
        if not self.running:
            return
            
        self.EndTime = datetime.now()
        duration = int((self.EndTime - self.StartTime).total_seconds() * 1000)  # Duration in milliseconds
        self.log_event('CPT Test End', self.StartTime, self.EndTime, duration, username=self.username)
        self.master.configure(bg=background_color)
        self.label.config(text="You can remove your hand now.", bg=background_color, fg="black")
        self.countdown_label.config(text="", bg=background_color, fg="black")
        self.stop_music()
        self.play_audio('RemoveHand.mp3')
        self.master.after(5000, self.start_post_test_relaxation)  # 5 seconds

    def start_post_test_relaxation(self):
        if not self.running:
            return
            
        self.label.config(text="Please relax and close your eyes.", bg=background_color, fg="black")
        self.start_countdown(self.post_test_relaxation_duration, self.test_complete)  # 175 seconds
        # Log the start of the post test relaxation
        self.StartTime = datetime.now()
        self.log_event('CPT Post Test Relaxation Start', self.StartTime, None, None, username=self.username)
        self.play_audio('relax.mp3')

    def test_complete(self):
        if not self.running:
            return
            
        # log the end of the post test relaxation
        self.EndTime = datetime.now()
        duration = int((self.EndTime - self.StartTime).total_seconds() * 1000)  # Duration in milliseconds
        self.log_event('CPT Post Test Relaxation End', self.StartTime, self.EndTime, duration, username=self.username)
        self.stop_music()
        self.label.config(text="Test Complete. Thank you.", bg=background_color, fg="black")
        self.countdown_label.config(text="", bg=background_color, fg="black")
        
        try:
            self.master.after(5000, self.master.destroy)  # Close window after 5 seconds
        except tk.TclError:
            pass  # Window might already be destroyed

    def play_audio(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            if file_path == 'clock.mp3':
                pygame.mixer.music.play(10) # Play 10 times
            else:
                pygame.mixer.music.play()
            self.music_playing = True
        except Exception as e:
            print(f"Error playing audio: {e}")

    def wait_and_play_next(self, next_track):
        def check_music():
            if not self.running:
                return
                
            if not pygame.mixer.music.get_busy():
                self.play_audio(next_track)
            else:
                # Check again after a short delay
                try:
                    self.master.after(100, check_music)
                except tk.TclError:
                    pass  # Window might already be destroyed
        check_music()

    def start_countdown(self, duration, callback):
        def countdown(time_left=duration):
            if not self.running:
                return
                
            if time_left <= 0:
                callback()
            else:
                try:
                    self.countdown_label.config(text="Time Remaining: " + f"{time_left}" + "s", fg="black")
                    self.master.after(1000, countdown, time_left-1)
                except tk.TclError:
                    pass  # Window might already be destroyed
        countdown()

def show_cold_pressure_test(username):
    root = tk.Tk()
    
    # Get responsive window size (85% of screen)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.85)
    window_height = int(screen_height * 0.85)
    
    # Ensure window size is reasonable
    window_width = min(window_width, 1920)
    window_height = min(window_height, 1080)
    
    # Set minimum size constraints
    window_width = max(window_width, 1200)
    window_height = max(window_height, 800)

    # Calculate the center position
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the window position to the center of the screen
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    # Set reasonable min/max sizes
    root.minsize(min(window_width, 1000), min(window_height, 700))
    root.maxsize(screen_width, screen_height)

    app = ColdPressorTest(root, username)
    app.start_initial_relaxation()  # Start the sequence
    root.mainloop()

if __name__ == "__main__":
    # Example username, replace with dynamic input as needed
    username = "testUser"
    show_cold_pressure_test(username)
