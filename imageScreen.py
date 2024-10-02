import tkinter as tk
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, image_path):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("Image Viewer")

        # Set window size
        window_width = 1800
        window_height = 1000

        # Get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the window position to the center of the screen
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Load and prepare the image
        self.img = Image.open(image_path)
        self.img = self.img.resize((400, 400))  # Resize if needed
        self.img_tk = ImageTk.PhotoImage(self.img)

        # Create a label widget to display the image
        self.label = tk.Label(self.window, image=self.img_tk)
        self.label.pack()

        # Start the main loop for the window
        self.window.mainloop()

if __name__ == "__main__":
    viewer = ImageViewer("images/IMG_1255.jpg")

