import tkinter as tk
from subprocess import Popen
from pyautogui import press, hotkey
import time

root = tk.Tk()
root.attributes('-alpha', 0.0)

root.iconify()
window = tk.Toplevel(root)

# Get screen width and height
screen_width = root.winfo_screenwidth()     # width of the screen
screen_height = root.winfo_screenheight()   # height of the screen

window.geometry('%dx%d' % (screen_width, screen_height))

window.overrideredirect(1)                  # remove border
window.attributes('-topmost', 1)            # display on top


""" Functions """

def zoomIn(root):
    root.destroy()
    Popen("Magnify.exe", shell=True)
    # Perform zoom in and out hotkey to get rid of magnifier frame
    time.sleep(5)  
    hotkey("win", "+")
    press("backspace")                      # removes the '+'
    hotkey("win", "-")

def returnToDefault(root):
    root.destroy()
    Popen("wmic process where name='Magnify.exe' delete", shell = True)

def exitMenu(root):
    root.destroy()


""" Contents """

# Zoom in button
zoom_image = tk.PhotoImage(file="img\\functions\\zoom.png").subsample(2)
zoom = tk.Button(window, command = lambda: zoomIn(root), image=zoom_image)
zoom["border"] = "0"
zoom.grid(row=1,column=1,padx=100, pady=50)

# Return to default screen (close the magnifier) button
default_image = tk.PhotoImage(file="img\\functions\\default.png").subsample(2)
default = tk.Button(window, command = lambda: returnToDefault(root), image=default_image)
default["border"] = "0"
default.grid(row=1,column=2,padx=100, pady=50)

# Exit menu button
exit_image = tk.PhotoImage(file="img\\functions\\exit.png").subsample(2)
exit = tk.Button(window, command = lambda: exitMenu(root), image=exit_image)
exit["border"] = "0"
exit.grid(row=1,column=3,padx=100, pady=50)

# Center the buttons
window.rowconfigure(0, weight=1)
window.rowconfigure(2, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(4, weight=1)


window.mainloop()