# import the packages
import tkinter as tk
from PIL import ImageTk, Image
from statistics import mean
import requests
import openpyxl
import pandas as pd
from screeninfo import get_monitors


##########################STIM_ON FUNCTION##########################

################## URL #######################################
url = 'http://localhost:51523/tvnsmanager/'

###Function sending requests to the software###
def stim_on(intensity):
    def stop_treatment(): #create a separate function to stop the treatment
        response = requests.post(url, data='stopTreatment')
    # commands to send the post request to initiate the stimulation#
    response = requests.post(url,data=f'minIntensity={intensity}&maxIntensity={intensity}&impulseDuration=250&frequency=25&stimulationDuration=5&pauseDuration=0')
    response = requests.post(url, data='manualSwitch')
    response = requests.post(url, data='startTreatment')
    screen.after(5000, stop_treatment) #stop the treatment after 5 seconds


##########################STIMULATION FUNCTION##########################
### This function puts the countdown and the fixation cross together###
def stimulation():
    start_the_button.destroy() #destroy the "Start stimulation" button
    countdown(3) #countdown function starting at 3s
    screen.after(3000, fixation_cross) #after 3s display the fixation cross

########################## GET_PARTICIPANT'SID FUNCTION ##########################
### Function to retrieve the participant's ID ###
def get_participantID():
    global participant_ID
    participant_ID = entry.get() # get the output from the widget
    print("Participant's ID: ", participant_ID)
    frame_participantID.destroy() # destroy the widget
    start_button()  # once they click on "OK", the start button appears

### Function to create the widget of participant's ID ###
def widget_ID():
    # Create a frame to contain the widgets
    global frame_participantID
    frame_participantID = tk.Frame(screen)
    frame_participantID.place(relx=0.5, rely=0.5, anchor="center")

    # Create a label widget to display instructions
    label_ID = tk.Label(frame_participantID, text="Participant's ID:")
    label_ID.pack(pady=5)

    # Create an entry widget for the participant to enter their ID
    global entry
    entry = tk.Entry(frame_participantID)
    entry.pack(pady=5)

    # Create a button to submit the participant ID
    OK_button = tk.Button(frame_participantID, text="OK", command=get_participantID)
    OK_button.pack(pady=5)

########################## START_BUTTON ##########################
def start_button():
    # create frame for the button
    global frame
    frame_start = tk.Frame(screen, width=200, height=100)
    frame_start.place(anchor='center', relx=0.5, rely=0.5)
    global start_the_button
    start_the_button = tk.Button(frame_start, text="Click here to start the stimulation", command=stimulation)
    start_the_button.pack()


##########################COUNTDOWN FUNCTION##########################
### this function counts down the seconds###
def countdown(s):
    ###CANVAS###
    # Get the dimensions of the screen
    window_width = screen.winfo_width()
    window_height = screen.winfo_height()
    # create canvas
    canvas_width = 2000
    canvas_height = 300
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas at the center of the window
    canvas = tk.Canvas(screen, width=canvas_width, height=canvas_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    def update_canvas(i):
        canvas.delete("text") #delete the text everytime the remaining time is updated
        #countdown = False
        if i > 0:
            sentence = f"The stimulation will start in {i}s."
            canvas.create_text(canvas_width // 2, canvas_height // 2, text=sentence, font=("Calibri", 50), tag="text")
            screen.after(1000, update_canvas, i - 1)
        # when the countdown is done, destroy the text canvas and initiate the stimulation
        else:
            canvas.destroy()
            stim_on(intensity)
    update_canvas(s)

##########################FIXATION CROSS##########################
### This function creates the fixation cross###
def fixation_cross():
    ###CANVAS###
    # Get the dimensions of the screen
    window_width = screen.winfo_width()
    window_height = screen.winfo_height()
    # create canvas
    canvas_width = 900
    canvas_height = 300
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas at the center of the window
    canvas = tk.Canvas(screen, width=canvas_width, height=canvas_height)
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    # Fixation cross appears for 5 seconds
    def cross_appears():
        canvas.create_text(canvas_width // 2, canvas_height // 2, text=f"+", font=("Calibri", 100))
    screen.after(1000, cross_appears()) #wait for 1 second to cover the delay from the stimulators
    screen.after(6000, canvas.destroy) #clear the screen after 5 seconds after the cross appeared
    ##########################SLIDER##########################
    screen.after(7000,my_slider) # after 6 seconds, display the slider

########################## MY_SLIDER FUNCTION ##########################
### this function creates the visual slider AND also the button that calls the "MY_OUTPUT"function###
def my_slider():
    # create frame for the slider
    global frame_slider
    frame_slider = tk.Frame(screen, width=400, height=500)
    frame_slider.place(anchor='center', relx=0.5, rely=0.55)

    # create canvas with the sentence
    global canvas_question
    window_width = screen.winfo_width()
    window_height = screen.winfo_height()
    # create canvas
    canvas_width = 800
    canvas_height = 100
    # Calculate the center coordinates for canvas
    x = (window_width - canvas_width) / 2
    y = (window_height - canvas_height) / 2
    # Place the canvas at the center of the window
    canvas_question = tk.Canvas(screen, width=canvas_width, height=canvas_height)
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
    frame_button = tk.Frame(screen)
    frame_button.pack(side=tk.BOTTOM, fill=tk.X, pady=100)
    global next_button
    next_button = tk.Button(frame_button, text="Next", command=my_output)
    next_button.pack()
########################## MY_OUTPUT FUNCTION ##########################
# function to retrieve the values from slider
# and to control increase or decrease of the stimulation
def my_output():
    global slider_value
    global intensity
    global selected_intensity
    slider_value = slider.get()  # get output from the slider
    list_output.append(slider_value)  # add all the slider values to the list_output
    list_intensity.append(intensity)  # add the updated intensity to the list
    Exclude = False # by default
    if intensity < 100 or intensity >= 4000: #if the intensity is below 100, or above 4000 stop the program
        Exclude = True # do not run any further action
        screen.destroy() #stop the program
        if len(list_wanted)>0:
            selected_intensity = mean(list_wanted)
            print("The selected intensity is:", selected_intensity) #print selected intensity
        else:
            selected_intensity=0
        print(list_intensity, list_output, list_wanted)  # print my lists
        create_excel()
    if Exclude == False: # if the intensity is higher than 100 and lower than 4000
        if slider_value in [0, 1, 2, 3, 4, 5, 6]: #if these values selected, always increase
            inc_dec("inc") # increase
        elif slider_value in [9, 10]: #if these values selected, always decrease
            inc_dec("dec") # decrease
        elif slider_value ==7: #only if 7 is chosen
            if len(list_intensity) < 2:  # if the list of intensities doesn't have at least 2 value (can happen at the beginning)
                inc_dec("inc") # increase
            else:
                last_intensity = list_intensity[-1]  # the last value in the list
                before_last_intensity = list_intensity[-2]  # the second last value in the list
                if before_last_intensity > last_intensity:  # if we are decreasing, keep decreasing
                    inc_dec("dec") # decrease
                elif before_last_intensity < last_intensity:  # if we are increasing, keep increasing
                    inc_dec("inc") # increase
        elif slider_value==8: #only if 8 is chosen
            list_wanted.append(intensity)  # add values to the list
            if len(list_intensity) <= 2:  # if the list doesn't have at least 2 value (can happen at the beginning)
                inc_dec("inc") # increase
            else:
                last_intensity = list_intensity[-1]  # the last value in the list
                before_last_intensity = list_intensity[-2]  # the second last value in the list
                if before_last_intensity > last_intensity:  # if we are decreasing, keep decreasing
                    inc_dec("dec") # decrease
                elif before_last_intensity < last_intensity:  # if we are increasing, keep increasing
                    inc_dec("inc") # increase
    return Exclude #return Exclude for this condition (intensity < 100 or intensity >= 4000)

########################## CHECK_FOR FUNCTION ##########################
###function to save the intensities that correspond to certain value on the slider###
###to add these intensities to a new list###
### this function is not being used in this code###
###and to calculate the average value + to stop the program once there are 4 values in the list###
def check_for(value):
    global selected_intensity
    Finish = False #start with false by default
    if slider_value == value:
        list_wanted.append(intensity) # add values to the list
        if len(list_wanted) == 4: # if there are 4 values in the list
            Finish = True  # stop running if there are 4 values in the list
            selected_intensity = mean(list_wanted)# calculate the average of the values in the list
            list_action.append("end")
            screen.destroy() #stop the program
            print(list_intensity, list_output, list_wanted, list_action) # print all my lists
            print("The selected intensity is:", selected_intensity)  # print the selected intensity
            create_excel() # create excel file
    return Finish # if the Finish = True, don't perform any further actions

########################## INC_DEC FUNCTION ##########################
def inc_dec(change):
    global selected_intensity
    global intensity
    Finish = False # by default
    if change == "inc": #if the argument of the function is to increase
        intensity += 100 # increase intensity by 100
        list_action.append("I") # add action of increase to the list of actions
    elif change == "dec": #if the argument of the function is to decrease
        intensity -= 100 # decrease intensity by 100
        list_action.append("D") # add action of decrease to the list of actions
    register_change()  # register whether there is a change from inc to dec or from dec to inc
    if list_change.count(1) == 4: # if there have been 4 changes already
        Finish = True  # stop running the program
        screen.destroy()  # stop the program
        if len(list_wanted) == 4:  # if there are 4 values in the list
            selected_intensity = mean(list_wanted)  # calculate the average of the values in the list
            create_excel()
        else:
            calculate_missing_intensity(list_output, list_intensity) # call the function "calculate_missing_intensity"
            selected_intensity = mean(list_wanted)# calculate the average of the intensities
            create_excel()
        # print all my lists
        print(f"list_intensity:", list_intensity)
        print(f"list_output:", list_output)
        print(f"list_action:", list_action)
        print("list_change:", list_change)
        print(f"list_wanted:", list_wanted)
        print("The selected intensity is:", selected_intensity)
    else: # if there have not been 4 changes, continue
        frame_slider.destroy() #delete the frame
        frame_button.destroy()  #delete the button
        canvas_question.destroy() #delete the question
        start_button() #start again
    return Finish  # if Finish = True, don't perform any further actions

########################## REGISTER_CHANGE FUNCTION ##########################
def register_change():
    if len(list_action) < 2: #if there have been less than 2 actions (meaning that for sure there can be a change from increase to decrease)
        list_change.append(0) # add 0 to the list of change (0 = no change)
    else: # if there have been at least 2 actions
        last_action = list_action[-1]  # the last value in the list of actions
        before_last_action = list_action[-2]  # the second last value in the list of actions
        if last_action != before_last_action: # if the second last value and the last value are not the same
            list_change.append(1) # add 1 to the list of change (1 = change)
        else: # if the last two actions are the same
            list_change.append(0) # add 0 to the list of change, because there was no change

####################################################
############CALCULATE_MISSING_INTENSITY#############
####################################################

def calculate_missing_intensity(list_output, list_intensity):

    # dictionary saving lists for all the skipped pairs
    all_skipped = {
        'intensity_start(Y1)': list_intensities_for_start,
        'start(X1)': list_start_values,
        'skipped(X_new)': list_skipped_values,
        'end(X2)': list_end_values,
        'intensity_end(Y2)': list_intensities_for_end
    }

    ############ FIND_SKIPPED_PAIRS############
    def find_skipped_pairs(numbers):
        for i in range(len(numbers) - 1):  # check for every number besides the last number in the list
            if ((abs(numbers[i] - numbers[i + 1])) > 1
                    # Subtract the consecutive numbers and take their absolute value.
                    # If the difference between these two numbers is larger than 1
                    # it means that some value on the slider was skipped
                    and (numbers[i] != 8)  # we don't want 8
                    and (numbers[i + 1] != 8)  # we don't want 8
                    and ((numbers[i] > 8) or (numbers[i + 1] > 8))):  # at lest one of these numbers must be 8 to be sure that 8 was skipped
                skipped_pairs.append((numbers[i], numbers[i + 1]))  # add these numbers as a pair to the list
                list_intensities_for_start.append(list_intensity[i])
                list_intensities_for_end.append(list_intensity[i + 1])
        return skipped_pairs


    wanted_pairs = find_skipped_pairs(list_output)  # find skipped pairs in the list_output
    print("Skipped pairs:")
    print(wanted_pairs)  # print the list with skipped pairs


    for pair_num, pair in enumerate(wanted_pairs, start=1):  # goes through each element in the skipped_pairs list
        ##pair_num is an index for each element and it starts at 1 (start = 1)
        start, end = pair  # unpacks the pair of numbers into two variables - start and end
        skipped_numbers = [num for num in range(min(start, end) + 1, max(start, end))
                           # creates the list with missing numbers
                           if num not in pair]
        list_start_values.append(start)  # add the start values to the list
        list_skipped_values.append(skipped_numbers)  # add the skipped numbers to the list
        list_end_values.append(end)  # add the end values to the list
        print(f"Pair {pair_num}: {pair}")  # prints the pair_num and the corresponding pair



    df = pd.DataFrame(all_skipped)  # create a table from the lists
    print("DataFrame:")
    print(df)

    for index, row in df.iterrows():  # calculate the equations
        y1, x1, x_new, x2, y2 = row  # define x1, x2, y1, y2
        new_x = 8  # define new x

        a = (y2 - y1) / (x2 - x1)  # Solve equations for a and b
        b = y1 - a * x1
        # Calculate the new y
        new_y = a * new_x + b  # Calculate the new intensity (new y, if x=8)
        list_wanted.append(new_y)
        print(f"For x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        print(f"{x1}a + b = {y1}")
        print(f"{x2}a + b = {y2}")
        print(f"For the new x = {new_x}, y = {new_y}")

##########################CREATING EXCEL FUNCTION##########################
def create_excel():
    # create data frame 1
    data = {
        'intensity': list_intensity,
        'slider': list_output,
        'action': list_action,
        'intense but not painful': list_wanted,
        '': " ",
        'selected intensity': selected_intensity,
        ' ': " ",
        'intensity_start(Y1)': list_intensities_for_start,
        'start(X1)': list_start_values,
        'skipped(X_new)': list_skipped_values,
        'end(X2)': list_end_values,
        'intensity_end(Y2)': list_intensities_for_end
    }

    # create data frame 2
    data_skipped_values = {
        'intensity_start(Y1)': list_intensities_for_start,
        'start(X1)': list_start_values,
        'skipped(X_new)': list_skipped_values,
        'end(X2)': list_end_values,
        'intensity_end(Y2)': list_intensities_for_end
    }

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    # Select the default sheet
    sheet = workbook.active

    file_name = f"{participant_ID}_data.xlsx"  # the name of the file is the participant's ID

    # Create DataFrame with NaN for missing values
    df = pd.DataFrame({key: pd.Series(value) for key, value in data.items()})
    df.to_excel(file_name, index=False)


##########################################################
########################## CODE ##########################
##########################################################

#create a list for all the ratings
list_output=[]
#create a list for rating=80
list_wanted=[]
#create a list for intensities
list_intensity=[]
#create a list for inc_dec
list_action=[]
#create a list for change
list_change=[]

# create lists saving values for all the skipped pairs
list_start_values = []
list_end_values = []
list_skipped_values = []
list_intensities_for_start = []
list_intensities_for_end = []

# create a list for skipped pairs
skipped_pairs = []


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

# intensity by default
intensity=100


########################## RUN THIS FUNCTION ##########################
widget_ID()




# this needs to be here to run the screen
screen.mainloop()


