import random
from openpyxl import Workbook


def random_order(participant_id, my_list):

    # Create a new workbook in excel
    wb = Workbook()
    ws = wb.active

    # Shuffle the list randomly
    random.shuffle(my_list)

    # Print the random order of items
    print("Random order of the items is:")
    for i, item in enumerate(my_list, start=1):
        print(f"Day {i}. {item}")
        ws.append([f"Day {i}.: {item}"])
    filename = f"Participant {participant_id}_sessionsorder.xlsx"
    wb.save(filename)


# my list
my_list = ["cymba conchae", "earlobe", "scapha"]

# Ask for participants ID:
participant_id = input("Participant ID: ")

random_order(participant_id, my_list)