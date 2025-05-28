from kivy.app import App
from gui import Home

class GuiApp(App):
    def build(self):
        self.root_widget = Home(self.switch_layout)
        return self.root_widget

    def switch_layout(self, layout_class):
        self.root_widget.clear_widgets()
        new_layout = layout_class(switch_layout_callback=self.switch_layout)
        self.root_widget.add_widget(new_layout)
