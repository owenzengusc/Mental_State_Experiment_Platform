# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git


from tkinter import *
import tkinter as tk

def create_new_window(Title, Width, Height):
    # create new window
    new_window = Tk()
    new_window.title(Title)
    new_window.geometry("{}x{}".format(Width, Height))
    new_window.configure(bg='lightgray')
    
    # move window center
    posRight = int(new_window.winfo_screenwidth() / 2 - Width / 2)
    posDown = int(new_window.winfo_screenheight() / 2 - Height / 2)
    new_window.geometry("{}x{}+{}+{}".format(Width, Height, posRight, posDown))
    
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
    window = create_new_window("EEG_Sensor_Interface", 800, 600)
    button = create_new_button(window,"Start",10,2,200,100)
    window.mainloop()