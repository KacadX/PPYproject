class Book:
    __id = 0

    def __init__(self, title: str, author: str, isbn: int, publisher: str, pageCount: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.pageCount = pageCount
        Book.__id += 1  # incremental unique ID for every single book

class Reader:
    __readerID = 0

    def __init__(self, name: str, surname: str, phone_num: str):
        self.name = name
        self,surname = surname

        for n in phone_num:
            if str(phone_num) < str(0) or str(phone_num) > str(9):
                except InvalidPhoneNumber:
                    print("Phone number can contain only numbers")
                else:
                    self.phone_num = phone_num

        Reader.__readerID += 1


class InvalidPhoneNumber(Exception):
    """Invalid phone number"""

