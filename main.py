# EEG_Sensor_Interface
# Owen Zeng
# https://github.com/owenzengusc/EEG_Senor_Interface.git

from window import *
from user import *


def main():
    main_window = create_new_window("EEG_Sensor_Interface", 800, 600)
    # create new canvas
    canvas_main = tk.Canvas(main_window, width=800, height=600)
    canvas_main.pack()

    # create new entry box
    entry_name = tk.Entry(main_window) 
    #
    canvas_main.create_window(200, 140, window=entry_name)
    
    ppl = Participant()
    def get_user_name(windw, enntry, canvas):
        user_name = enntry.get()
        user_name_lable = tk.Label(windw, text=user_name)
        canvas.create_window(200, 230, window=user_name_lable)
        ppl.name = user_name
    
    # button1 is a button that calls get_user_name() when clicked
    button1 = tk.Button(text='Enter', command= lambda: get_user_name(main_window, entry_name, canvas_main))
   
    canvas_main.create_window(200, 180, window=button1)
    while True:
        # wait for user to enter name
        if ppl.name != "New_User":
            print(ppl.name)
            break
        main_window.update()
    main_window.mainloop()

if __name__ == "__main__":
    main()

    
    

