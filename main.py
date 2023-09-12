# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git

from window import *

if __name__ == "__main__":
    awindow = create_new_window("EEG_Sensor_Interface", 800, 600)
    abutton = create_new_button(awindow,"Start",10,2,400,300)
    awindow.mainloop()