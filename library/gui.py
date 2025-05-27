from kivy.uix.image import Image
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

        top_layout = BoxLayout(orientation="horizontal", size_hint_y=0.4)

        left_image = Image(source="./data/bibliotecznyPiems.jpg")
        welcome_label = Label(text="Welcome in library management system")
        right_image = Image(source="./data/bibliotecznyPiems.jpg")

        top_layout.add_widget(left_image)
        top_layout.add_widget(welcome_label)
        top_layout.add_widget(right_image)

        buttons_layout = BoxLayout(orientation="horizontal")
        btn_add_book = Button(text="Add new book")
        btn_borrow_book = Button(text="Lend a book")
        btn_add_reader = Button(text="Add new reader")
        
        btn_add_book.bind(on_press=lambda x: switch_layout_callback(AddBook))
        btn_borrow_book.bind(on_press=lambda x: switch_layout_callback(LendBook))
        btn_add_reader.bind(on_press=lambda x: switch_layout_callback(AddReader))
        
        buttons_layout.add_widget(btn_add_book)
        buttons_layout.add_widget(btn_borrow_book)
        buttons_layout.add_widget(btn_add_reader)

        self.add_widget(top_layout)
        self.add_widget(buttons_layout)


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


class GuiApp(App):
    def build(self):
        self.root_widget = Home(self.switch_layout)
        return self.root_widget

    def switch_layout(self, layout_class):
        self.root_widget.clear_widgets()
        new_layout = layout_class(switch_layout_callback=self.switch_layout)
        self.root_widget.add_widget(new_layout)