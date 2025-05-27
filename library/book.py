import os
import pandas as pd

from library.library_db import Book

books_path = "./library/data/books.xlsx"
books_columns = ["ID", "Title", "Author", "ISBN", "Publisher", "Pages"]

"""
Pandas books =====
"""

def excel_file_preparer():
    os.makedirs("./library/data", exist_ok=True)
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
    excel_file_preparer()

    df = load_books()
    new_id = 1 if df.empty else int(df["ID"].max()) + 1
    book.id = new_id
    Book._Book__id = new_id
    new_df = pd.DataFrame([book.to_dict()])
    df = pd.concat([df, new_df], ignore_index=True)
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