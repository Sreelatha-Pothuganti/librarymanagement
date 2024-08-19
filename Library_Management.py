import mysql.connector

class LibrarySystem:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hareesh",
            database="sreedb"
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                quantity INT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_id INT,
                quantity INT,
                action VARCHAR(10),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')
        self.connection.commit()

    def add_book(self, title, author, quantity):
        self.cursor.execute('''
            INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)
        ''', (title, author, quantity))
        self.connection.commit()
        print(f"'{title}' added to the library inventory.")

    def display_inventory(self):
        self.cursor.execute('''
            SELECT * FROM books
        ''')
        books = self.cursor.fetchall()
        print("\nLibrary Book Inventory:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")

    def update_quantity(self, book_id, quantity_change, action):
        self.cursor.execute('''
            UPDATE books SET quantity = quantity + %s WHERE id = %s
        ''', (quantity_change, book_id))
        self.cursor.execute('''
            INSERT INTO transactions (book_id, quantity, action) VALUES (%s, %s, %s)
        ''', (book_id, quantity_change, action))
        self.connection.commit()

    def borrow_book(self, book_id, quantity):
        self.cursor.execute('''
            SELECT quantity FROM books WHERE id = %s
        ''', (book_id,))
        current_quantity = self.cursor.fetchone()[0]

        if current_quantity >= quantity:
            self.update_quantity(book_id, -quantity, 'borrow')
            print(f"{quantity} copies of book (ID: {book_id}) borrowed successfully.")
        else:
            print("Not enough copies available to borrow.")

    def return_book(self, book_id, quantity):
        self.update_quantity(book_id, quantity, 'return')
        print(f"{quantity} copies of book (ID: {book_id}) returned successfully.")

if __name__ == "__main__":
    library = LibrarySystem()

    while True:
        print("\nLibrary Management System")
        print("1. Add New Book")
        print("2. Display Book Inventory")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            quantity = int(input("Enter quantity: "))
            library.add_book(title, author, quantity)

        elif choice == "2":
            library.display_inventory()

        elif choice == "3":
            book_id = int(input("Enter book ID to borrow: "))
            quantity = int(input("Enter quantity to borrow: "))
            library.borrow_book(book_id, quantity)

        elif choice == "4":
            book_id = int(input("Enter book ID to return: "))
            quantity = int(input("Enter quantity to return: "))
            library.return_book(book_id, quantity)

        elif choice == "5":
            print("Exiting library management system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
