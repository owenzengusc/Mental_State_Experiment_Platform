# ColdPressorTest.py
import tkinter as tk
import pygame

class ColdPressorTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Cold Pressor Test")

        # Initialize pygame for audio playback
        pygame.mixer.init()

        self.setup_gui()

    def setup_gui(self):
        self.label = tk.Label(self.master, text="", font=("Arial", 50))
        self.label.pack(pady=20)

        self.countdown_label = tk.Label(self.master, text="", font=("Arial", 70))
        self.countdown_label.pack(pady=10)

    def start_initial_relaxation(self):
        self.master.configure(bg="#97C1A9")
        self.label.config(text="Please close your eyes and relax \n until next instruction", bg="#97C1A9")
        self.countdown_label.config(bg="#97C1A9")
        self.start_countdown(18, self.play_cpt_instruction)  # 3 minutes
        self.play_audio('relax.mp3')

    def play_cpt_instruction(self):
        self.master.configure(bg="White")
        self.label.config(text="Please put and keep \n your hand in iced water now.", bg="White")
        self.countdown_label.config(bg="White")
        self.start_countdown(18, self.end_instruction)  # 3 minutes for CPT
        self.play_audio('CPT.mp3')
        self.wait_and_play_next('clock.mp3')

    def end_instruction(self):
        self.master.configure(bg="#97C1A9")
        self.label.config(text="You can remove your hand now.", bg="#97C1A9")
        self.countdown_label.config(text="", bg="#97C1A9")
        pygame.mixer.music.stop()
        self.play_audio('RemoveHand.mp3')
        self.master.after(5000, self.start_post_test_relaxation)  # 5 seconds

    def start_post_test_relaxation(self):
        self.label.config(text="Please relax and close your eyes.")
        self.start_countdown(17, self.test_complete)  # 175 seconds
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
        def countdown(time_left=duration):
            if time_left <= 0:
                callback()
            else:
                self.countdown_label.config(text="Time Remaining: " + f"{time_left}" + "s")
                self.master.after(1000, countdown, time_left-1)
        countdown()
    

def show_cold_pressure_test():
    root = tk.Tk()
    window_width = 1800
    window_height = 1000

    # Get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the center position
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Set the window position to the center of the screen
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    app = ColdPressorTest(root)
    app.start_initial_relaxation()  # Start the sequence
    root.mainloop()


if __name__ == "__main__":
    show_cold_pressure_test()
