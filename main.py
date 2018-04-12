#reservation system for hotels. reads from a database and displays the info for a customer

import datetime
import os
import calendar
from datetime import date
from datetime import timedelta
import sqlite3



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
    #os.system("cls")
    print("Menu:")
    print("1- Make reservation")
    print("2- View occupation")
    print("3- Add Hotel")
    print("4- See Hotels")
    print("5- Delete Hotel")
    print("6- Save changes")
    print("7- Exit")
    
    while True:
        selection = input("Choose an option: ")
        if selection not in ['1', '2', '3', '4', '5', '6','7']:
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

def init_database(db_name):
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(DATABASE)
        # Get a cursor object
        cursor = db.cursor()
        # Check if table hotels does not exist and create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                        hotels(hotel_id INTEGER PRIMARY KEY, name TEXT, n_rooms INT)''')
        #create table rooms if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                        rooms(room_id INTEGER PRIMARY KEY, hotel_id INT, room_number INT,
                        CONSTRAINT FK_hotel_id FOREIGN KEY(hotel_id) REFERENCES hotels(hotel_id))''')
        #create table for bookins
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                        bookings(booking_id INTEGER PRIMARY KEY, hotel_id INT, room_id INT,
                        date DATE,
                        CONSTRAINT FK_hotel_id FOREIGN KEY(hotel_id) REFERENCES hotels(hotel_id),
                        CONSTRAINT FK_room_id FOREIGN KEY(room_id) REFERENCES rooms(room_id))''')

        # Commit the change
        db.commit()
        # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()

def read_hotels(DATABASE):
    hotels = []
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(DATABASE)
        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('''SELECT name, n_rooms FROM hotels''')
        for hotel in cursor:
            hotels.append(Hotel(name=hotel[0],number_of_rooms=hotel[1]))
            cursor.execute('''SELECT room_number FROM rooms''')
            for row in cursor:
                hotel.rooms[].room_number = row[0]
                #####fill the rooms and the bookings###

        db.close()
    except Exception as e:
        raise e
    
    return hotels

def add_hotel(hotels):
    while True:
        try:
            hotel_name = input("Enter hotel name: ")
            if hotel_name == '':
                continue
            else:
                number_of_rooms = int(input("Enter number of rooms:"))
        except:
            continue
        else:
            hotels.append(Hotel(hotel_name,number_of_rooms))
            break
    
def see_hotels(hotels):
    if len(hotels) == 0:
        print("No hotels to show")
        return
    counter =0
    for hotel in hotels:
        print(f"{counter}- " + hotel.name)
        counter += 1

def delete_hotel(hotels):
    if len(hotels) == 0:
        print("No hotels to delete")
        return
    while  len(hotels) > 0:
        try:
            see_hotels(hotels)
            hotel_id = int(input("Enter the hotel to delete:"))
            hotels.pop(hotel_id)
            if ask_yes_or_no("Do you want to delete another one? y/n :"):
                continue
            break
        except:
            print("error ocurred while deleting")
        continue
    
def save_to_database(hotels, DATABASE):
    '''save hotels, rooms and bookings store in hotels to db
    '''
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect(DATABASE)
        # Get a cursor object
        cursor = db.cursor()
        #clear tables and rewrite it with updated info
        cursor.execute('''DELETE FROM hotels''')
        cursor.execute('''DELETE FROM rooms''')
        for hotel in hotels:
            cursor.execute('''INSERT INTO hotels VALUES(NULL,?,?)''', (hotel.name, hotel.number_of_rooms))
            cursor.execute('''SELECT last_insert_rowid()''')
            hotel_id = int(cursor.fetchone()[0])
            for room in hotel.rooms:
                cursor.execute('''INSERT INTO rooms VALUES(NULL, ?, ?)''', (hotel_id, room.room_number))
                room_id = cursor.execute('''SELECT last_insert_rowid()''')
                room_id = int(cursor.fetchone()[0])
                for single_date in room.booked_dates:
                    cursor.execute('''INSERT INTO bookings VALUES(NULL, ?, ?, ?)''', (hotel_id, room_id, single_date))

        
        db.commit()
        db.close()
    except Exception as e:
        raise e        


#program start

#create a hotel (later to be read from DB)
hotel = Hotel(name="Almirante", number_of_rooms=10)

DATABASE = "hotel_rooms.db"
init_database(DATABASE)
hotels = read_hotels(DATABASE)



menu = True

while menu:

    selection = option_menu()
    if selection == 1:
        book_a_room()
    elif selection == 2:
        hotel.see_occupation()
    elif selection == 3:
        add_hotel(hotels)
    elif selection == 4:
        see_hotels(hotels)
    elif selection == 5:
        delete_hotel(hotels)
    elif selection == 6:
        save_to_database(hotels, DATABASE)
    else:
        break
