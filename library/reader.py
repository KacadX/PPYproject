import os
from datetime import datetime, timedelta
import pandas as pd

from address import *
from book import *
from exceptions import *

#Part responsible for readers
readers_path = "./library/data/readers.xlsx"
readers_columns = ["ID", "Name", "Surname", "Phone", "City", "Street", "Apartment", "Postal Code"]

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
                raise Exception("Can't borrow already lent book.")
        else:
            return "Book reserved by someone else"

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
            return "Can't reserve book - already reserved"

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

"""
Pandas readers =====
"""

def prepare_readers_file():
    os.makedirs("./library/data", exist_ok=True)
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
    reader._Reader__id = new_id
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
        df.loc[df["ID"] == reader_id, ["Name", "Surname", "Phone", "City", "Street", "Apartment", "Postal Code"]] = [
            updated_reader.name,
            updated_reader.surname,
            updated_reader.phone_num,
            updated_reader.address.city if updated_reader.address else "",
            updated_reader.address.street if updated_reader.address else "",
            updated_reader.address.apartment if updated_reader.address else "",
            updated_reader.address.postal_code if updated_reader.address else ""
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
