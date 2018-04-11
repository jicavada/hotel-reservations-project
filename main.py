#reservation system for hotels. reads from a database and displays the info for a customer

import datetime
import calendar
from datetime import date
from datetime import timedelta


class Hotel():

    def __init__(self, name, number_of_rooms):
        self.name = name 
        self.number_of_rooms = number_of_rooms
        self.rooms = []
        for room_number in range(number_of_rooms):
            self.rooms.append(Room(room_number))

    def book(self, sdate, edate):
        for room in self.rooms:
            if room.is_available(sdate,edate):
                print("Room number {} is available".format(room.room_number))            
                while True:
                    ok_to_book = input("Do you want to book it? y/n : ")
                    if ok_to_book == 'y':
                        room.book(sdate,edate)
                        return room.room_number 
                    elif ok_to_book == 'n':
                        break
                    else: 
                        print("wrong answer. Answer y or n")
            else:
                print("no more rooms available")

    def see_occupation(self):
        for room in self.rooms:
            print("Room {} is full on {}".format(room.room_number, room.booked_dates))          
        

class Room():

    def __init__(self, room_number):
        self.room_number = room_number
        self.booked_dates = []

    def book(self, sdate, edate):
        '''
        books a room by adding the dates to booked_dates, if the room is free
        '''
        if self.is_available(sdate, edate):
            for single_date in self.daterange(sdate, edate):
                self.booked_dates.append(single_date)
        print(f"Room {self.room_number} booked for selected dates")
        
    
    def is_available(self, sdate, edate):
        '''
        returns True if the room is free during these dates
        uses a date iterator defined below as daterange
        '''
        #return single_date not in self.booked_dates
        for single_date in self.daterange(sdate,edate):
            if single_date in self.booked_dates: #if date in booked dates return false
                return False
        return True

    
    def daterange(self, start_date, end_date):
        '''
        iterator for dates start date to end date
        '''
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)
            

def get_dates():
    '''
    get start and end reservation dates. check for correct format.
    RETURN: (START_DATE, END_DATE)
    '''
    while True:
        while True:
            try:
                entered_date = input("Enter check-in date dd-mm-yyyy:")
                sdate = datetime.datetime.strptime(entered_date, '%d-%m-%Y')
                break
            except:
                print("wrong date format")

        while True:
            try:
                entered_date = input("Enter check-out date dd-mm-yyyy:")
                edate = datetime.datetime.strptime(entered_date, '%d-%m-%Y')
                break
            except:
                print("wrong date format")

        if sdate-edate > timedelta(days=0):
            print("check in date cannot be later than checkout date")
        else:
            return (sdate,edate)


def option_menu():
    '''
    print menu with options and return result
    '''
    print("Menu:")
    print("1- Make reservation")
    print("2- View occupation")
    print("3 -Exit")
    
    while True:
        selection = input("Choose an option: ")
        if selection not in ['1', '2', '3']:
            continue
        else:
            return int(selection)

def ask_yes_or_no(question):
    '''
    ask a question and return True if y, False if n or repeat the question if invalid
    '''
    while True:
            answer = input(question)
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print("Please answer y or n: ")

def book_a_room():
    
    booking = True
    while booking:
        #ask for dates
        (start_date, end_date) = get_dates()
        #manual imput for testing
        #start_date = datetime.date(2018,1,1)
        #end_date = datetime.date(2018,1,3)

        #book room in hotel
        hotel.book(start_date, end_date)
        #ask customer if he wants to book anotoher room, else finish program
        booking = ask_yes_or_no("Do you want to book antoher room? y/n: ")




#program start

#create a hotel (later to be read from DB)
hotel = Hotel(name="Almirante", number_of_rooms=10)



menu = True

while menu:

    selection = option_menu()
    if selection == 1:
        book_a_room()
    elif selection == 2:
        hotel.see_occupation()
    else:
        break
