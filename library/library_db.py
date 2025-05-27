import os
from datetime import datetime, timedelta
import pandas as pd

from library.address import Address
from library.exceptions import InvalidPhoneNumber


#Part responsible for books
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
        self.lent_to: Reader | None = None
        self.return_date: datetime.date = None
        self.lent = False
        self.reserved = False
        self.reserved_until: datetime.date = datetime.now()
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



class Reader:
    __readerID = 0

    def __init__(self, name: str, surname: str, phone_num: str, address: Address = None):
        if not phone_num.isdigit() or len(phone_num) != 9:
            raise InvalidPhoneNumber("Phone number must consist of exactly 9 digits.")

        self.name = name
        self.surname = surname
        self.phone_num = phone_num
        self.address = address
        Reader.__readerID += 1
        self.__id = Reader.__readerID
        self.borrowed_books: list[Book] = []

        self.past_borrowed: dict[Book, list[datetime]] = {}
        self.past_returned: dict[Book, list[datetime]] = {}
        self.past_extended: dict[Book, list[datetime]] = {}
        self.past_reserved: dict[Book, list[datetime]] = {}

    @property
    def id(self):
        return self.__id

    def borrow(self, book: Book):
        now = datetime.now()
        if ((not book.reserved_until < now) or book.reserved_by == self):
            if not book.lent:
                self.borrowed_books.append(book)
                if book in self.past_borrowed:
                        self.past_borrowed[book].append(now())
                else:
                    self.past_borrowed[book] = [now()]

                book.lent = True
                book.lent_to = self
                book.lent_date = now
                book.return_date = now + timedelta(days=30)
                # Either create the list or append to the existing one
                if book in self.past_borrowed:
                    self.past_borrowed[book].append(now)
                else:
                    self.past_borrowed[book] = [now]

                if book.reserved_by == self:
                    book.reserved = False
                    book.reserved_by = None

                book.lent = True
                book.lent_date = now
                book.return_date = now + timedelta(days=30)

            else:
                raise BookLentToSomeone("Can't borrow already lent book.")
        else:
            raise BookReserved("Book reserved by someone else")

    def return_book(self, book: Book):
        now = datetime.now()
        date_until_fee = book.return_date
        fee = 0

        if now > date_until_fee:
            fee = 0.5 * (now - date_until_fee).days

        # Either create the list or append to the existing one
        if book in self.past_returned:
                self.past_returned[book].append(now)
        else:
            self.past_returned[book] = [now]

        self.borrowed_books.remove(book)

        book.lent = False
        book.lent_date = None
        book.lent_to = None
        book.return_date = None

        if book.reserved and book.reserved_by == self:
            book.reserved = False
            book.reserved_by = None

        return fee

    def extend(self, book: Book):
        if not book.lent:
            return "Can't extend book that hasn't been lent"
        if book.lent_to != self:
            return "Can't extend book lent by someone else"
        if book.reserved:
            return "Can't extend - book reserved by someone"

        self.past_extended.setdefault(book, []).append(datetime.now())
        book.return_date += timedelta(days=30)
        return f"Extended the return date, new return date: {book.return_date}"

    def reserve(self, book: Book):
        if not book.reserved:
            book.reserved_until = datetime.now() + timedelta(days=7)
            book.reserved_by = self
            self.past_reserved.setdefault(book, []).append(datetime.now())
        else:
            raise BookReserved("Can't reserve book - already reserved")

    def to_dict(self):
        return {
            "ID": self.__id,
            "Name": self.name,
            "Surname": self.surname,
            "Phone": self.phone_num,
            "City": self.address.city if self.address else "",
            "Street": self.address.street if self.address else "",
            "Apartment": self.address.apartment if self.address else "",
            "Postal Code": self.address.postal_code if self.address else ""
        }

    @staticmethod
    def from_dict(d):
        address = Address(
            d.get("City", ""),
            d.get("Street", ""),
            d.get("Apartment", ""),
            d.get("Postal Code", "")
        )

        reader = Reader(d["Name"], d["Surname"], str(d["Phone"]), address=address)
        reader._Reader__id = d["ID"]
        Reader._Reader__readerID = max(Reader._Reader__readerID, d["ID"])
        return reader


# Library database
class Library:
    def __init__(self):
        self.readers: list[Reader] = []
        self.books: list[Book] = []
        self.available_books: list[Book] = []
        self.lent_books: list[Book] = []

    def show_available_books(self) -> list[Book]:
        self.available_books = [b for b in self.books if not b.lent and not b.reserved]
        return self.available_books

    def show_lent_books(self) -> list[Book]:
        self.lent_books = [b for b in self.books if b.lent]
        return self.lent_books

    def objects_from_excel(self, path: str, objects: list) -> list:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} not found.")
        df = pd.read_excel(path)
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            objects.append(row_dict)

        return objects

    def readers_from_excel(self, path):
        self.objects_from_excel(path, self.readers)

    def books_from_excel(self, path):
        self.objects_from_excel(path, self.books)
