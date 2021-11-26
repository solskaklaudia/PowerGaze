import tkinter as tk
import autopy
import time
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController


keyboard = Controller()
mouse = MouseController()

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

def simulateDrag(root):
    root.destroy()
    time.sleep(2)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
    time.sleep(3)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)


def doubleClick(root):
    root.destroy()
    time.sleep(2)
    autopy.mouse.click()
    time.sleep(.1)
    autopy.mouse.click()


def rightClick(root):
    root.destroy()
    time.sleep(2)
    autopy.mouse.toggle(autopy.mouse.Button.RIGHT, True)
    time.sleep(.1)
    autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
    

def simulateCopy(root):
    root.destroy()
    time.sleep(2)
    keyboard.press(Key.ctrl)
    keyboard.press('c')
    keyboard.release('c')
    keyboard.release(Key.ctrl)


def simulatePaste(root):
    root.destroy()
    time.sleep(2)
    keyboard.press(Key.ctrl)
    keyboard.press('v')
    keyboard.release('v')
    keyboard.release(Key.ctrl)


def simulateScroll(root):
    root.destroy()
    time.sleep(2)
    autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, True)
    time.sleep(3)
    autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, False)


""" Contents """

# Drag mouse button
drag_image = tk.PhotoImage(file="img\\mouse\\drag.png").subsample(2)
drag = tk.Button(window, command = lambda: simulateDrag(root), image=drag_image)
drag["border"] = "0"
drag.grid(row=1,column=1,padx=80, pady=50)

# Double click button
double_click_image = tk.PhotoImage(file="img\\mouse\\double_click.png").subsample(2)
double_click = tk.Button(window, command = lambda: doubleClick(root), image=double_click_image)
double_click["border"] = "0"
double_click.grid(row=1,column=2,padx=80, pady=50)

# Right click button
right_click_image = tk.PhotoImage(file="img\\mouse\\right_click.png").subsample(2)
right_click = tk.Button(window, command = lambda: rightClick(root), image=right_click_image)
right_click["border"] = "0"
right_click.grid(row=1,column=3,padx=80, pady=50)


# Copy button
copy_image = tk.PhotoImage(file="img\\mouse\\copy.png").subsample(2)
copy = tk.Button(window, command = lambda: simulateCopy(root), image=copy_image)
copy["border"] = "0"
copy.grid(row=2,column=1,padx=80, pady=50)

# Paste button
paste_image = tk.PhotoImage(file="img\\mouse\\paste.png").subsample(2)
paste = tk.Button(window, command = lambda: simulatePaste(root), image=paste_image)
paste["border"] = "0"
paste.grid(row=2,column=2,padx=80, pady=50)

# Scroll button
scroll_image = tk.PhotoImage(file="img\\mouse\\scroll.png").subsample(2)
scroll = tk.Button(window, command = lambda: simulateScroll(root), image=scroll_image)
scroll["border"] = "0"
scroll.grid(row=2,column=3,padx=80, pady=50)


# Center the buttons
window.rowconfigure(0, weight=1)
window.rowconfigure(3, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(4, weight=1)


window.mainloop()