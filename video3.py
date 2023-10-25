import subprocess, os, platform

filepath = "./videos/starwar.mp4"
if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', filepath))
elif platform.system() == 'Windows':    # Windows
    os.startfile(filepath)
else:                                   # linux variants
    subprocess.call(('xdg-open', filepath))
    
    
    