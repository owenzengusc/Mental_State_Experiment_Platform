# RelaxationScreen.py
import tkinter as tk
import pygame

class RelaxationScreen:
    def __init__(self, master, duration=180):  # Adjust duration as needed
        self.master = master
        self.duration = duration
        self.master.title("Relaxation Time")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event

        # Setup window size and position
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 1800
        window_height = 1000
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.master.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

        # change the background color
        self.master.configure(bg="#97C1A9")

        pygame.mixer.init()
        self.play_music('relax.mp3')

        self.setup_gui()
        self.update_countdown()  # Start the countdown

    def setup_gui(self):
        self.label = tk.Label(self.master, text="Please close your eyes and relax", font=("Arial", 70), bg="#97C1A9")
        self.label.pack(pady=20)

        # Initialize countdown label with the correct starting duration
        self.countdown_label = tk.Label(self.master, text="Time Remaining: "+f"{self.duration}"+"s", font=("Arial", 65), bg="#97C1A9")
        self.countdown_label.pack(pady=10)

    def play_music(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)  # Play indefinitely

    def update_countdown(self):
        if self.duration > 0:
            # Update the label to include the full text with the remaining time
            self.countdown_label.config(text="Time Remaining: " + f"{self.duration}" + "s")
            self.duration -= 1
            self.master.after(1000, self.update_countdown)
        else:
            self.stop_music_and_close()

    def stop_music_and_close(self):
        pygame.mixer.music.stop()
        self.play_music("OpenEyes.mp3")
        self.master.after(1800, pygame.mixer.music.stop)
        self.master.after(2000, self.master.destroy)

    def on_close(self):
        self.stop_music_and_close()

def show_relaxation_screen(duration=180):  
    root = tk.Tk()
    app = RelaxationScreen(root, duration=duration)
    root.mainloop()

if __name__ == "__main__":
    show_relaxation_screen()
