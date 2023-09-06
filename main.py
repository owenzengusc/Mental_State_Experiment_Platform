# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git

from tkinter import *

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


def create_new_button(window,Text,Width,Height,Row,Column,Command=None):
    new_button = Button(window, text=Text, width=Width, height=Height)
    new_button.grid(row=Row, column=Column)
    return new_button
    
window = create_new_window("EEG_Sensor_Interface", 800, 600)
button = create_new_button(window,"Start",10,2,0,0)
window.mainloop()
    
    
    
    



