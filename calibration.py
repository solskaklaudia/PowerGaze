import time 
import tkinter as tk

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

canvas = tk.Canvas(window, width = screen_width, height = screen_height)
canvas.pack()

# Display informational text before calibration
info = "Podążaj wzrokiem za pojawiającymi się punktami w celu kalibracji systemu."
canvas.create_text(screen_width/2, screen_height/2, fill="red", font="Arial 30 bold", text=info, tags="info")

root.update()
time.sleep(3)

# Clear the canvas
canvas.delete("info")
root.update()

margin = int(0.05 * screen_height)
circle_size = int(0.1 * screen_height)

# Animation functions
def setCircle(size, color):
    canvas.itemconfig("circle", width = size, fill = color, outline = color)
    root.update()
    time.sleep(0.5)

def animateCircle():
    setCircle(int(circle_size/6), "green")
    setCircle(int(circle_size/12), "red")
    setCircle(int(circle_size/24), "orange")
    setCircle(int(circle_size/48), "gold")


# O  -  -
# -  -  -
# -  -  -

canvas.create_oval(margin, margin, circle_size, circle_size, fill="green", outline="green", tags="circle")
animateCircle()

# -  O  -
# -  -  -
# -  -  -

canvas.move("circle", int(screen_width/2-margin), 0)
animateCircle()

# -  -  O
# -  -  -
# -  -  -

canvas.move("circle", int(screen_width/2-2*margin), 0)
animateCircle()

# -  -  -
# O  -  -
# -  -  -

canvas.move("circle", -screen_width+3*margin, int(screen_height/2-margin))
animateCircle()

# -  -  -
# -  O  -
# -  -  -

canvas.move("circle", int(screen_width/2-margin), 0)
animateCircle()

# -  -  -
# -  -  O
# -  -  -

canvas.move("circle", int(screen_width/2-2*margin), 0)
animateCircle()

# -  -  -
# -  -  -
# O  -  -

canvas.move("circle", -screen_width+3*margin, int(screen_height/2-2*margin))
animateCircle()

# -  -  -
# -  -  -
# -  O  -

canvas.move("circle", int(screen_width/2-margin), 0)
animateCircle()

# -  -  -
# -  -  -
# -  -  O

canvas.move("circle", int(screen_width/2-2*margin), 0)
animateCircle()


# clear the canvas
canvas.delete("circle")

# display quick usage instructions after calibration
screen_above = "⬆ funkcje myszy"               # mouse functions
screen_below = "⬇ przybliżanie ekranu"         # screen magnifier
screen_left = "⬅ otwórz/zamknij klawiaturę"    # open/close keyboard
screen_right = "ponowna kalibracja ➡"          # recalibrate

canvas.create_text(screen_width/2, screen_height/5, fill="red", font="Arial 30 bold", text=screen_above)
canvas.create_text(screen_width/2, screen_height*4/5, fill="red", font="Arial 30 bold", text=screen_below)
canvas.create_text(screen_width/5, screen_height/2, fill="red", font="Arial 30 bold", text=screen_left)
canvas.create_text(screen_width*4/5, screen_height/2, fill="red", font="Arial 30 bold", text=screen_right)

root.update()

time.sleep(3)
