from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
import random

class MainScreen(Screen):
    pass
        
class NewScreen(Screen):
    def on_enter(self):
        main_screen = self.manager.get_screen('main_screen')
        columns = int(main_screen.ids.input_people.text)
        rows = int(main_screen.ids.input_items.text)

        layout = self.ids.table_grid
        # Create a ScrollView and add it to the layout
        scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True)
        scroll_layout = GridLayout(cols=columns, spacing=10, padding=10, size_hint=(None, None))
        scroll_layout.bind(minimum_width=scroll_layout.setter('width'), minimum_height=scroll_layout.setter('height'))

        for i in range(rows): 
            button = Button(text=f'Button {i}', size_hint=(None, None), size=(150, 50))
            button.bind(on_press=self.change_color)
            scroll_layout.add_widget(button)

        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)
    
    def change_color(self, instance):
        instance.background_color = (1, 0, 0, 1)
    
class SplitReceipt(App):
    def build(self):
        sm = ScreenManager()
        main_screen = MainScreen(name='main_screen')
        new_screen = NewScreen(name='new_screen')
        sm.add_widget(main_screen)
        sm.add_widget(new_screen)
        return sm

if __name__ == '__main__':
    SplitReceipt().run()


# name_grid = self.ids.boxlayout_name
        # name_grid.clear_widgets()
        # row_layout = GridLayout(cols=columns, spacing=10, padding=10)
        # for j in range(columns):
        #     button = Button(text=f'Name {j}')
        #     row_layout.add_widget(button)
        # name_grid.add_widget(row_layout)

        #In .kv
        # BoxLayout:
        #     orientation: 'vertical'
        #     id: boxlayout_name
        #     size_hint: (1, None)
        #     height: 100

# class MainScreen(Screen):
#     pass
    # def __init__(self):
    #     super(MainScreen, self).__init__()
    

    # def create_table(self):
    #     rows = int(self.ids.input_items.text)
    #     columns = int(self.ids.input_people.text)

    #     table_grid = self.ids.table_grid
    #     table_grid.clear_widgets()
        
    #     for i in range(rows):
    #         if i == 0:
    #             row_layout = GridLayout(cols=columns,size_hint=(1, None), height=100)
    #         else:
    #             row_layout = GridLayout(cols=columns,size_hint=(1, None), height=50)
    #         for j in range(columns):
    #             button = Button(text=f'Button {i * columns + j + 1}')
    #             row_layout.add_widget(button)
    #         table_grid.add_widget(row_layout)

# class NewScreen(Screen):
#     pass

# class SplitReceipt(App):
#     def build(self):
#         sm = ScreenManager()
#         main_screen = MainScreen(name='main_screen')
#         new_screen = NewScreen(name='new_screen')
#         sm.add_widget(main_screen)
#         sm.add_widget(new_screen)
#         return sm()
        
# splitReceipt = SplitReceipt()
# splitReceipt.run()
