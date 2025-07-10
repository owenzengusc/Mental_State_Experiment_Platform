# RelaxationScreen.py
import tkinter as tk
import pygame
import threading
import time
from resource_utils import get_resource_path

background_color = "white"

class RelaxationScreen:
    def __init__(self, master, duration=180):  # Adjust duration as needed
        self.master = master
        self.duration = duration
        self.master.title("Relaxation Time")
        
        # Thread control flag
        self.running = True
        
        # Handle window close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Setup window size and position with responsive sizing
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Calculate responsive window size (85% of screen)
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # Ensure window size is reasonable
        window_width = min(window_width, 1920)
        window_height = min(window_height, 1080)
        
        # Calculate center position
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        
        # Apply the window geometry
        self.master.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

        # change the background color
        self.master.configure(bg=background_color)

        # Audio state tracking
        self.music_playing = False
        self.pygame_initialized = False
        
        # Initialize pygame in a safe way
        self.init_pygame()
        
        # Play music in a thread to avoid blocking
        self.play_music_thread(get_resource_path('relax.mp3'))

        self.setup_gui()
        self.update_countdown()  # Start the countdown

    def init_pygame(self):
        """Initialize pygame safely"""
        try:
            if not hasattr(pygame, 'mixer') or not pygame.mixer.get_init():
                pygame.mixer.init()
            self.pygame_initialized = True
        except Exception as e:
            print(f"Error initializing pygame: {e}")
            self.pygame_initialized = False

    def setup_gui(self):
        self.label = tk.Label(self.master, text="Please close your eyes and relax \n until next instruction", font=("Arial", 70), bg=background_color, fg="black")
        self.label.pack(pady=20)

        # Initialize countdown label with the correct starting duration
        self.countdown_label = tk.Label(self.master, text="Time Remaining: "+f"{self.duration}"+"s", font=("Arial", 65), bg=background_color, fg="black")
        self.countdown_label.pack(pady=10)

    def play_music(self, file_path):
        """Play music in a thread-safe way"""
        try:
            if self.pygame_initialized:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play(-1)  # Play indefinitely
                self.music_playing = True
        except Exception as e:
            print(f"Error playing music: {e}")
            
    def play_music_thread(self, file_path):
        """Start music in a separate thread"""
        music_thread = threading.Thread(target=self.play_music, args=(file_path,))
        music_thread.daemon = True
        music_thread.start()

    def stop_music(self):
        """Stop music in a thread-safe way"""
        try:
            if self.pygame_initialized and self.music_playing:
                pygame.mixer.music.stop()
                self.music_playing = False
        except Exception as e:
            print(f"Error stopping music: {e}")

    def update_countdown(self):
        if not self.running:
            return
            
        if self.duration > 0:
            try:
                # Update the label to include the full text with the remaining time
                self.countdown_label.config(text="Time Remaining: " + f"{self.duration}" + "s")
                self.duration -= 1
                self.master.after(1000, self.update_countdown)
            except tk.TclError:
                # Window was probably destroyed
                pass
        else:
            self.stop_music_and_close()

    def stop_music_and_close(self):
        """Safe cleanup and window close"""
        if not self.running:
            return
            
        self.running = False
        self.stop_music()
        
        try:
            self.master.destroy()
        except tk.TclError:
            # Window was probably already destroyed
            pass
    
    def on_close(self):
        """Handle window closing event properly"""
        self.running = False
        self.stop_music()
        
        # Allow time for threads to clean up
        time.sleep(0.1)
        
        try:
            self.master.destroy()
        except tk.TclError:
            # Window was probably already destroyed
            pass

def show_relaxation_screen(duration=180):
    root = tk.Tk()
    app = RelaxationScreen(root, duration)
    root.mainloop()

if __name__ == "__main__":
    show_relaxation_screen()
