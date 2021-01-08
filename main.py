from tkinter import *
from math import floor

# CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#228b22"
YELLOW = "#f7f5dd"
FONT_BIG = ("Courier", 50, "bold")
FONT_MEDIUM = ("Courier", 30, "bold")
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
WIDTH = 200
HEIGHT = 224
CHECKMARK = '✓'
TITLE = 'Timer'

# GLOBAL VARIABLES ------------------------ #
rounds = 0
checkmarks = []
current_timer = None


# TIMER ACTIONS --------------------------- #
def reset_timer():
    """resets timer_text, cancels the current countdown,
    sets the header back to TITLE, resets the rounds and deletes all checkmarks"""
    global rounds, checkmarks
    canvas.itemconfig(timer_text, text='00:00')
    window.after_cancel(current_timer)
    adjust_header(-1)
    rounds = 0
    for checkmark in checkmarks:
        checkmark.destroy()
    checkmarks = []


def start_timer():
    """starts the rounds count and sets the timer_time and the header accordingly"""
    global rounds
    rounds += 1
    if rounds == 8:
        timer_time = LONG_BREAK_MIN
        rounds = 0
    elif rounds % 2 == 0:
        timer_time = SHORT_BREAK_MIN
        show_checkmark()
    else:
        timer_time = WORK_MIN
    countdown(timer_time * 60)
    adjust_header(timer_time)


def countdown(minutes):
    """loops every second, refreshing the timer display with the current minutes and seconds"""
    global rounds
    mt = floor(minutes / 60)
    sc = floor(minutes % 60)
    if mt < 10:
        mt = f'0{mt}'
    if sc < 10:
        sc = f'0{sc}'
    clock = f'{mt}:{sc}'
    canvas.itemconfig(timer_text, text=clock)
    if minutes > 0:
        global current_timer
        current_timer = window.after(1000, countdown, minutes - 1)
    elif minutes == 0 and 0 < rounds < 8:
        start_timer()


def show_checkmark():
    """shows a checkmark symbol for every completed work timer at the bottom of the screen"""
    checkmark = Label(text=CHECKMARK, fg=GREEN, bg=YELLOW, font=FONT_BIG)
    checkmark.grid(column=len(checkmarks), row=3)
    checkmarks.append(checkmark)


def adjust_header(time):
    """changes the header text according to the timer running"""
    if time == WORK_MIN:
        header.config(text='Working', fg=GREEN)
        header.grid(column=1, row=0)
    elif time == SHORT_BREAK_MIN:
        header.config(text='Break', fg=PINK)
    elif time == LONG_BREAK_MIN:
        header.config(text='Big Break', fg=RED)
    elif time == -1:
        header.config(text=TITLE, fg=GREEN)


# UI SETUP -------------------------------- #
# WINDOW
window = Tk()
window.title('Pomodoro Timer')
window.minsize(width=400, height=400)
window.config(bg=YELLOW, padx=50, pady=20)

# HEADER TEXT
header = Label(text=TITLE, font=FONT_BIG, fg=GREEN, bg=YELLOW)
header.grid(column=1, row=0)

# BACKGROUND IMAGE
img = PhotoImage(file='./tomato.png')
canvas = Canvas(width=WIDTH, height=HEIGHT, bg=YELLOW, highlightthickness=0)
canvas.create_image(WIDTH / 2, HEIGHT / 2, image=img)
timer_text = canvas.create_text(WIDTH / 2, HEIGHT / 1.7, text='00:00', fill=GREEN, font=FONT_BIG)
canvas.grid(column=1, row=1)

# START AND RESET BUTTONS
start_button = Button(window, text='START', fg=RED, bg=YELLOW, highlightthickness=0, font=FONT_MEDIUM,
                      command=start_timer)
start_button.grid(column=0, row=2)
reset_button = Button(window, text='RESET', fg=RED, bg=YELLOW, highlightthickness=0, font=FONT_MEDIUM,
                      command=reset_timer)
reset_button.grid(column=2, row=2)

# KEEP TIMER RUNNING
window.mainloop()
