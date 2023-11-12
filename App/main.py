from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager

class SplitReceipt(App):
    def build(self):
        return MyRoot()


class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()
    

    def create_table(self):
        rows = int(self.ids.input_items.text)
        columns = int(self.ids.input_people.text)

        table_grid = self.ids.table_grid
        table_grid.clear_widgets()
        
        for i in range(rows):
            if i == 0:
                row_layout = GridLayout(cols=columns,size_hint=(1, None), height=100)
            else:
                row_layout = GridLayout(cols=columns,size_hint=(1, None), height=50)
            for j in range(columns):
                button = Button(text=f'Button {i * columns + j + 1}')
                row_layout.add_widget(button)
            table_grid.add_widget(row_layout)
splitReceipt = SplitReceipt()
splitReceipt.run()
