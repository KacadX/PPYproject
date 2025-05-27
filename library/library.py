from reader import *

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