# Capstone Project Database.
# Importing sqlite3.
import sqlite3

# Function to create the database and table if it does not exist.
def create_database_and_table():
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS book
                 (id INTEGER PRIMARY KEY,
                 title TEXT,
                 author TEXT,
                 quantity INTEGER)''')
    db.commit()
    db.close()


# Function to populate the table with initial values.
def populate_initial_values():
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    initial_values = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    # Inserting book id, title, author and quantity into the database.
    cursor.executemany('INSERT INTO book VALUES (?, ?, ?, ?)', initial_values)
    db.commit()
    db.close()


# Function to add a new book to the database.
def add_new_book():
    title = True
    title = input('\nPlease enter the book title: ')
    author = input('Please enter the name of the author: ')
    while True:
        try:
            quantity = int(input('Please enter the quantity of books: '))
            break
        except ValueError:
            print('\nInvalid input. Please enter a valid number.')
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    cursor.execute('INSERT INTO book (title, author, quantity) VALUES (?, ?, ?)', (title, author, quantity))
    db.commit()
    db.close()
    print(f'\nBook has successfully been added. ({title}).')


# Function to update book information.
def update_book():
    try:
        book_id = int(input('\nPlease enter the book ID you wish to update: '))
    except ValueError:
        print('\nInvalid input. Please enter a valid book ID (a number ID).')
        print('(You can search for a book number ID at the \'search for books\' option).')
        return
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    # Check if the book with the provided ID exists.
    cursor.execute('SELECT * FROM book WHERE id=?', (book_id,))
    existing_book = cursor.fetchone()
    if existing_book is None:
        print(f'\nBook with ID ({book_id}) has not been found.')
        print('(You can search for available book number ID at the \'search for books\' option).')
        db.close()
        return

    # If book is in the database, proceed with updating it.
    title = input('\nPlease enter the new book title (leave empty if you wish to keep current title): ')
    author = input('Please enter new author name (leave empty if you wish to keep current author): ')
    quantity = input('Please enter the new quantity (leave empty if you wish to keep current quantity): ')

    # Checking if all the fields are left empty, if so, inform the user and return without updating.
    if not any([title, author, quantity]):
        print("\nYou have chosen not to update any fields.")
        db.close()
        return

    # Updating data with new values if user has provided them.
    updated_data = {}
    if title:
        updated_data['title'] = title
    if author:
        updated_data['author'] = author
    if quantity:
        try:
            updated_data['quantity'] = int(quantity)
        except ValueError:
            print('\nInvalid input. You have not entered a valid quantity.')
            db.close()
            return

    # Updating the record.
    update_record = 'UPDATE book SET '
    update_values = []
    for key, value in updated_data.items():
        update_record += f'{key}=?, '
        update_values.append(value)
    update_record = update_record.rstrip(', ') + ' WHERE id=?'
    update_values.append(book_id)

    cursor.execute(update_record, tuple(update_values))
    db.commit()
    db.close()

    print(f'\nBook information has been updated successfully for (ID: {book_id}).')


# Function to delete a book from the database.
def delete_book():
    try:
        book_id = int(input('\nPlease enter book ID you wish to delete: '))
    except ValueError:
        print('\nInvalid input. Please enter a valid book ID (a number ID).')
        print('(You can search for a book number ID at the \'search for books\' option).')
        return
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM book WHERE id=?', (book_id,))
    book = cursor.fetchone()
    if book is None:
        print(f'\nBook with ID ({book_id}) has not been found.')
        print('(You can search for available book number ID at the \'search for books\' option).')
    else:
        # To have the title of the book saved to show the user once book deleted.
        title = book[1]
        cursor.execute('DELETE FROM book WHERE id=?', (book_id,))
        db.commit()
        print(f'\nBook (ID: {book_id}) - \'{title}\' has been deleted successfully.')
    db.close()


# Function to search for a book in the database.
def search_books():
    keyword = input('\nPlease enter book id, book title or book author you wish to search: ')
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM book WHERE id LIKE ? OR title LIKE ? OR author LIKE ?', ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))
    books = cursor.fetchall()
    if books:
        print('\nHere are the search Results:')
        for book in books:
            print(book)
    else:
        print('\nThere are no matching books found.')
    db.close()



# Main function to display menu and execute user's choice.
def main():
    create_database_and_table()
    populate_initial_values()
    while True:
        print('\nMenu:')
        print('\n1. Enter new book.')
        print('2. Update book.')
        print('3. Delete book.')
        print('4. Search for books.')
        print('0. Exit')
        choice = input('\nPlease enter your choice: ')
        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '0':
            print('\nThank you for using the ebookstore program, have a great day!\n')
            break
        else:
            print('\nInvalid choice, please try again.')
            print('(Options 1, 2, 3, 4 or 0.)')

print('\nWelcome!')
main()
