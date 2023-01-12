# importing SQLite 3 module
import sqlite3

# creates a db called ebook store
db = sqlite3.connect('ebookstore')

# getting a cursor object
cursor = db.cursor()

# checks if a table exists called books and if not it creates it
cursor.execute('''CREATE TABLE IF NOT EXISTS
                books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)''')

# function allowing user to enter data about a book and add it to the database
def capture_books():
    try:
        # getting user input for each variable in the list
        id = int(input("\nPlease enter a id number for this book: \n"))

        # code to check if ID already exists
        cursor.execute("SELECT id FROM books where id = ?", (id,))
        if cursor.fetchone() is not None:
            raise ValueError("This id already exists in the database.")

        title = str(input("\nPlease enter the Title for this book: \n"))
        author = str(input("\nPlease enter the Author of this book: \n"))
        qty = int(input("\nPlease enter the quantity of this book: \n"))

        # inserting data into table
        cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                       VALUES(?,?,?,?)''', (id,title,author,qty))
        # sucessful print message
        print("Book Added Sucessfully.")
        # commits the changes
        db.commit()
    except sqlite3.Error as e:
        print(f"An error has occured: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")
    

# function to view everything in the database
def view_all():
    # if database is empty
    if not db:
        print("The database is empty!")
    else:
        cursor.execute('''SELECT id, Title, Author, Qty FROM books''')
        for row in cursor:
            print(f'\nid: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}')

# function to search for books by name
def search_book():
    id = int(input("Please Enter the ID of the book you would like to search for: "))
    cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id = ?''', (id,))
    for row in cursor:
            print(f'\nid: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}')


# function to update a book in the DB
def update_book():
    try:
        # creating a var that stores user choice to see what they want to update
        choice = int(input("What would you like to update - \nEnter 1 for Book ID.\nEnter 2 for Book Title.\nEnter 3 for Book Author.\nEnter 4 for Book Quantity.: \n"))
        # if statement to execute different code depending on input
        if choice == 1:
            id = str(input("Enter the current ID of the book you would like to amend: "))
            new_id = int(input("Enter a new ID: "))

            # code to check if new id already exists
            cursor.execute("SELECT id FROM books WHERE id = ?", (new_id,))
            if cursor.fetchone() is not None:
                raise ValueError("This id already exists in the database.")
            
            # this code updates the id   
            cursor.execute('''UPDATE books SET id = ? WHERE id = ?''', (new_id, id))
        elif choice == 2:
            id = str(input("Enter the current ID of the book you would like to amend: "))
            new_title = str(input("What would you like to change the title too: "))
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (new_title, id))
        elif choice == 3:
            id = str(input("Enter the current ID of the book you would like to amend: "))
            new_author = str(input("What would you like to change the Author name too: "))
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (new_author, id))
        elif choice == 4:
            id = str(input("Enter the current ID of the book you would like to amend: "))
            new_qty = int(input("What would you like to change the quantity too: "))
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_qty, id))
        else:
            print("Please choose a valid choice!")
        # commits the changes
        db.commit()
    except sqlite3.Error as e:
        print(f"An error has occured: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")



# function to delete a book
def delete_book():
    try:
        # asks user to input id of book they want to delete
        id = int(input("Please enter the ID of the book you would like to delete: "))
        cursor.execute('''DELETE FROM books WHERE id = ?''', (id,))
        # commits the changes
        db.commit()
    except sqlite3.Error as e:
        print(f"An error has occured: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")


        

#==========Main Menu=============

# function for main menu - i will use a while loop and dictionary to map the users input to the functions i created
def main_menu():

    # dictionary called options with all of the user options
    options = {
        "1": capture_books,
        "2": update_book,
        "3": delete_book,
        "4": search_book,
        "5": view_all,
        "6": exit
    }

    # while the dictionary is true it will print a list of options for the user and let them pick one - when they input a number it will correspond to a function
    while True:
        print("""
        Bookstore Inventory Management System
        1. Add Book data to the database
        2. Update a Book
        3. Delete a Book
        4. Search for a Book
        5. View all Books
        6. Exit
        """)
        # allows user to input their choice
        choice = str(input("\nEnter an option: \n"))
        # try except that maps user input to the above dictionary
        try:
            #
                options[choice]()

                if options[6]:
                    db.close()
        # excepts key errors of wrong input and prints appropriate message
        except KeyError:
            print("\nPlease choose a valid option!\n")

# runs the main menu function to initiate the program
main_menu()


