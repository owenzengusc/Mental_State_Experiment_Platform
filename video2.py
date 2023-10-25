import os
# os.startfile("./videos/starwar.mp4")

def openFile():
    fileName = listbox_1.get(ACTIVE)
    os.system("start " + fileName)