import tkinter as tk
import os

root = tk.Tk()
root.attributes('-alpha', 0.0)

root.iconify()
window = tk.Toplevel(root)

# get screen width and height
screen_width = root.winfo_screenwidth()     # width of the screen
screen_height = root.winfo_screenheight()   # height of the screen

window.geometry('%dx%d' % (screen_width, screen_height))

window.overrideredirect(1)                  # remove border
window.attributes('-topmost', 1)            # display on top


""" Functions """

def open_keyboard(root):
    root.destroy()
    os.system('osk')


""" Contents """

# Open mouse menu button
mouse_image = tk.PhotoImage(file="img\\functions\\mouse.png").subsample(2)
mouse = tk.Button(window, command = lambda: print("open mouse menu"), image=mouse_image)
mouse["border"] = "0"
mouse.grid(row=1,column=1,padx=80, pady=50)

# Zoom in button
zoom_image = tk.PhotoImage(file="img\\functions\\zoom.png").subsample(2)
zoom = tk.Button(window, command = lambda: print("zoom"), image=zoom_image)
zoom["border"] = "0"
zoom.grid(row=1,column=2,padx=80, pady=50)

# Open keyboard button
keyboard_image = tk.PhotoImage(file="img\\functions\\keyboard.png").subsample(2)
keyboard = tk.Button(window, command = lambda: open_keyboard(root), image=keyboard_image)
keyboard["border"] = "0"
keyboard.grid(row=1,column=3,padx=80, pady=50)


# Calibrate the system button
calibrate_image = tk.PhotoImage(file="img\\functions\\calibrate.png").subsample(2)
calibrate = tk.Button(window, command = lambda: print("calibrate"), image=calibrate_image)
calibrate["border"] = "0"
calibrate.grid(row=2,column=1,padx=80, pady=50)

# Return to default screen button
default_image = tk.PhotoImage(file="img\\functions\\default.png").subsample(2)
default = tk.Button(window, command = lambda: print("default screen"), image=default_image)
default["border"] = "0"
default.grid(row=2,column=2,padx=80, pady=50)

# Exit menu button
exit_image = tk.PhotoImage(file="img\\functions\\exit.png").subsample(2)
exit = tk.Button(window, command = lambda: root.destroy(), image=exit_image)
exit["border"] = "0"
exit.grid(row=2,column=3,padx=80, pady=50)


# Center the buttons
window.rowconfigure(0, weight=1)
window.rowconfigure(3, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(4, weight=1)


window.mainloop()