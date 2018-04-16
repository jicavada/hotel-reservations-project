#reservation system for hotels. reads from a database and displays the info for a customer

import datetime
import random
import os
import calendar
from datetime import date
from datetime import datetime
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
                sdate = datetime.strptime(entered_date, '%d-%m-%Y')
                break
            except:
                print("wrong date format")

        while True:
            try:
                entered_date = input("Enter check-out date dd-mm-yyyy:")
                edate = datetime.strptime(entered_date, '%d-%m-%Y')
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
    print("6- Delete booking")
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

def book_a_room(DATABASE):
    '''
    prompt for a hotel and book a room
    '''
    hotel_to_book = get_hotel(DATABASE)
    (sdate, edate) = get_dates()
    insert_booking(DATABASE, sdate, edate, hotel_to_book)
   
   
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
                        sdate DATE, edate DATE, booking_ref INT UNIQUE,
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
        retrieved_hotels = cursor.fetchall()
        
        
        for hotel_row in retrieved_hotels:
            hotels.append(Hotel(name=hotel_row[0], number_of_rooms=hotel_row[1]))
            """
            cursor.execute('''SELECT bookings.date, bookings.room_id FROM bookings 
                            LEFT JOIN hotels ON bookings.hotel_id = hotels.hotel_id 
                            WHERE hotels.name = ? ''', (hotels[-1].name,))
            """
            cursor.execute('''SELECT bookings.date, rooms.room_number FROM bookings 
                            LEFT JOIN hotels ON bookings.hotel_id = hotels.hotel_id 
                            LEFT JOIN rooms ON bookings.room_id = rooms.room_id
                            WHERE hotels.name = ? ''', (hotels[-1].name,))
            date_and_room = cursor.fetchall()
            for date,room in date_and_room:
                date_formatted = datetime.strptime(date, '%Y-%m-%d').date()
                hotels[-1].rooms[room].booked_dates.append(date_formatted)
            
                

        db.close()
    except Exception as e:
        raise e
    
    return hotels

def add_hotel(DATABASE):
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
            db = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            cursor = cursor.execute('''INSERT INTO hotels VALUES(NULL, ?,?)''', (hotel_name, number_of_rooms))
            cursor.execute('''SELECT last_insert_rowid()''')
            hotel_id = int(cursor.fetchone()[0])
            for room_number in range(number_of_rooms):
                cursor.execute('''INSERT INTO rooms VALUES(NULL, ?, ?)''', (hotel_id, room_number))
            db.commit()
            db.close()
            break
    
def see_hotels(DATABASE):
    try:
        
        db = sqlite3.connect(DATABASE)
        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('''SELECT name, hotel_id from hotels''')
        print("Hotel \t Hotel Id")
        for hotel_names, hotel_id  in cursor.fetchall():
            print(hotel_names + '\t' + str(hotel_id))
        db.close()
    except Exception as e:
        db.rollback()
        raise e

def get_hotel(DATABASE):
    try:
        hotel_ids = []
        db = sqlite3.connect(DATABASE)
        # Get a cursor object
        cursor = db.cursor()
        cursor.execute('''SELECT name, hotel_id from hotels''')
        print("Hotel \t Hotel Id")
        for hotel_names, hotel_id  in cursor.fetchall():
            print(hotel_names + '\t' + str(hotel_id))
            hotel_ids.append(hotel_id)
        db.close()
        while True:
            try:
                hotel_selected = int(input("Choose a hotel id: "))
                if hotel_selected not in hotel_ids:
                    continue
                else:
                    return hotel_selected
            except:
                print("invalid input")

    except Exception as e:
        db.rollback()
        raise e

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
                cursor.execute('''SELECT last_insert_rowid()''')
                room_id = int(cursor.fetchone()[0])
                for single_date in room.booked_dates:
                    cursor.execute('''INSERT INTO bookings VALUES(NULL, ?, ?, ?)''', (hotel_id, room_id, single_date))

        
        db.commit()
        db.close()
    except Exception as e:
        raise e        

def view_occupation(hotels):
    '''
    view occupied rooms
    '''
    if len(hotels) == 0:
        print("no hotels available")
        return

    see_hotels(hotels) #show hotels and select one
    
    while True:
        try:
            hotel_number = int(input("Pick a hotel: "))
            selected_hotel = hotels[hotel_number]
            break
        except:
            print("wrong input")
            continue
    for room in selected_hotel.rooms:
        list_of_dates = map(datetime.strftime('%d-%M-%y'),room.booked_dates)
        print(f"Room {room.room_number} occupation: {list_of_dates}")

def insert_booking(DATABASE, sdate, edate, hotel_id):
    '''
    INSERTS BOOKING IN DATABASE
    '''
    sdate = sdate.strftime('%Y-%m-%d')
    edate = edate.strftime('%Y-%m-%d')
    booking_ref = random.randint(1, 10000)
    room_to_book = room_avl_db(DATABASE, hotel_id, sdate, edate)
    if not room_to_book:
        return
    try:
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor = cursor.execute('''INSERT INTO bookings VALUES(NULL, ?, ?, ?, ?, ?)''', (hotel_id, room_to_book, sdate, edate, booking_ref))
        db.commit()
        db.close()
    except:
        db.rollback()
        print("error introducing booking")
            
def see_bookings(DATABASE):
    try:
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        #cursor = cursor.execute('''select * from bookings''')
        cursor = cursor.execute('''
                                SELECT hotels.name, rooms.room_number, bookings.sdate, bookings.edate, bookings.booking_ref
                                FROM bookings 
                                LEFT JOIN hotels 
                                ON bookings.hotel_id = hotels.hotel_id
                                LEFT JOIN rooms 
                                on bookings.room_id = rooms.room_id
                                ''')
        for row in cursor.fetchall():
            print(row)
        db.commit()
        db.close()
    except:
        db.rollback()
        print("error introducing booking")

def delete_booking(DATABASE):
    see_bookings(DATABASE)
    
    try:
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        while True:
            booking_ref = int(input("Enter booking id to delete:"))
            cursor.execute('''DELETE FROM bookings WHERE bookings.booking_ref = ?''', (booking_ref, ))
            db.commit()
            break
    except Exception as e:
        print("error deleteting")
        raise e
    finally:
        db.close()

def room_avl_db(DATABASE, hotel_id, sdate, edate):
    try:
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute('''SELECT room_id FROM rooms WHERE rooms.hotel_id=? AND room_id NOT IN (SELECT room_id FROM bookings
                        WHERE hotel_id = ? AND (
                        (? BETWEEN bookings.sdate AND bookings.edate )
                        OR
                        (? BETWEEN bookings.sdate AND bookings.edate) 
                        OR 
                        (bookings.sdate BETWEEN ? AND ?)))''', (hotel_id, hotel_id, sdate, edate, sdate, edate))
        result = cursor.fetchall()
        return result[0][0]
    except:
        print("no rooms avilable for this hotel in the selected dates")
        return 0
    finally:
        db.close()

#program start

#create a hotel (later to be read from DB)


DATABASE = "hotel_rooms.db"
init_database(DATABASE)


#not needed anymore
#hotels = read_hotels(DATABASE)



menu = True

while menu:

    selection = option_menu()
    if selection == 1:
        book_a_room(DATABASE)
    elif selection == 2:
        see_bookings(DATABASE)
    elif selection == 3:
        add_hotel(DATABASE)
    elif selection == 4:
        see_hotels(DATABASE)
    elif selection == 5:
        delete_hotel(DATABASE)
    elif selection == 6:
        delete_booking(DATABASE)
    else:
        break
