import pandas as pd
import os
from datetime import datetime, timedelta


#Part responsible for books
books_path = "./data/books.xlsx"
books_columns = ["ID", "Title", "Author", "ISBN", "Publisher", "Pages"]

class Book:
    __id = 0

    def __init__(self, title: str, author: str, isbn: int, publisher: str, page_count: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.page_count = page_count

        Book.__id += 1
        self.id = Book.__id

        self.lent_date: datetime.date = None
        self.lent_to: Reader = None
        self.return_date: datetime.date = None
        self.lent = False
        self.reserved = False
        self.reserved_until: datetime.date = datetime.now() # Just to be sure you can check between now and this variable when trying to borrow
        self.reserved_by: Reader = None

    def to_dict(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Author": self.author,
            "ISBN": self.isbn,
            "Publisher": self.publisher,
            "Pages": self.page_count
        }

    @staticmethod
    def from_dict(d):
        book = Book(
            d["Title"],
            d["Author"],
            d["ISBN"],
            d["Publisher"],
            d["Pages"]
        )
        book.id = d["ID"]
        Book.__id = max(Book.__id, d["ID"])  # Ensure unique IDs
        return book

    def __str__(self):
        return f"{self.title} ({self.author}, {self.publisher}, {self.page_count} pages.)"

"""
===== Pandas books =====
"""

def excel_file_preparer():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(books_path):
        df = pd.DataFrame(columns=books_columns)
        df.to_excel(books_path, index=False)

def load_books():
    excel_file_preparer()
    return pd.read_excel(books_path)

def load_books_object():
    df = load_books()
    return [Book.from_dict(row) for _, row in df.iterrows()]

def add_book(book: Book):
    df = load_books()
    new_id = 1 if df.empty else int(df["ID"].max()) + 1
    book.id = new_id
    Book._Book__id = new_id
    df = pd.concat([df,pd.DataFrame([book.to_dict()])], ignore_index=True)
    df.to_excel(books_path, index=False)

def remove_book(book_id: int):
    df = load_books()
    df = df[df["ID"] != book_id]
    df.to_excel(books_path, index=False)


def edit_book(book_id: int, updated_book: Book):
    df = load_books()
    if book_id in df["ID"].values:
        df.loc[df["ID"] == book_id, ["Title", "Author", "ISBN", "Publisher", "Pages"]] = [
            updated_book.title,
            updated_book.author,
            updated_book.isbn,
            updated_book.publisher,
            updated_book.page_count
        ]
        df.to_excel(books_path, index=False)
    else:
        print(f"No book with ID {book_id} found.")


def search_book(query: str):
    df = load_books()
    query = query.lower()
    mask = (
        df["Title"].str.lower().str.contains(query) |
        df["Author"].str.lower().str.contains(query) |
        df["Publisher"].str.lower().str.contains(query) |
        df["ISBN"].astype(str).str.contains(query)
    )
    return df[mask]

# Part responsible for addresses
class Address:
    def __init__(self, city: str, street: str, apartment: int, postal_code: str):
        self.__street = street
        self.__city = city
        self.__postal_code = postal_code
        self.__apartment = apartment

    def __str__(self):
        return f"{self.__city}, {self.__street}, {self.__apartment} {self.postal_code}"

#Part responsible for readers
readers_path = "./data/readers.xlsx"
readers_columns = ["ID", "Name", "Surname", "Phone"]

class InvalidPhoneNumber(Exception):
    """Raised when phone number is invalid."""

class Reader:
    __readerID = 0

    def __init__(self, name: str, surname: str, phone_num: str, address: Address):
    try:
        if not phone_num.isdigit() or len(phone_num) != 9:
            raise InvalidPhoneNumber("Phone number must consist of exactly 9 digits.")
        except InvalidPhoneNumber as e:
            print(e)

        self.name = name
        self.surname = surname
        self.phone_num = phone_num
        Reader.__readerID += 1
        self.__id = Reader.__readerID
        self.borrowed_books: list[Book] = []

        self.past_borrowed: dict[Book, list[datetime.date]] = {}
        self.past_returned: dict[Book, list[datetime.date]] = {}
        self.past_extended: dict[Book, list[datetime.date]] = {}
        self.past_reserved: dict[Book, list[datetime.date]] = {}

    def getID(self):
        return self.__id

    def borrow(self, book: Book):
        now = datetime.now()

        if ((not book.reserved_until < now) or book.reserved_by == self):
            if not book.lent:
                self.borrowed_books.append(book)

                # Either create the list or append to the existing one
                if book in self.past_borrowed:
                        self.past_borrowed[book].append(now())
                else:
                    self.past_borrowed[book] = [now()]

                book.lent = True
                book.lent_date = now
                book.return_date = now + timedelta(days=30)
            else:
                return "Can't borrow already lent book."
        else:
            return: "Book lent and reserved by someone else"

    def return_book(self, book: Book):
        now = datetime.now()
        date_until_fee = book.return_date
        fee = 0

        if now > date_until_fee:
            difference = (now - date_until_fee).days
            fee = 0.5 * difference

        # Either create the list or append to the existing one
        if book in self.past_returned:
                self.past_returned[book].append(now)
        else:
            self.past_returned[book] = [now]

        self.borrowed_books.remove(book)

        book.borrowed = False
        book.lent_date = None

        if book.reserved == True and book.reserved_by == self:
            book.reserved = False
            book.reserved_by = None

        return fee
        
    def extend(self, book: Book):
        if not book.borrowed:
            return "Can't extend book that hasn't been lent"

        if not book.lent_to == self:
            return "Can't extend book lent by someone else"

        # Either create the list or append to the existing one
        if not book.reserved:
            if book in self.past_extended:
                    self.past_extended[book].append(datetime.now())
            else:
                self.past_extended[book] = [datetime.now()]
            book.return_date += timedelta(days=30)

            return f"Extended the return date, new return date: {book.return_date}"
        else:
            return "Can't extend - book reserved by someone"

    def reserve(self, book: Book):
        now = datetime.now()

        if not book.reserved:
            book.reserved_until = book.return_date + timedelta(days=7)
            book.reserved_by = self

            # Either create the list or append to the existing one
            if book in self.past_borrowed:
                    self.past_reserved[book].append(datetime.now())
            else:
                self.past_reserved[book] = [datetime.now()]
        else:
            return "can't reserve book - already reserved"

    def to_dict(self):
        return {
            "ID": self.__id,
            "Name": self.name,
            "Surname": self.surname,
            "Phone": self.phone_num
        }

    @staticmethod
    def from_dict(d):
        reader = Reader(d["Name"], d["Surname"], str(d["Phone"]))
        reader.__id = d["ID"]
        Reader.__readerID = max(Reader.__readerID, d["ID"])
        return reader

"""
===== Pandas readers =====
"""

def prepare_readers_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(readers_path):
        df = pd.DataFrame(columns=readers_columns)
        df.to_excel(readers_path, index=False)

def load_readers():
    prepare_readers_file()
    return pd.read_excel(readers_path)

def load_readers_object():
    df = load_readers()
    return [Reader.from_dict(row) for _, row in df.iterrows()]

def add_reader(reader: Reader):
    df = load_readers()
    new_id = 1 if df.empty else int(df["ID"].max()) + 1
    reader.__id = new_id
    Reader._Reader__readerID = new_id
    df = pd.concat([df, pd.DataFrame([reader.to_dict()])], ignore_index=True)
    df.to_excel(readers_path, index=False)

def remove_reader(reader_id: int):
    df = load_readers()
    df = df[df["ID"] != reader_id]
    df.to_excel(readers_path, index=False)

def edit_reader(reader_id: int, updated_reader: Reader):
    df = load_readers()
    if reader_id in df["ID"].values:
        df.loc[df["ID"] == reader_id, ["Name", "Surname", "Phone"]] = [
            updated_reader.name,
            updated_reader.surname,
            updated_reader.phone_num
        ]
        df.to_excel(readers_path, index=False)
    else:
        return(f"No reader with ID {reader_id}.")

def search_reader(query: str):
    df = load_readers()
    query = query.lower()
    mask = (
        df["Name"].str.lower().str.contains(query) |
        df["Surname"].str.lower().str.contains(query) |
        df["Phone"].astype(str).str.contains(query)
    )
    return df[mask]

# Library database
class Library:
    def __init__(self):
        self.readers: list[Reader] = []
        self.books: list[Book] = []

    def show_available_books(self) -> list[Book]:
        books = self.books

        for book in books:
            if not book.lent and not book.reserved:
                available_books.append(book)
        return available_books

    def show_lent_books(self) -> list[Book]:
        books = self.books

        for book in books:
            if book.lent:
                lent_books.append(book)
        return lent_books
    
    def objects_from_excel(self, path: str, objects: list) -> list:
        try:
            if not os.path.isfile(path):
                raise FileNotFoundError
        except FileNotFoundError as e:
            print(e)
            df = pd.read_excel(path)
            for index, row in df.iterrows():
                row_dict = row.to_dict()
                objects.append(row_dict)

            return objects


    def readers_from_excel(self, path):
        self.objects_from_excel(path, self.readers)

    def books_from_excel(self, path):
        self.objects_from_excel(path, self.books)

