from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config

class MainScreen(Screen):
    random_str = StringProperty()
    input_items = ObjectProperty()
    input_price = ObjectProperty
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.random_str = "Hello"
        self.input_items = []
        self.input_price = []
    #     # self.cols = 1
    #     # self.inside = GridLayout()
    #     # self.inside.cols = 2
    #     # self.inside.size_hint = (None, None)
    #     # self.inside.add_widget(Button(text="Submit", font_size=40))
    #     # self.add_widget(self.inside)
    def on_enter(self):
        Window.size = (1080/2,2400/3)

    def add_to_right(self):
        data_grid = self.ids.right_boxlayout2
        
        new_button = TextInput(hint_text='Person', size_hint=(1, None), height=100, background_color=[0.2,0.2,0.2,1], foreground_color=[1,1,1,1], font_size=30)
         
        data_grid.add_widget(new_button)

    def add_to_left(self):
        data_grid = self.ids.left_boxlayout2
        textinput_item = TextInput(hint_text='Item', size_hint=(1, None), height=100, font_size=20)
        label_middle = Label(text='$', size_hint=(0.1,None), height=100, font_size=50)
        textinput_price = TextInput(hint_text='Price', size_hint=(0.6, None), height=100, font_size= 40)

        self.input_items.append(textinput_item)
        data_grid.add_widget(textinput_item)

        data_grid.add_widget(label_middle)

        self.input_price.append(textinput_price)
        data_grid.add_widget(textinput_price)

    def add_to_left_preset(self):
        self.add_to_left()
        self.add_to_left()
        self.add_to_left()

        items = self.input_items
        prices = self.input_price

        items[0].text = "Item A"
        items[1].text = "Item B"
        items[2].text = "Item C"

        prices[0].text = "1.00"
        prices[1].text = "5"
        prices[2].text = "0.05"

class NewScreen(Screen):
    def on_enter(self):
        mn_screen = self.manager.get_screen("main_screen")

        items = mn_screen.input_items
        prices = mn_screen.input_price
       

        layout = self.ids.table_grid

        for i in range(len(items)):
            label_item = Label(text=f'{items[i].text} : ${prices[i].text}',size_hint=(0.1,None), height=50, font_size=20)
            layout.add_widget(label_item)
        

        
        # has_scroll = False
        # for child in self.children:
        #     for c in child.children:
        #         for c_sub in c.children:
        #             for c_sub2 in c_sub.children:
        #                 if isinstance(c_sub2, ScrollView):
        #                     has_scroll = True
        # if has_scroll == False:
        #     main_screen = self.manager.get_screen('main_screen')
        #     # columns = int(main_screen.ids.input_people.text)
        #     # rows = int(main_screen.ids.input_items.text)
        #     columns = 4
        #     rows = 10
        #     layout = self.ids.table_grid
        #     # Create a ScrollView and add it to the layout
        #     scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=True)
        #     scroll_layout = GridLayout(cols=columns, spacing=10, padding=10, size_hint=(None, None))
        #     scroll_layout.bind(minimum_width=scroll_layout.setter('width'), minimum_height=scroll_layout.setter('height'))

        #     for i in range(rows): 
        #         button = Button(text=f'Button {i}', size_hint=(None, None), size=(150, 50))
        #         button.bind(on_press=self.change_color)
        #         scroll_layout.add_widget(button)

        #     scroll_view.add_widget(scroll_layout)
        #     layout.add_widget(scroll_view)
    
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
