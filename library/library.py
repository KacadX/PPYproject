class Book:
    __bookID = 0

    def __init__(self, title: str, author: str, isbn: str, publisher: str, pageCount: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.pageCount = pageCount
        self.__id = Book.__bookID
        Book.__bookID += 1 # Incremental unique ID for every single book
        borrowed = False

    @property
    def id(self):
        return self.__id

class Reader:
    __readerID = 0

    def __init__(self, name: str, surname: str, phone_num: str):
        self.name = name
        self.surname = surname

        # Check if phone number is valid
        if len(str(phone_num)) != 9:
            except InvalidPhoneNumber:
                print("Phone number must consist of 9 digits")

        for n in phone_num:
            if str(n) < str(0) or str(n) > str(9):
                except InvalidPhoneNumber:
                    print("Phone number can contain only numbers")
                else:
                    self.phone_num = phone_num

        self.__id = Reader.__readerID
        Reader.__readerID += 1

        self.borrowed_books = []

    def borrow(self, book: Book):
        if book.borrowed == False:
            self.borrowed_books.append(book)
            book.borrowed = True
        else:
            print("Can't borrow already borrowed book")


class InvalidPhoneNumber(Exception):
    """Invalid phone number"""

