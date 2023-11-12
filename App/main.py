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
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.input_items = []
        self.input_prices = []
        self.input_persons= []
        self.height_item = []
        self.input_totals = []

    def on_enter(self):
        # Window.bind(on_resize=self.on_window_resize)
        Window.size = (1080/3,2400/3)

        # window_width, window_height = Window.size
        button_obj = []
        label_obj = []
        textinput_obj = []
        
        
        height_item = 50
        for child in self.children:
            if isinstance(child,Button):
                button_obj.append(child)
            elif isinstance(child,Label):
                label_obj.append(child)
            elif isinstance(child, TextInput):
                textinput_obj.append(child)

            for c in child.children:
                if isinstance(c,Button):
                    button_obj.append(c)
                elif isinstance(c,Label):
                    label_obj.append(c)
                elif isinstance(c, TextInput):
                    textinput_obj.append(c)

                for c_sub in c.children:
                    if isinstance(c_sub,Button):
                        button_obj.append(c_sub)
                    elif isinstance(c_sub,Label):
                        label_obj.append(c_sub)
                    elif isinstance(c_sub, TextInput):
                        textinput_obj.append(c_sub)

                    for c_sub2 in c_sub.children:
                        if isinstance(c_sub2,Button):
                            button_obj.append(c_sub2)
                        elif isinstance(c_sub2,Label):
                            label_obj.append(c_sub2)
                        elif isinstance(c_sub2, TextInput):
                            textinput_obj.append(c_sub2)
                        
                        for c_sub3 in c_sub2.children:
                            if isinstance(c_sub3, Button):
                                button_obj.append(c_sub3)
                            elif isinstance(c_sub3, Label):
                                label_obj.append(c_sub3)
                            elif isinstance(c_sub3, TextInput):
                                textinput_obj.append(c_sub3)


        for i in range(len(button_obj)):
                print(button_obj[i].height)
        for i in range(len(label_obj)):
                print(label_obj[i].height)
        for i in range(len(textinput_obj)):
                print(textinput_obj[i].height)
                print(textinput_obj[i].hint_text)
                if textinput_obj[i].hint_text == "Tip":
                    self.input_totals.append(textinput_obj[i])
                if textinput_obj[i].hint_text == "Tax":
                    self.input_totals.append(textinput_obj[i])
        
        for p in range(len(self.input_totals)):
            print(f'OBJECT: {self.input_totals[p]}')
            self.input_totals[p].bind(text=self.update_totals)
        # tip_obj.bind(text=self.update_totals)
        # tax_obj.bind(text=self.update_totals)


    def on_window_resize(self, instance, width, height):
        print("Size:", Window.width, Window.height)


    def add_to_right(self):
        data_grid = self.ids.right_boxlayout2
        new_button = TextInput(hint_text='Person', size_hint=(1, None), height=100, background_color=[0.2,0.2,0.2,1], foreground_color=[1,1,1,1], font_size=30)
         
        self.input_persons.append(new_button)
        data_grid.add_widget(new_button)

    def add_to_left(self):
        data_grid = self.ids.left_boxlayout2
        textinput_item = TextInput(hint_text='Item', size_hint=(1, None), height=100, font_size=20)
        label_middle = Label(text='$', size_hint=(0.1,None), height=100, font_size=50)
        textinput_price = TextInput(hint_text='Price', size_hint=(0.6, None), height=100, font_size= 40)
        textinput_price.bind(text=self.update_totals)
        self.input_items.append(textinput_item)
        data_grid.add_widget(textinput_item)

        data_grid.add_widget(label_middle)

        self.input_prices.append(textinput_price)
        data_grid.add_widget(textinput_price)
        
    def add_to_left_preset(self):
        for i in range(10):
            self.add_to_left()
        

        for i in range(5):
            self.add_to_right()
        

        items = self.input_items
        prices = self.input_prices
        persons = self.input_persons

        items[0].text = "Item A"
        items[1].text = "Item B"
        items[2].text = "Item C"
        items[3].text = "Item A"
        items[4].text = "Item B"
        items[5].text = "Item C"
        items[6].text = "Item A"
        items[7].text = "Item B"
        items[8].text = "Item C"
        items[9].text = "Item A"
        

        prices[0].text = "53.00"
        prices[1].text = "5"
        prices[2].text = "0.05"
        prices[3].text = "10"
        prices[4].text = "10"
        prices[5].text = "10"
        prices[6].text = "10"
        prices[7].text = "10"
        prices[8].text = "10"
        prices[9].text = "10"

        persons[0].text = "Alex"
        persons[1].text = "Bob"
        persons[2].text = "Clara"
        persons[3].text = "Daniel"
        persons[4].text = "Evelyn"

    def update_totals(self, instance,text):
        prices = self.input_prices

        subtotal = 0.00
        grandtotal = 0.00
        tip = 0.00
        tax = 0.00
        
        tip_obj = self.input_totals[0]
        tax_obj = self.input_totals[1]
        if tip_obj.text != "":
            tip = float(self.input_totals[0].text)
        if tax_obj.text != "":
            tax = float(self.input_totals[1].text)
        
          
    
        for p in prices:
            if p.text != "":
                subtotal = subtotal + float(p.text)

        if subtotal != 0:
            grandtotal = grandtotal + subtotal
        if tip != 0:
            grandtotal = grandtotal + tip
        if tax != 0:
            grandtotal = grandtotal + tax
        
        self.ids.label_subtotal.text = f'Sub Total: ${subtotal:.2f}'
        self.ids.label_grandtotal.text =f'Grand Total: ${grandtotal:.2f}'

class NewScreen(Screen):
    def __init__(self, **kwargs):
        super(NewScreen, self).__init__(**kwargs)
        self.button_grid = []
        self.grid_objects = []

    def on_enter(self):
        mn_screen = self.manager.get_screen("main_screen")

        items = mn_screen.input_items
        prices = mn_screen.input_prices
        persons = mn_screen.input_persons

        layout_left = self.ids.table_grid_left
        layout_right = self.ids.table_grid_right
        layout_left_header = self.ids.grid_left_header
        layout_right_header = self.ids.grid_right_header

        grid_created = False
        for child in self.children:
            for c in child.children:
                for c_sub in c.children:
                    for c_sub2 in c_sub.children:
                        for c_sub3 in c_sub2.children:
                            for c_sub4 in c_sub3.children:
                                grid_created = True
        
        # for i in range(len(layout_delete)):
        #     print("Delete", layout_delete[i], layout_delete[i].text)
        #     layout.remove_widget(layout_delete[i])

        #Adds to Grid
        if grid_created == False:
            row_objects = []

            layout_left.cols = 2
            layout_left_header.cols = 2

            layout_right.cols = len(persons)
            layout_right_header.cols = len(persons)
            layout_right_header.size_hint = (None, 0.2)

            layout_right.width = 500
            layout_right_header.width = 500

            price_total = 0.00
            
            #Item Header
            label_item = Label(text='Item',size_hint=(None,None), height=50, font_size=20)
            row_objects.append(label_item)
            #layout_left.add_widget(label_item)
            layout_left_header.add_widget(label_item)

            #Price Header
            label_item = Label(text='Price',size_hint=(None,None), height=50, font_size=20)
            row_objects.append(label_item)
            #layout_left.add_widget(label_item)
            layout_left_header.add_widget(label_item)


            #Adds persons
            for i in range(len(persons)):
                label_item = Label(text=f'{persons[i].text}',size_hint=(None,None), height=50, width = 100, font_size=20)
                row_objects.append(label_item)
                #layout_right.add_widget(label_item)
                layout_right_header.add_widget(label_item)
            
            self.grid_objects.append(row_objects)

            #Add items
            for i in range(len(items)):
                row_objects = []
                label_item = Label(text=f'{items[i].text} : $',size_hint=(None,None), height=50, width = 80, font_size=20)
                label_price = Label(text=f'{prices[i].text}', size_hint=(None,None), height=50, width = 50, font_size=20)
                row_objects.append(label_item)
                row_objects.append(label_price)
                layout_left.add_widget(label_item)
                layout_left.add_widget(label_price)
                
                if prices[i].text != "":
                    price_total = price_total + float(prices[i].text)


                #Add Buttons
                for j in range(len(persons)):
                    button = Button(text='Add', size_hint=(None, None), height=50, width = 100, font_size=15)
                    button.bind(on_press=self.change_color)
                    row_objects.append(button)
                    layout_right.add_widget(button)
                
                self.grid_objects.append(row_objects)

        mystr = ""
        obj_str = ""
        for i in range(len(self.grid_objects)):
            row_objects = self.grid_objects[i]
            mystr = f"Row:{i}"
            for j in range(len(row_objects)):
                myobj = row_objects[j]
                if isinstance(myobj, Button):
                    obj_str = "Buttn"
                elif isinstance(myobj, Label):
                    obj_str = "Label"
                else:
                    obj_str = "Unknown"
                mystr = mystr + " | " + obj_str
            print(mystr)


        #updates totals 
        bottom_left = self.ids.bottom_left_boxlayout

        #adds subtotal
        subtotal_layout = BoxLayout(orientation='horizontal', size_hint_y = 1, spacing=10, padding=10)
        subtotal_label_item = Label(text="Sub Total $:")
        subtotal_label_price = Label(text="0.00")
        subtotal_layout.add_widget(subtotal_label_item)
        subtotal_layout.add_widget(subtotal_label_price)
        bottom_left.add_widget(subtotal_layout)

        #adds tax
        tax_layout = BoxLayout(orientation='horizontal', size_hint_y = 1, spacing = 10, padding=10)
        tax_label_item = Label(text="Tax $:")
        tax_label_price = Label(text="0.00")
        tax_layout.add_widget(tax_label_item)
        tax_layout.add_widget(tax_label_price)
        bottom_left.add_widget(tax_layout)

        #adds tip
        tip_layout = BoxLayout(orientation='horizontal', size_hint_y = 1, spacing = 10, padding=10)
        tip_label_item = Label(text="Tip $:")
        tip_label_price = Label(text="0.00")
        tip_layout.add_widget(tip_label_item)
        tip_layout.add_widget(tip_label_price)
        bottom_left.add_widget(tip_layout)

        #adds grand total
        grandtotal_layout = BoxLayout(orientation='horizontal', size_hint_y = 1, spacing = 10, padding=10)
        grandtotal_label_item = Label(text="Grand Total $:")
        grandtotal_label_price = Label(text="0.00")
        grandtotal_layout.add_widget(grandtotal_label_item)
        grandtotal_layout.add_widget(grandtotal_label_price)
        bottom_left.add_widget(grandtotal_layout)

    def change_color(self, instance):
        grid_obj = self.grid_objects 
        if instance.background_color == [0, 1, 0, 1]:
            instance.background_color = [1, 1, 1, 1]
        else:
            instance.background_color = [0, 1, 0, 1]
        self.update_grid()

    def update_grid(self):
        print("---------------------------------------")
        grid_obj = self.grid_objects
        color_grn = [0, 1, 0, 1]
        
        for i in range(1,len(grid_obj)):
            row_obj = grid_obj[i]
            row_price = float(grid_obj[i][1].text)
            row_green = 0
            #get total # of green
            for j in range(len(row_obj)):
                if isinstance(row_obj[j], Button):
                    if row_obj[j].background_color == color_grn:
                        row_green += 1
            

            for j in range(len(row_obj)):
                if isinstance(row_obj[j], Button):
                    if row_obj[j].background_color == color_grn:
                        price = row_price/row_green
                        row_obj[j].text = f'${price:.2f}'
                    else:
                        row_obj[j].text = 'Add'
    def update_totals(self):
        print("-------")

    
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
