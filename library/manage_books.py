from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from gui import Home
from exceptions import *
from book import add_book, load_books_object, edit_book, remove_book
from library_db import Book
from reader import load_readers_object

class ManageBooks(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(ManageBooks, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Book Management", size_hint_y=0.1))

        buttons_layout = GridLayout(cols=1, padding=50, spacing=20)

        btn_add_book = Button(text="Add New Book", size_hint_y=None, height=50)
        btn_edit_book = Button(text="Edit Book", size_hint_y=None, height=50)
        btn_remove_book = Button(text="Remove Book", size_hint_y=None, height=50)
        btn_lend_book = Button(text="Lend Book", size_hint_y=None, height=50)
        btn_return_book = Button(text="Return Book", size_hint_y=None, height=50)
        btn_reserve_book = Button(text="Reserve Book", size_hint_y=None, height=50)
        btn_extend_book = Button(text="Extend Return Date", size_hint_y=None, height=50)
        btn_list_books = Button(text="Show Book List", size_hint_y=None, height=50)
        btn_back = Button(text="Back to Main Menu", size_hint_y=None, height=50)

        btn_add_book.bind(on_press=lambda x: switch_layout_callback(AddBook))
        btn_edit_book.bind(on_press=lambda x: switch_layout_callback(EditBook))
        btn_remove_book.bind(on_press=lambda x: switch_layout_callback(RemoveBook))
        btn_lend_book.bind(on_press=lambda x: switch_layout_callback(LendBook))
        btn_return_book.bind(on_press=lambda x: switch_layout_callback(ReturnBook))
        btn_reserve_book.bind(on_press=lambda x: switch_layout_callback(ReserveBook))
        btn_extend_book.bind(on_press=lambda x: switch_layout_callback(ExtendReturnDate))
        btn_list_books.bind(on_press=lambda x: switch_layout_callback(BookList))
        btn_back.bind(on_press=lambda x: switch_layout_callback(Home))

        buttons_layout.add_widget(btn_add_book)
        buttons_layout.add_widget(btn_edit_book)
        buttons_layout.add_widget(btn_remove_book)
        buttons_layout.add_widget(btn_lend_book)
        buttons_layout.add_widget(btn_return_book)
        buttons_layout.add_widget(btn_reserve_book)
        buttons_layout.add_widget(btn_extend_book)
        buttons_layout.add_widget(btn_list_books)
        buttons_layout.add_widget(btn_back)

        scroll_view = ScrollView()
        scroll_view.add_widget(buttons_layout)
        self.add_widget(scroll_view)

class AddBook(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(AddBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.title_input = TextInput(hint_text="Title")
        self.author_input = TextInput(hint_text="Author")
        self.isbn_input = TextInput(hint_text="ISBN")
        self.publisher_input = TextInput(hint_text="Publisher")
        self.pages_input = TextInput(hint_text="Page count")

        self.add_widget(Label(text="Add a new book:"))

        form_layout = BoxLayout(orientation='vertical')
        form_layout.add_widget(self.title_input)
        form_layout.add_widget(self.author_input)
        form_layout.add_widget(self.isbn_input)
        form_layout.add_widget(self.publisher_input)
        form_layout.add_widget(self.pages_input)

        self.add_widget(form_layout)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)

        submit_btn = Button(text="Add Book")
        submit_btn.bind(on_press=self.submit_book)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(submit_btn)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def submit_book(self, instance):
        title = self.title_input.text.strip()
        author = self.author_input.text.strip()
        isbn = self.isbn_input.text.strip()
        publisher = self.publisher_input.text.strip()
        pages_text = self.pages_input.text.strip()

        if not title or not author or not isbn or not publisher or not pages_text:
            self.message_label.text = "Please fill in all fields."
            return

        try:
            pages = int(pages_text)
        except PageCountException:
            self.message_label.text = "Page count must be numbers."
            return

        try:
            book = Book(title, author, isbn, publisher, pages)
            add_book(book)
            self.message_label.text = f"Book '{title}' added successfully!"
            self.clear_inputs()
        except AddingException as e:
            self.message_label.text = f"Error: {e}"

    def clear_inputs(self):
        self.title_input.text = ""
        self.author_input.text = ""
        self.isbn_input.text = ""
        self.publisher_input.text = ""
        self.pages_input.text = ""

class BookList(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(BookList, self).__init__(**kwargs)

        self.switch_layout_callback = switch_layout_callback

        self.orientation = "vertical"
        self.spacing = 10

        columns_layout = BoxLayout(orientation="horizontal", size_hint_y=0.9)

        free_books_layout = BoxLayout(orientation="vertical")
        free_books_layout.add_widget(Label(text="Available Books", size_hint_y=0.1))

        self.free_scroll = ScrollView()
        self.free_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.free_list.bind(minimum_height=self.free_list.setter('height'))
        self.free_scroll.add_widget(self.free_list)
        free_books_layout.add_widget(self.free_scroll)

        lent_books_layout = BoxLayout(orientation="vertical")
        lent_books_layout.add_widget(Label(text="Borrowed Books", size_hint_y=0.1))

        self.lent_scroll = ScrollView()
        self.lent_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.lent_list.bind(minimum_height=self.lent_list.setter('height'))
        self.lent_scroll.add_widget(self.lent_list)
        lent_books_layout.add_widget(self.lent_scroll)

        columns_layout.add_widget(free_books_layout)
        columns_layout.add_widget(lent_books_layout)

        self.add_widget(columns_layout)

        btn_back = Button(text="Back", size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: self.switch_layout_callback(ManageBooks))
        self.add_widget(btn_back)

        self.refresh_list()

    def refresh_list(self):
        self.free_list.clear_widgets()
        self.lent_list.clear_widgets()

        books = load_books_object()

        for book in books:
            book_label = Label(text=f"{book.id}: {book.title} by {book.author}",
                               size_hint_y=None, height=40)

            if book.lent:
                book_label.color = (1, 0, 0, 1)
                self.lent_list.add_widget(book_label)
            else:
                book_label.color = (0, 1, 0, 1)
                self.free_list.add_widget(book_label)

class EditBook(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(EditBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Edit Book:"))

        self.book_spinner = Spinner(text="Select Book to edit")
        self.update_books()
        self.add_widget(self.book_spinner)

        self.title_input = TextInput(hint_text="Title")
        self.author_input = TextInput(hint_text="Author")
        self.isbn_input = TextInput(hint_text="ISBN")
        self.publisher_input = TextInput(hint_text="Publisher")
        self.pages_input = TextInput(hint_text="Page count")

        form_layout = BoxLayout(orientation='vertical')
        form_layout.add_widget(self.title_input)
        form_layout.add_widget(self.author_input)
        form_layout.add_widget(self.isbn_input)
        form_layout.add_widget(self.publisher_input)
        form_layout.add_widget(self.pages_input)

        self.add_widget(form_layout)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        btn_back = Button(text="Back")
        btn_save = Button(text="Save Changes")

        btn_back.bind(on_press=lambda x: switch_layout_callback(ManageBooks))
        btn_save.bind(on_press=self.save_changes)

        buttons_layout.add_widget(btn_back)
        buttons_layout.add_widget(btn_save)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def update_books(self):
        self.books = load_books_object()
        self.book_spinner.values = [f"{b.id}: {b.title}" for b in self.books]
        self.book_spinner.bind(text=self.show_book_details)

    def show_book_details(self, spinner, text):
        if text == "Select Book to edit":
            return

        book_id = int(text.split(":")[0])
        book = next((b for b in self.books if b.id == book_id), None)

        if book:
            self.title_input.text = book.title
            self.author_input.text = book.author
            self.isbn_input.text = str(book.isbn)
            self.publisher_input.text = book.publisher
            self.pages_input.text = str(book.page_count)

    def save_changes(self, instance):
        book_text = self.book_spinner.text
        if book_text == "Select Book to edit":
            self.message_label.text = "Please select a book to edit."
            return

        book_id = int(book_text.split(":")[0])
        book_search = next((b for b in self.books if b.id == book_id), None)

        if not book_search:
            self.message_label.text = "Book not found."
            return

        try:
            updated_book = Book(
                self.title_input.text.strip(),
                self.author_input.text.strip(),
                int(self.isbn_input.text.strip()),
                self.publisher_input.text.strip(),
                int(self.pages_input.text.strip())
            )
            updated_book.id = book_id

            edit_book(book_id, updated_book)
            self.message_label.text = "Book updated successfully!"
            self.update_books()
        except BookEditException as e:
            self.message_label.text = f"Error: {e}"

class LendBook(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(LendBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Lend a Book"))

        self.reader_spinner = Spinner(text="Select Reader")
        self.book_spinner = Spinner(text="Select Book")

        self.update_readers_and_books()

        self.add_widget(self.reader_spinner)
        self.add_widget(self.book_spinner)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        back_btn = Button(text="Back to Menu")
        back_btn.bind(on_press=self.go_back)

        borrow_btn = Button(text="Lend Book")
        borrow_btn.bind(on_press=self.lend_book)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(borrow_btn)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def update_readers_and_books(self):
        self.readers = load_readers_object()
        self.books = [b for b in load_books_object() if not getattr(b, "lent", False)]

        self.reader_spinner.values = [f"{r.id}: {r.name} {r.surname}" for r in self.readers]
        self.book_spinner.values = [f"{b.id}: {b.title}" for b in self.books]

    def lend_book(self, instance):
        reader_text = self.reader_spinner.text
        book_text = self.book_spinner.text

        if reader_text == "Select Reader" or book_text == "Select Book":
            self.message_label.text = "Please select both reader and book."
            return

        reader_id = int(reader_text.split(":")[0])
        book_id = int(book_text.split(":")[0])

        reader_search = next((r for r in self.readers if r.id == reader_id), None)
        book_search = next((b for b in self.books if b.id == book_id), None)

        if reader_search and book_search:
            try:
                reader_search.borrow(book_search)
                self.message_label.text = f"Book '{book_search.title}' lent to {reader_search.name}."
                self.update_readers_and_books()
            except (BookLentToSomeone, BookReserved) as e:
                self.message_label.text = f"Error: {e}"


class ReturnBook(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(ReturnBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Return a Book"))

        self.reader_spinner = Spinner(text="Select Reader")
        self.book_spinner = Spinner(text="Select Book to Return")

        self.update_readers_and_books()

        self.add_widget(self.reader_spinner)
        self.add_widget(self.book_spinner)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        back_btn = Button(text="Back to Menu")
        back_btn.bind(on_press=self.go_back)

        return_btn = Button(text="Return Book")
        return_btn.bind(on_press=self.return_book)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(return_btn)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def update_readers_and_books(self):
        self.readers = load_readers_object()
        self.books = [b for b in load_books_object() if getattr(b, "lent", False)]

        self.reader_spinner.values = [f"{r.id}: {r.name} {r.surname}" for r in self.readers]
        self.book_spinner.values = [f"{b.id}: {b.title}" for b in self.books if b.lent]

    def return_book(self, instance):
        reader_text = self.reader_spinner.text
        book_text = self.book_spinner.text

        if reader_text == "Select Reader" or book_text == "Select Book to Return":
            self.message_label.text = "Please select both reader and book."
            return

        reader_id = int(reader_text.split(":")[0])
        book_id = int(book_text.split(":")[0])

        reader_search = next((r for r in self.readers if r.id == reader_id), None)
        book_search = next((b for b in self.books if b.id == book_id), None)

        if reader_search and book_search:
            if not book_search.lent or book_search.lent_to != reader_id:
                self.message_label.text = f"Error: This book is not borrowed by {reader_search.name} {reader_search.surname}."
                return

            try:
                fee = reader_search.return_book(book_search)
                if fee > 0:
                    self.message_label.text = f"Book '{book_search.title}' returned with a fee of ${fee:.2f}."
                else:
                    self.message_label.text = f"Book '{book_search.title}' returned successfully with no fee."
                self.update_readers_and_books()
            except Exception as e:
                self.message_label.text = f"Error: {e}"
        else:
            self.message_label.text = "Reader or book not found."

class RemoveBook(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(RemoveBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Remove a book:"))

        self.book_spinner = Spinner(text="Select Book to remove")
        self.update_books()

        self.add_widget(self.book_spinner)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)

        remove_btn = Button(text="Remove Book")
        remove_btn.bind(on_press=self.remove_book)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(remove_btn)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def update_books(self):
        self.books = load_books_object()
        self.book_spinner.values = [f"{b.id}: {b.title}" for b in self.books]

    def remove_book(self, instance):
        book_text = self.book_spinner.text

        if book_text == "Select Book to remove":
            self.message_label.text = "Please select a book to remove."
            return

        book_id = int(book_text.split(":")[0])
        book_search = next((b for b in self.books if b.id == book_id), None)

        if book_search:
            try:
                remove_book(book_id)
                self.message_label.text = f"Book '{book_search.title}' removed successfully!"
                self.update_books()
            except DeletionException as e:
                self.message_label.text = f"Error: {e}"
        else:
            self.message_label.text = "Book not found."
            
class ReserveBook(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(ReserveBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Reserve a Book"))

        self.reader_spinner = Spinner(text="Select Reader")
        self.book_spinner = Spinner(text="Select Book to Reserve")

        self.update_readers_and_books()

        self.add_widget(self.reader_spinner)
        self.add_widget(self.book_spinner)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        back_btn = Button(text="Back to Menu")
        back_btn.bind(on_press=self.go_back)

        reserve_btn = Button(text="Reserve Book")
        reserve_btn.bind(on_press=self.reserve_book)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(reserve_btn)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def update_readers_and_books(self):
        self.readers = load_readers_object()
        self.books = [b for b in load_books_object() if getattr(b, "lent", False) and not getattr(b, "reserved", False)]

        self.reader_spinner.values = [f"{r.id}: {r.name} {r.surname}" for r in self.readers]
        self.book_spinner.values = [f"{b.id}: {b.title}" for b in self.books]

    def reserve_book(self, instance):
        reader_text = self.reader_spinner.text
        book_text = self.book_spinner.text

        if reader_text == "Select Reader" or book_text == "Select Book to Reserve":
            self.message_label.text = "Please select both reader and book."
            return

        reader_id = int(reader_text.split(":")[0])
        book_id = int(book_text.split(":")[0])

        reader_search = next((r for r in self.readers if r.id == reader_id), None)
        book_search = next((b for b in self.books if b.id == book_id), None)

        if reader_search and book_search:
            try:
                reader_search.reserve(book_search)
                self.message_label.text = f"Book '{book_search.title}' reserved for {reader_search.name} until {book_search.reserved_until.strftime('%Y-%m-%d')}."
                self.update_readers_and_books()
            except Exception as e:
                self.message_label.text = f"Error: {e}"
        else:
            self.message_label.text = "Reader or book not found."

class ExtendReturnDate(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(ExtendReturnDate, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Extend Return Date"))

        self.reader_spinner = Spinner(text="Select Reader")
        self.book_spinner = Spinner(text="Select Book to Extend")

        self.update_readers_and_books()

        self.add_widget(self.reader_spinner)
        self.add_widget(self.book_spinner)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        back_btn = Button(text="Back to Menu")
        back_btn.bind(on_press=self.go_back)

        extend_btn = Button(text="Extend Return Date")
        extend_btn.bind(on_press=self.extend_return_date)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(extend_btn)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def update_readers_and_books(self):
        self.readers = load_readers_object()
        self.books = [b for b in load_books_object() if getattr(b, "lent", False)]

        self.reader_spinner.values = [f"{r.id}: {r.name} {r.surname}" for r in self.readers]
        self.book_spinner.values = [f"{b.id}: {b.title}" for b in self.books if b.lent]

    def extend_return_date(self, instance):
        reader_text = self.reader_spinner.text
        book_text = self.book_spinner.text

        if reader_text == "Select Reader" or book_text == "Select Book to Extend":
            self.message_label.text = "Please select both reader and book."
            return

        reader_id = int(reader_text.split(":")[0])
        book_id = int(book_text.split(":")[0])

        reader_search = next((r for r in self.readers if r.id == reader_id), None)
        book_search = next((b for b in self.books if b.id == book_id), None)

        if reader_search and book_search:
            if not book_search.lent or book_search.lent_to != reader_id:
                self.message_label.text = f"Error: This book is not borrowed by {reader_search.name} {reader_search.surname}."
                return

            try:
                result = reader_search.extend(book_search)
                self.message_label.text = result
                self.update_readers_and_books()
            except Exception as e:
                self.message_label.text = f"Error: {e}"
        else:
            self.message_label.text = "Reader or book not found."