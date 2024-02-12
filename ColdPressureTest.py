import tkinter as tk
import pygame
import csv
import time

class ColdPressureTest:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Cold Pressure Test")
        pygame.mixer.init()
        self.username = username
        self.first_relaxation_duration = 180  # 3 minutes
        self.test_duration = 180
        self.post_test_relaxation_duration = 175  # 2 minutes 55 seconds 5 seconds for hand removal

        # Define the path for the CSV file including the username
        self.cpt_data_path = f'./data/cptTest_{self.username}.csv'

        self.setup_gui()
        self.create_csv_file()

    def setup_gui(self):
        self.label = tk.Label(self.master, text="", font=("Arial", 50))
        self.label.pack(pady=20)

        self.countdown_label = tk.Label(self.master, text="", font=("Arial", 70))
        self.countdown_label.pack(pady=10)

    def create_csv_file(self):
        """Create or append to the CSV file with headers if it's new."""
        with open(self.cpt_data_path, 'a', newline='') as file:
            file.seek(0, 2)  # Go to the end of the file
            if file.tell() == 0:  # Check if file is empty
                writer = csv.writer(file)
                writer.writerow(['Event', 'Start Time', 'Duration (seconds)'])

    def record_event(self, event_name, duration):
        """Record the event start time and duration to the CSV file."""
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with open(self.cpt_data_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([event_name, start_time, duration])

    def start_initial_relaxation(self):
        self.label.config(text="Please relax and close your eyes.")
        self.record_event('Initial Relaxation', self.first_relaxation_duration)  # Assuming 180 seconds for relaxation
        self.start_countdown(self.first_relaxation_duration, self.play_cpt_instruction)  # Adjust duration as necessary
        self.play_audio('relax.mp3')

    def play_cpt_instruction(self):
        self.label.config(text="Please put and keep \n your hand in iced water now.")
        self.record_event('Hand in Water', self.test_duration)  # Assuming 180 seconds for hand in water
        self.start_countdown(self.test_duration, self.end_instruction)  # Adjust duration as necessary
        self.play_audio('CPT.mp3')
        self.wait_and_play_next('clock.mp3')

    def end_instruction(self):
        # Stop any playing music, including the clock sound
        pygame.mixer.music.stop()
        self.label.config(text="You can remove your hand now.")
        self.countdown_label.config(text="")
        self.master.after(5000, self.start_post_test_relaxation)  # 5 seconds

    def start_post_test_relaxation(self):
        self.label.config(text="Please relax and close your eyes.")
        self.record_event('Post-Test Relaxation', self.post_test_relaxation_duration)  # Assuming 175 seconds for relaxation
        self.start_countdown(self.post_test_relaxation_duration, self.test_complete)  # Adjust duration as necessary
        self.play_audio('relax.mp3')

    def test_complete(self):
        pygame.mixer.music.stop()
        self.label.config(text="Test Complete. Thank you.")
        self.countdown_label.config(text="")
        self.master.after(5000, self.master.destroy)  # Close window after 5 seconds

    def play_audio(self, file_path):
        pygame.mixer.music.load(file_path)
        if file_path == 'clock.mp3':
            pygame.mixer.music.play(10) # Play 10 times
        else:
            pygame.mixer.music.play()

    def wait_and_play_next(self, next_track):
        def check_music():
            if not pygame.mixer.music.get_busy():
                self.play_audio(next_track)
            else:
                # Check again after a short delay
                self.master.after(100, check_music)
        check_music()

    def start_countdown(self, duration, callback):
        def countdown(time_left=int(duration)):
            if time_left <= 0:
                callback()
            else:
                self.countdown_label.config(text=str(time_left))
                self.master.after(1000, countdown, time_left-1)
        countdown()

def show_cold_pressure_test(username):
    root = tk.Tk()
    window_width = 1000
    window_height = 800

    # Get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the center position
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the window position to the center of the screen
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    app = ColdPressureTest(root, username)
    app.start_initial_relaxation()  # Start the sequence
    root.mainloop()

if __name__ == "__main__":
    # Example username, replace with dynamic input as needed
    username = "testUser"
    show_cold_pressure_test(username)
