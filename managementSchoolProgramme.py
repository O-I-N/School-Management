import sys 
from time import strftime, gmtime

PARTECIPANTS = "./partecipants.txt"
TIMETABLE = "./timetable.txt"

def timeNow(date=None):
    if date == strftime("%Y_%m_%d", gmtime()):
        return strftime("%H:%M", gmtime())
    else:
        return strftime("/%Y_%m_%d/%H:%M", gmtime())


def FindName(name, file_name):
    with open(file_name, "r") as ft:
        raws = ft.readlines()
    for index,raw in enumerate(raws):
        raw = raw.split(";")
        if name == raw[0]:
            return index
    return "no presence"
    
def SearchPeople(name):
    if FindName(name, PARTECIPANTS) == "no presence":
        return name + " is not inside the school"
    else:
        return f"{name} is inside the school at the moment"


def UpdateFile(file_name, rawList):
	with open(file_name, "w") as ft:
		for raw in rawList:
			ft.write(f"{raw}")

def Copy_Paste(name, index, file1, file2):
	with open(file1, "r") as ft:
		raws = ft.readlines()
	copy = raws.pop(index)
	date=copy.split("/")[-2] #return last date
	UpdateFile(file1, raws)
	if file1 == PARTECIPANTS:
            paste = copy[:-1] + "-" + timeNow(date) + "\n"
	else:
            paste = copy[:-1] + "; " + timeNow(date) + "\n"
	with open(file2, "a") as ft:
		ft.write(paste)


def InsertName(name):
    if FindName(name, PARTECIPANTS) != "no presence":
        return (f"{name} has already entered")
        
    elif FindName(name, TIMETABLE) != "no presence":
        index = FindName(name, TIMETABLE)
        Copy_Paste(name, index, TIMETABLE, PARTECIPANTS)
        return "Well done, we have inserted a student"
    else:
        with open(PARTECIPANTS, "a") as f:
            f.write(f"{name}; {timeNow()}\n")
        return "Well done, we have inserted a student"
            
def ExitName(name):
    if FindName(name, PARTECIPANTS) == "no presence":
        return (f"{name} has never entered")
    else:
        index = FindName(name, PARTECIPANTS)
        Copy_Paste(name, index, PARTECIPANTS, TIMETABLE)
        return f"We have removed {name} succesfully"
	
def Name():
	name = input("insert name and surname ")
	return name.lower().strip() 


def Number_of_people():
	with open(PARTECIPANTS, "r") as f:
		NoP = len(f.readlines())
	return (f"in this moment there are {NoP} people in the school")


def SendFiles():
	return PARTECIPANTS,TIMETABLE



