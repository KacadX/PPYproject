class Book:
    __id = 0

    def __init__(self, title: str, author: str, isbn: int, publisher: str, pageCount: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.pageCount = pageCount
        self.id += 1  # incremental unique ID for every single book
