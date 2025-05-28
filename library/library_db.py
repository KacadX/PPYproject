import os
from datetime import datetime, timedelta
import pandas as pd

from address import Address
from exceptions import InvalidPhoneNumber, BookLentToSomeone, BookReserved


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
            "Pages": self.page_count,
            "Lent": self.lent,
            "Lent to": self.lent_to.id if self.lent_to else None,
            "Lent date": self.lent_date,
            "Return date": self.return_date,
            "Reserved": self.reserved,
            "Reserved by": self.reserved_by.id if self.reserved_by else None,
            "Reserved until": self.reserved_until
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
        book.lent = d.get("Lent", False)
        book.lent_to = d.get("Lent to", None)
        book.lent_date = d.get("Lent date", None)
        book.return_date = d.get("Return date", None)
        book.reserved = d.get("Reserved", False)
        book.reserved_by = d.get("Reserved by", None)
        book.reserved_until = d.get("Reserved until", None)

        Book.__id = max(Book.__id, d["ID"])
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
        if not book.reserved or book.reserved_by == self:
            if not book.lent:
                self.borrowed_books.append(book)
                if book in self.past_borrowed:
                    self.past_borrowed[book].append(now)
                else:
                    self.past_borrowed[book] = [now]

                book.lent = True
                book.lent_to = self
                book.lent_date = now
                book.return_date = now + timedelta(days=30)

                if book.reserved_by == self:
                    book.reserved = False
                    book.reserved_by = None

                from book import update_book_status
                update_book_status(book.id, True, self.id)
            else:
                raise BookLentToSomeone("Can't borrow already lent book.")
        else:
            raise BookReserved("Book reserved by someone else")

    def return_book(self, book: Book):
        now = datetime.now()
        date_until_fee = book.return_date
        fee = 0

        if now.day > date_until_fee.day:
            fee = 0.5 * (now - date_until_fee).days

        if book in self.past_returned:
            self.past_returned[book].append(now)
        else:
            self.past_returned[book] = [now]

        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

        book.lent = False
        book.lent_to = None
        book.lent_date = None
        book.return_date = None

        if book.reserved and book.reserved_by == self:
            book.reserved = False
            book.reserved_by = None

        from book import update_book_status
        update_book_status(book.id, False, None)

        return fee
    def extend(self, book: Book):
        if not book.lent:
            return "Can't extend book that hasn't been lent"
        if book.reserved:
            return "Can't extend - book reserved by someone"

        self.past_extended.setdefault(book, []).append(datetime.now())
        book.return_date += timedelta(days=30)
        return f"Extended the return date, new return date: {book.return_date}"

    def reserve(self, book: Book):
        if book.lent and not book.reserved:
            book.reserved_until = book.return_date + timedelta(days=7)
            book.reserved_by = self
            book.reserved = True
            self.past_reserved.setdefault(book, []).append(datetime.now())
        else:
            raise BookReserved("Can't reserve book - already reserved or not lent")

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

        from book import load_books_object
        all_books = load_books_object()
        reader.borrowed_books = [book for book in all_books if book.lent and book.lent_to == reader.id]

        return reader