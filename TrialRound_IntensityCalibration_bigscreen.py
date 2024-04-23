# import the packages
import tkinter as tk
from PIL import ImageTk, Image
from screeninfo import get_monitors

def start_button():
    # create frame for the button
    global frame
    frame_start = tk.Frame(second_screen_window, width=200, height=100)
    frame_start.place(anchor='center', relx=0.5, rely=0.5)
    global start_the_button
    start_the_button = tk.Button(frame_start, text="Click here to start the stimulation", command=stimulation)
    start_the_button.pack()

def stimulation():
    start_the_button.destroy() #destroy the "Start stimulation" button
    countdown(3) #countdown function starting at 3s
    second_screen_window.after(3000, fixation_cross) #after 3s display the fixation cross


##########################FIXATION CROSS##########################
### This function creates the fixation cross###
def fixation_cross():
    ###CANVAS###
    # Get the dimensions of the screen
    window_width = second_screen_window.winfo_width()
    window_height = second_screen_window.winfo_height()
    # create canvas
    canvas_width = 900
    canvas_height = 300
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas at the center of the window
    canvas = tk.Canvas(second_screen_window, width=canvas_width, height=canvas_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    # Fixation cross appears for 5 seconds
    def cross_appears():
        canvas.create_text(canvas_width // 2, canvas_height // 2, text=f"+", font=("Calibri", 100))
    second_screen_window.after(1000, cross_appears()) #wait for 1 second to cover the delay from the stimulators
    second_screen_window.after(6000, canvas.destroy) #clear the screen after 5 seconds after the cross appeared
    ##########################SLIDER##########################
    second_screen_window.after(7000,my_slider) # after 6 seconds, display the slider

##########################COUNTDOWN FUNCTION##########################
### this function counts down the seconds###
def countdown(s):
    ###CANVAS###
    # Get the dimensions of the screen
    window_width = second_screen_window.winfo_width()
    window_height = second_screen_window.winfo_height()
    # create canvas
    canvas_width = 2000
    canvas_height = 300
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas at the center of the window
    canvas = tk.Canvas(second_screen_window, width=canvas_width, height=canvas_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    def update_canvas(i):
        canvas.delete("text") #delete the text everytime the remaining time is updated
        #countdown = False
        if i > 0:
            sentence = f"The stimulation will start in {i}s."
            canvas.create_text(canvas_width // 2, canvas_height // 2, text=sentence, font=("Calibri", 50), tag="text")
            second_screen_window.after(1000, update_canvas, i - 1)
        # when the countdown is done, destroy the text canvas and initiate the stimulation
        else:
            canvas.destroy()
    update_canvas(s)

########################## MY_SLIDER FUNCTION ##########################
### this function creates the visual slider AND also the button that calls the "MY_OUTPUT"function###
def my_slider():
    # create frame for the slider
    global frame_slider
    frame_slider = tk.Frame(second_screen_window, width=400, height=500)
    frame_slider.place(anchor='center', relx=0.5, rely=0.55)

    # create canvas with the sentence
    global canvas_question
    window_width = second_screen_window.winfo_width()
    window_height = second_screen_window.winfo_height()
    # create canvas
    canvas_width = 800
    canvas_height = 100
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas at the center of the window
    canvas_question = tk.Canvas(second_screen_window, width=canvas_width, height=canvas_height)
    canvas_question.place(relx=0.5, rely=0.2, anchor="center")
    # Question
    canvas_question.create_text(canvas_width // 2, canvas_height // 2, text=f"Please rate the intensity of the sensation", font=("Calibri", 20))

    # create slider
    global slider
    slider = tk.Scale(frame_slider, from_=10, to=0, length=525, showvalue=0, orient='vertical')
    slider.pack(side='left')

    # Create a picture within the frame
    global image
    image = ImageTk.PhotoImage(Image.open("Scale_ENG.png"))

    # Create a Label Widget to display the picture
    global label
    label = tk.Label(frame_slider, image=image)
    label.pack(side='left')

    # CREATE THE BUTTON (and get the value from the slider)
    global frame_button
    frame_button = tk.Frame(second_screen_window)
    frame_button.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    global next_button
    next_button = tk.Button(frame_button, text="Next", command=second_screen_window.destroy)
    next_button.pack()

##########################################################
########################## CODE ##########################
##########################################################
# Get information about all screens
monitors = get_monitors()

# Check if there is a second screen available

second_monitor = monitors[1]
screen_width = second_monitor.width
screen_height = second_monitor.height

# Create a new Tkinter window
second_screen_window = tk.Tk()


# Position and size the window to fit the second screen and make it fullscreen
second_screen_window.geometry(f"{screen_width}x{screen_height}+{second_monitor.x}+{second_monitor.y}")

    #second_screen_window.attributes("-fullscreen", True)


    # Run the function to start the application
start_button()


second_screen_window.mainloop()