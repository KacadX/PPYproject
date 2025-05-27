from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from library import *
from book import *
from reader import *


class Home(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.switch_layout_callback = switch_layout_callback

        top_layout = BoxLayout(orientation="horizontal", size_hint_y=0.4)

        left_image = Image(source="./data/bibliotecznyPiems.jpg")
        welcome_label = Label(text="Welcome in library management system")
        right_image = Image(source="./data/bibliotecznyPiems.jpg")

        top_layout.add_widget(left_image)
        top_layout.add_widget(welcome_label)
        top_layout.add_widget(right_image)

        buttons_layout = BoxLayout(orientation="vertical", padding=50, spacing=20)

        btn_manage_books = Button(text="Manage Books", size_hint_y=None, height=60)
        btn_manage_readers = Button(text="Manage Readers", size_hint_y=None, height=60)
        btn_exit = Button(text="Exit", size_hint_y=None, height=60)

        btn_manage_books.bind(on_press=lambda x: switch_layout_callback(ManageBooks))
        btn_manage_readers.bind(on_press=lambda x: switch_layout_callback(ManageReaders))
        btn_exit.bind(on_press=self.exit_app)

        buttons_layout.add_widget(btn_manage_books)
        buttons_layout.add_widget(btn_manage_readers)
        buttons_layout.add_widget(btn_exit)

        self.add_widget(top_layout)
        self.add_widget(buttons_layout)

    def exit_app(self, instance):
        App.get_running_app().stop()


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
        btn_list_books = Button(text="Show Book List", size_hint_y=None, height=50)
        btn_back = Button(text="Back to Main Menu", size_hint_y=None, height=50)

        btn_add_book.bind(on_press=lambda x: switch_layout_callback(AddBook))
        btn_edit_book.bind(on_press=lambda x: switch_layout_callback(EditBook))
        btn_remove_book.bind(on_press=lambda x: switch_layout_callback(RemoveBook))
        btn_lend_book.bind(on_press=lambda x: switch_layout_callback(LendBook))
        btn_list_books.bind(on_press=lambda x: switch_layout_callback(BookList))
        btn_back.bind(on_press=lambda x: switch_layout_callback(Home))

        buttons_layout.add_widget(btn_add_book)
        buttons_layout.add_widget(btn_edit_book)
        buttons_layout.add_widget(btn_remove_book)
        buttons_layout.add_widget(btn_lend_book)
        buttons_layout.add_widget(btn_list_books)
        buttons_layout.add_widget(btn_back)

        scroll_view = ScrollView()
        scroll_view.add_widget(buttons_layout)
        self.add_widget(scroll_view)


class ManageReaders(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(ManageReaders, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Reader Management", size_hint_y=0.1))

        buttons_layout = GridLayout(cols=1, padding=50, spacing=20)

        btn_add_reader = Button(text="Add New Reader", size_hint_y=None, height=50)
        btn_edit_reader = Button(text="Edit Reader", size_hint_y=None, height=50)
        btn_remove_reader = Button(text="Remove Reader", size_hint_y=None, height=50)
        btn_list_readers = Button(text="Show Reader List", size_hint_y=None, height=50)
        btn_back = Button(text="Back to Main Menu", size_hint_y=None, height=50)

        btn_add_reader.bind(on_press=lambda x: switch_layout_callback(AddReader))
        btn_edit_reader.bind(on_press=lambda x: switch_layout_callback(EditReader))
        btn_remove_reader.bind(on_press=lambda x: switch_layout_callback(RemoveReader))
        btn_list_readers.bind(on_press=lambda x: switch_layout_callback(ReaderList))
        btn_back.bind(on_press=lambda x: switch_layout_callback(Home))

        buttons_layout.add_widget(btn_add_reader)
        buttons_layout.add_widget(btn_edit_reader)
        buttons_layout.add_widget(btn_remove_reader)
        buttons_layout.add_widget(btn_list_readers)
        buttons_layout.add_widget(btn_back)

        scroll_view = ScrollView()
        scroll_view.add_widget(buttons_layout)
        self.add_widget(scroll_view)


class BookList(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(BookList, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Book List", size_hint_y=0.1))

        scroll_view = ScrollView()
        self.list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))

        self.refresh_list()

        scroll_view.add_widget(self.list_layout)
        self.add_widget(scroll_view)

        btn_back = Button(text="Back", size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: switch_layout_callback(ManageBooks))
        self.add_widget(btn_back)

    def refresh_list(self):
        self.list_layout.clear_widgets()
        books = load_books_object()
        for book in books:
            book_label = Label(text=f"{book.id}: {book.title} by {book.author}",
                               size_hint_y=None, height=40)
            self.list_layout.add_widget(book_label)


class ReaderList(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(ReaderList, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Reader List", size_hint_y=0.1))

        scroll_view = ScrollView()
        self.list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))

        self.refresh_list()

        scroll_view.add_widget(self.list_layout)
        self.add_widget(scroll_view)

        btn_back = Button(text="Back", size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: switch_layout_callback(ManageReaders))
        self.add_widget(btn_back)

    def refresh_list(self):
        self.list_layout.clear_widgets()
        readers = load_readers_object()
        for reader in readers:
            reader_label = Label(text=f"{reader.id}: {reader.name} {reader.surname}",
                                 size_hint_y=None, height=40)
            self.list_layout.add_widget(reader_label)


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
        except ValueError:
            self.message_label.text = "Page count must be numbers."
            return

        try:
            book = Book(title, author, isbn, publisher, pages)
            add_book(book)
            self.message_label.text = f"Book '{title}' added successfully!"
            self.clear_inputs()
        except Exception as e:
            self.message_label.text = f"Error: {e}"

    def clear_inputs(self):
        self.title_input.text = ""
        self.author_input.text = ""
        self.isbn_input.text = ""
        self.publisher_input.text = ""
        self.pages_input.text = ""

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
        book = next((b for b in self.books if b.id == book_id), None)

        if book:
            try:
                remove_book(book_id)
                self.message_label.text = f"Book '{book.title}' removed successfully!"
                self.update_books()
            except Exception as e:
                self.message_label.text = f"Error: {e}"
        else:
            self.message_label.text = "Book not found."


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

        reader = next((r for r in self.readers if r.id == reader_id), None)
        book = next((b for b in self.books if b.id == book_id), None)

        if reader and book:
            result = reader.borrow(book)
            if result is None:
                self.message_label.text = f"Book '{book.title}' lent by {reader.name}."
                self.update_readers_and_books()
            else:
                self.message_label.text = result
        else:
            self.message_label.text = "Reader or book not found."


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
        book = next((b for b in self.books if b.id == book_id), None)

        if not book:
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
        except Exception as e:
            self.message_label.text = f"Error: {e}"


class AddReader(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(AddReader, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Add a new reader here."))

        self.name = TextInput(hint_text="Name")
        self.surname = TextInput(hint_text="Surname")
        self.phone_num = TextInput(hint_text="Phone number")
        self.city = TextInput(hint_text="City")
        self.street = TextInput(hint_text="Street")
        self.apartment = TextInput(hint_text="Apartment")
        self.postal_code = TextInput(hint_text="Postal code")

        self.add_widget(self.text_input_layout())

        self.message_label = Label(text="")
        self.add_widget(self.message_label)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        back_btn = Button(text="Back to Menu")
        back_btn.bind(on_press=self.go_back)

        add_btn = Button(text="Add Reader")
        add_btn.bind(on_press=self.add_reader)

        buttons_layout.add_widget(back_btn)
        buttons_layout.add_widget(add_btn)

        self.add_widget(buttons_layout)

    def go_back(self, instance):
        self.switch_layout_callback(Home)

    def first_column_layout(self) -> BoxLayout:
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.name)
        layout.add_widget(self.surname)
        layout.add_widget(self.phone_num)
        return layout

    def second_column_layout(self) -> BoxLayout:
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.city)
        layout.add_widget(self.street)
        layout.add_widget(self.apartment)
        layout.add_widget(self.postal_code)
        return layout

    def text_input_layout(self) -> BoxLayout:
        layout = BoxLayout(orientation="horizontal")
        layout.add_widget(self.first_column_layout())
        layout.add_widget(self.second_column_layout())
        return layout

    def add_reader(self, instance):
        name = self.name.text.strip()
        surname = self.surname.text.strip()
        phone = self.phone_num.text.strip()
        city = self.city.text.strip()
        street = self.street.text.strip()
        apartment = self.apartment.text.strip()
        postal_code = self.postal_code.text.strip()

        if not name or not surname or not phone:
            self.message_label.text = "Please fill in all required fields."
            return

        try:
            address = Address(city, street, apartment, postal_code)
            reader = Reader(name, surname, phone, address)
            add_reader(reader)

            self.message_label.text = f"Reader '{name} {surname}' added successfully!"
            self.clear_inputs()
        except InvalidPhoneNumber as e:
            self.message_label.text = f"Invalid phone number: {e}"
        except Exception as e:
            self.message_label.text = f"Error: {e}"

    def clear_inputs(self):
        self.name.text = ""
        self.surname.text = ""
        self.phone_num.text = ""
        self.city.text = ""
        self.street.text = ""
        self.apartment.text = ""
        self.postal_code.text = ""


class EditReader(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(EditReader, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.switch_layout_callback = switch_layout_callback

        self.add_widget(Label(text="Edit Reader:"))

        self.reader_spinner = Spinner(text="Select Reader to edit")
        self.update_readers()
        self.add_widget(self.reader_spinner)

        self.name = TextInput(hint_text="Name")
        self.surname = TextInput(hint_text="Surname")
        self.phone_num = TextInput(hint_text="Phone number")
        self.city = TextInput(hint_text="City")
        self.street = TextInput(hint_text="Street")
        self.apartment = TextInput(hint_text="Apartment")
        self.postal_code = TextInput(hint_text="Postal code")

        self.add_widget(self.text_input_layout())

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        btn_back = Button(text="Back")
        btn_save = Button(text="Save Changes")

        btn_back.bind(on_press=lambda x: switch_layout_callback(ManageReaders))
        btn_save.bind(on_press=self.save_changes)

        buttons_layout.add_widget(btn_back)
        buttons_layout.add_widget(btn_save)

        self.add_widget(buttons_layout)

        self.message_label = Label()
        self.add_widget(self.message_label)

    def text_input_layout(self):
        layout = BoxLayout(orientation='horizontal')

        col1 = BoxLayout(orientation='vertical')
        col1.add_widget(self.name)
        col1.add_widget(self.surname)
        col1.add_widget(self.phone_num)

        col2 = BoxLayout(orientation='vertical')
        col2.add_widget(self.city)
        col2.add_widget(self.street)
        col2.add_widget(self.apartment)
        col2.add_widget(self.postal_code)

        layout.add_widget(col1)
        layout.add_widget(col2)
        return layout

    def update_readers(self):
        self.readers = load_readers_object()
        self.reader_spinner.values = [f"{r.id}: {r.name} {r.surname}" for r in self.readers]
        self.reader_spinner.bind(text=self.show_reader_details)

    def show_reader_details(self, spinner, text):
        if text == "Select Reader to edit":
            return

        reader_id = int(text.split(":")[0])
        reader = next((r for r in self.readers if r.id == reader_id), None)

        if reader:
            self.name.text = reader.name
            self.surname.text = reader.surname
            self.phone_num.text = reader.phone_num
            if reader.address:
                self.city.text = reader.address.city
                self.street.text = reader.address.street
                self.apartment.text = reader.address.apartment
                self.postal_code.text = reader.address.postal_code

    def save_changes(self, instance):
        reader_text = self.reader_spinner.text
        if reader_text == "Select Reader to edit":
            self.message_label.text = "Please select a reader to edit."
            return

        reader_id = int(reader_text.split(":")[0])
        reader = next((r for r in self.readers if r.id == reader_id), None)

        if not reader:
            self.message_label.text = "Reader not found."
            return

        try:
            address = Address(
                self.city.text.strip(),
                self.street.text.strip(),
                self.apartment.text.strip(),
                self.postal_code.text.strip()
            )

            updated_reader = Reader(
                self.name.text.strip(),
                self.surname.text.strip(),
                self.phone_num.text.strip(),
                address
            )
            updated_reader._Reader__id = reader_id

            edit_reader(reader_id, updated_reader)
            self.message_label.text = "Reader updated successfully!"
            self.update_readers()
        except InvalidPhoneNumber as e:
            self.message_label.text = f"Invalid phone number: {e}"
        except Exception as e:
            self.message_label.text = f"Error: {e}"

    class RemoveReader(BoxLayout):
        def __init__(self, switch_layout_callback, **kwargs):
            super(RemoveReader, self).__init__(**kwargs)
            self.orientation = 'vertical'
            self.switch_layout_callback = switch_layout_callback

            self.add_widget(Label(text="Remove Reader:"))

            self.reader_spinner = Spinner(text="Select Reader to remove")
            self.update_readers()

            self.add_widget(self.reader_spinner)

            buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)

            back_btn = Button(text="Back to Menu")
            back_btn.bind(on_press=self.go_back)

            remove_btn = Button(text="Remove Reader")
            remove_btn.bind(on_press=self.remove_reader)

            buttons_layout.add_widget(back_btn)
            buttons_layout.add_widget(remove_btn)

            self.add_widget(buttons_layout)

            self.message_label = Label()
            self.add_widget(self.message_label)

        def go_back(self, instance):
            self.switch_layout_callback(ManageReaders)

        def update_readers(self):
            self.readers = load_readers_object()
            self.reader_spinner.values = [f"{r.id}: {r.name} {r.surname}" for r in self.readers]

        def remove_reader(self, instance):
            reader_text = self.reader_spinner.text

            if reader_text == "Select Reader to remove":
                self.message_label.text = "Please select a reader to remove."
                return

            reader_id = int(reader_text.split(":")[0])
            reader = next((r for r in self.readers if r.id == reader_id), None)

            if reader:
                try:
                    remove_reader(reader_id)
                    self.message_label.text = f"Reader '{reader.name} {reader.surname}' removed successfully!"
                    self.update_readers()
                except Exception as e:
                    self.message_label.text = f"Error: {e}"
            else:
                self.message_label.text = "Reader not found."


class GuiApp(App):
    def build(self):
        self.root_widget = Home(self.switch_layout)
        return self.root_widget

    def switch_layout(self, layout_class):
        self.root_widget.clear_widgets()
        new_layout = layout_class(switch_layout_callback=self.switch_layout)
        self.root_widget.add_widget(new_layout)
