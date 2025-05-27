from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from gui import Home
from exceptions import *
from reader import *
from library_db import Reader

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
        except AddingException as e:
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
            except DeletionException as e:
                self.message_label.text = f"Error: {e}"
        else:
            self.message_label.text = "Reader not found."
