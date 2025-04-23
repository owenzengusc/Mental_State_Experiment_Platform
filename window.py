# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git


from tkinter import *
import tkinter as tk
from window_utils import set_responsive_geometry, get_responsive_window_size, calculate_center_position

def create_new_window(Title, Width=None, Height=None, window_type="small"):
    # create new window
    new_window = Tk()
    new_window.title(Title)
    
    # If Width and Height are provided, use them
    # Otherwise, use responsive sizing based on window_type
    if Width and Height:
        posRight = int(new_window.winfo_screenwidth() / 2 - Width / 2)
        posDown = int(new_window.winfo_screenheight() / 2 - Height / 2)
        new_window.geometry("{}x{}+{}+{}".format(Width, Height, posRight, posDown))
    else:
        # Use the responsive geometry function
        set_responsive_geometry(new_window, window_type)
    
    new_window.configure(bg='lightgray')
    return new_window


def create_new_button(window, Text="button", Width=10, Height=20, x=0, y=0, Command=None):
    new_button = Button(window, text=Text, width=Width, height=Height, command=Command)
    new_button.place(x=x, y=y)
    return new_button

def create_entry_box(window, Width, x=0, y=0):
    new_entry_box = Entry(window, width=Width)
    new_entry_box.place(x=x, y=y)
    return new_entry_box


if __name__ == "__main__":
    window = create_new_window("EEG_Sensor_Interface", window_type="main")
    button = create_new_button(window,"Start",10,2,200,100)
    window.mainloop()