from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class Home(BoxLayout):
    def __init__(self, switch_layout_callback, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = "vertical"

        buttons_layout = BoxLayout(orientation="horizontal")

        welcome_label = Label(text="Lorem ipsum")

        btn_add_book = Button(text="Add new book")
        btn_borrow_book = Button(text="Borrow a book")
        btn_add_reader = Button(text="Add new reader")
        
        btn_add_book.bind(on_press=lambda x: switch_layout_callback(AddBook))
        btn_borrow_book.bind(on_press=lambda x: switch_layout_callback(BorrowBook))
        btn_add_reader.bind(on_press=lambda x: switch_layout_callback(AddReader))
        
        buttons_layout.add_widget(btn_add_book)
        buttons_layout.add_widget(btn_borrow_book)
        buttons_layout.add_widget(btn_add_reader)

        self.add_widget(welcome_label)
        self.add_widget(buttons_layout)

class AddBook(BoxLayout):
    def __init__(self, **kwargs):
        super(AddBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text="Add a new book here."))

class BorrowBook(BoxLayout):
    def __init__(self, **kwargs):
        super(BorrowBook, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text="Borrow a book here."))

class AddReader(BoxLayout):
    def __init__(self, **kwargs):
        super(AddReader, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text="Add a new reader here."))

class GuiApp(App):
    def build(self):
        self.root_widget = Home(self.switch_layout)
        return self.root_widget

    def switch_layout(self, layout_class):
        self.root_widget.clear_widgets()
        new_layout = layout_class()
        self.root_widget.add_widget(new_layout)

