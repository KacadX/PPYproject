from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from address import Address
from book import add_book, load_books_object, edit_book, remove_book
from exceptions import InvalidPhoneNumber
from library_db import Book, Reader
from reader import load_readers_object, add_reader, edit_reader, remove_reader


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

        from manage_books import ManageBooks
        from manage_readers import ManageReaders

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

