# import necessary packages

import tkinter as tk
import serial
from screeninfo import get_monitors


########################## FUNCTION TO DISPLAY THE INSTRUCTIONS ##########################
def instructions():
    ###CANVAS###
    # Get the dimensions of the screen
    window_width = screen.winfo_width()
    window_height = screen.winfo_height()
    # create canvas
    canvas_width = 2000
    canvas_height = 1000
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas in the center of the window
    global canvas
    canvas = tk.Canvas(screen, width=canvas_width, height=canvas_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    # Create the text (instructions) that will be displayed on the canvas
    #################################
    ###WRITE THE INSTRUCTIONS HERE###
    #################################
    instructions = f"Sente-se confortavelmente.\n Quando o símbolo\n +\naparecer no ecrã mantenha o olhar no símbolo.\n Carregue no botão se compreendeu as instruções."
    canvas.create_text(canvas_width // 2, canvas_height // 2,
                       text=instructions,
                       font=("Calibri", 20), anchor="center", justify="center", tags="inst")

    # Create the "next" button at the bottom of the screen
    global frame_button_next
    frame_button_next = tk.Frame(screen)
    frame_button_next.pack(side=tk.BOTTOM, fill=tk.X, pady=300)

    # when the next button is clicked, start the start screen
    global button_next
    button_next = tk.Button(frame_button_next, text="Avançar", command=start_screen)
    button_next.pack()


############################### START_SCREEN FUNCTION############################
def start_screen():
    canvas.delete("inst")  # delete the instructions
    frame_button_next.destroy()  # destroy the "next" button
    # Create the start button
    global frame_button_start
    frame_button_start = tk.Frame(screen)
    frame_button_start.place(anchor='center', relx=0.5, rely=0.5)
    button_font = ("Arial", 12)
    # The starting button calls the countdown function
    button_start = tk.Button(frame_button_start, text="Carregue aqui para iniciar.", font=button_font, height=2, width=20,
                             command=start)
    button_start.pack()


def countdown(minutes, seconds):
    # Create canvas and place it in the center
    canvas_width = 900
    canvas_height = 300
    canvas = tk.Canvas(screen, width=canvas_width, height=canvas_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    # Create text for the timer
    time = f"{minutes:02d}:{seconds:02d}"
    timer_text_id = canvas.create_text(canvas_width / 2, canvas_height / 2, text=time, font=("Arial", 24), tags="timer")

    # Update the timer text
    canvas.itemconfig(timer_text_id, text=time)

    # Counts down the minutes and seconds
    # Counts down the minutes and seconds
    if minutes > 0 or seconds > 0:
        if seconds == 0:
            time = f"{minutes:02d}:00"
            canvas.itemconfig(timer_text_id, text=time)
            # Countdown to the next minute
            screen.after(1000,countdown, minutes - 1, 59)
        else:
            # Countdown to the next second
            screen.after(1000, countdown, minutes, seconds - 1)
    else:  # Once the countdown is at 00:00
        canvas.delete("timer")  # Delete the timer
        canvas.create_text(canvas_width / 2, canvas_height / 2, text="+", font=("Arial", 40),
                           tags="fixation")  # Display the fixation cross
        # After the defined time, the cross disappears and the next countdown starts
        ######################################################
        ### DEFINE THE DURATION OF THE FIXATION CROSS HERE ###
        ######################################################
        screen.after(120000, loop_countdown)


############################### LOOP_COUNTDOWN FUNCTION############################
# This function creates a loop of countdown and fixation cross
# the initial "repetitions_countdown_cross" defines the number of repetitions
def loop_countdown():
    global repetitions_countdown_cross  # this needs to be defined at the beginning of the code
    print(f"Countdown_cross:{repetitions_countdown_cross}")
    repetitions_countdown_cross -= 1  # every time that this function is called, decrease the number of repetitions
    if repetitions_countdown_cross >= 0:  # once all the repetitions have been executed
        ########################################################
        ######DEFINE THE DURATION OF THE TIMER HERE############
        ########################################################
        countdown(3, 0)
    else:  # when all the repetitions are executed, close the program
        arduino.write(bytes('2', 'utf-8'))  # sends the closing signal to arduino
        print("signal sent_2")
        screen.destroy()

def start():
    arduino.write(bytes('1', 'utf-8'))  # sends the starting signal to arduino
    print("signal 1 sent")
    loop_countdown()


##########################################################################
###################### THE CODE STARTS HERE ##############################
##########################################################################

### ARDUINO ###
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

### SCREEN ###
# Get information about all screens
monitors = get_monitors()
# Set monitor to the big monitor
second_monitor = monitors[1]
screen_width = second_monitor.width
screen_height = second_monitor.height
# Create a new Tkinter window
screen = tk.Tk()
# Position and size the window to fit the second screen and make it fullscreen
screen.geometry(f"{screen_width}x{screen_height}+{second_monitor.x}+{second_monitor.y}")

###### Define the number of repetitions here###
### 1 repetition represents the countdown timer and the fixation cross ###

repetitions_countdown_cross = 2


instructions()

screen.mainloop()