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

# To update for app deployment
# buildozer -v android debug

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.input_items = []
        self.input_prices = []
        self.input_persons= []
        self.height_item = 120.02/3
        self.width_item = 200/3
        self.input_totals = []
        self.totals = [0.00,0.00,0.00,0.00]
        
    def on_enter(self):
        # Window.bind(on_resize=self.on_window_resize)
        Window.size = (1080/3,2400/3)

        # window_width, window_height = Window.size
        button_obj = []
        label_obj = []
        textinput_obj = []
        
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
        textinput_height = self.height_item 

        data_grid = self.ids.right_boxlayout2
        new_button = TextInput(hint_text='Person', size_hint=(1, None), height=textinput_height, background_color=[0.2,0.2,0.2,1], foreground_color=[1,1,1,1])
         
        self.input_persons.append(new_button)
        data_grid.add_widget(new_button)

    def add_to_left(self):
        data_grid = self.ids.left_boxlayout2

        textinput_height = self.height_item 

        textinput_item = TextInput(hint_text='Item', size_hint=(1, None), height=textinput_height)
        label_middle = Label(text='$', size_hint=(0.1,None), height=textinput_height)
        textinput_price = TextInput(hint_text='Price', size_hint=(0.6, None), height=textinput_height)
        textinput_price.bind(text=self.update_totals)
        self.input_items.append(textinput_item)
        data_grid.add_widget(textinput_item)

        data_grid.add_widget(label_middle)

        self.input_prices.append(textinput_price)
        data_grid.add_widget(textinput_price)
        
    def add_to_left_preset(self):
        for i in range(18):
            self.add_to_left()
        

        for i in range(10):
            self.add_to_right()
        

        items = self.input_items
        prices = self.input_prices
        persons = self.input_persons

        items[0].text = "Item 1"
        items[1].text = "Item 2"
        items[2].text = "Item 3"
        items[3].text = "Item 4"
        items[4].text = "Item 5"
        items[5].text = "Item 6"
        items[6].text = "Item 7"
        items[7].text = "Item 8"
        items[8].text = "Item 9"
        items[9].text = "Item 10"
        items[10].text = "Item 11"
        items[11].text = "Item 12"
        items[12].text = "Item 13"
        items[13].text = "Item 14"
        items[14].text = "Item 15"
        items[15].text = "Item 16"
        items[16].text = "Item 17"
        items[17].text = "Item 18"

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
        prices[10].text = "10"
        prices[11].text = "10"
        prices[12].text = "10"
        prices[13].text = "10"
        prices[14].text = "10"
        prices[15].text = "10"
        prices[16].text = "10"
        prices[17].text = "10"


        persons[0].text = "Alex"
        persons[1].text = "Bob"
        persons[2].text = "Clara"
        persons[3].text = "Daniel"
        persons[4].text = "Evelyn"
        persons[5].text = "Frank"
        persons[6].text = "Gabe"
        persons[7].text = "Henry"
        persons[8].text = "Iggy"
        persons[9].text = "Jackie"


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
            self.totals[0] = subtotal
        if tax != 0:
            grandtotal = grandtotal + tax
            self.totals[1] = tax
        if tip != 0:
            grandtotal = grandtotal + tip
            self.totals[2] = tip
        
        
        self.totals[3] = grandtotal
        self.ids.label_subtotal_price.text = f'{subtotal:.2f}'
        self.ids.label_grandtotal_price.text =f'{grandtotal:.2f}'

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
        layout_right_bottom = self.ids.grid_right_bottom

        

        grid_created = False
        for child in self.children:
            for c in child.children:
                for c_sub in c.children:
                    for c_sub2 in c_sub.children:
                        for c_sub3 in c_sub2.children:
                            for c_sub4 in c_sub3.children:
                                if isinstance(c_sub4, Button):
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
            layout_right_header.size_hint = (None, None)
            
            layout_right_bottom.cols = len(persons)
            layout_right_bottom.size_hint = (None, None)


            price_total = 0.00

            height_item = mn_screen.height_item 
            width_item = mn_screen.width_item
            
            #Item Header
            label_item = Label(text='Item')
            row_objects.append(label_item)
            #layout_left.add_widget(label_item)
            layout_left_header.add_widget(label_item)

            #Price Header
            label_item = Label(text='Price')
            row_objects.append(label_item)
            #layout_left.add_widget(label_item)
            layout_left_header.add_widget(label_item)


            #Adds persons
            for i in range(len(persons)):
                label_item = Label(text=f'{persons[i].text}',size_hint=(None,None), height=height_item, width = width_item)
                row_objects.append(label_item)
                layout_right_header.add_widget(label_item)

            self.grid_objects.append(row_objects)

            #Add items
            for i in range(len(items)):
                row_objects = []
                label_item = Label(text=f'{items[i].text} : $',size_hint_y=None, height=height_item)
                label_price = Label(text=f'{prices[i].text}', size_hint_y=None, height=height_item)
                row_objects.append(label_item)
                row_objects.append(label_price)
                layout_left.add_widget(label_item)
                layout_left.add_widget(label_price)
                
                if prices[i].text != "":
                    price_total = price_total + float(prices[i].text)


                #Add Buttons
                for j in range(len(persons)):
                    button = Button(text='Add', size_hint=(None, None), height=height_item, width = width_item)
                    button.bind(on_press=self.change_color)
                    row_objects.append(button)
                    layout_right.add_widget(button)
                
                self.grid_objects.append(row_objects)

            

            #Subtotal
            row_objects = []
            row_objects.append(self.ids.label_bl_subtotal_item)
            row_objects.append(self.ids.label_bl_subtotal_price)
            for i in range(len(persons)):
                label_item_bottom = Label(text=f'0.00',size_hint=(None,None), height=height_item, width = width_item)
                layout_right_bottom.add_widget(label_item_bottom)
                row_objects.append(label_item_bottom)
            
            self.grid_objects.append(row_objects)

            #Tax
            row_objects = []
            row_objects.append(self.ids.label_bl_tax_item)
            row_objects.append(self.ids.label_bl_tax_price)
            for i in range(len(persons)):
                label_item_bottom = Label(text=f'0.00',size_hint=(None,None), height=height_item, width = width_item)
                layout_right_bottom.add_widget(label_item_bottom)
                row_objects.append(label_item_bottom)

            self.grid_objects.append(row_objects)

            #Tip
            row_objects = []
            row_objects.append(self.ids.label_bl_tip_item)
            row_objects.append(self.ids.label_bl_tip_price)
            for i in range(len(persons)):
                label_item_bottom = Label(text=f'0.00',size_hint=(None,None), height=height_item, width = width_item)
                layout_right_bottom.add_widget(label_item_bottom)
                row_objects.append(label_item_bottom)

            self.grid_objects.append(row_objects)

            #Grand Total
            row_objects = []
            row_objects.append(self.ids.label_bl_grandtotal_item)
            row_objects.append(self.ids.label_bl_grandtotal_price)
            for i in range(len(persons)):
                label_item_bottom = Label(text=f'0.00',size_hint=(None,None), height=height_item, width = width_item)
                layout_right_bottom.add_widget(label_item_bottom)
                row_objects.append(label_item_bottom)

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

        #update totals
        self.ids.label_bl_subtotal_price.text = str(f'{mn_screen.totals[0]:.2f}')
        self.ids.label_bl_tax_price.text = str(f'{mn_screen.totals[1]:.2f}')
        self.ids.label_bl_tip_price.text = str(f'{mn_screen.totals[2]:.2f}')
        self.ids.label_bl_grandtotal_price.text = str(f'{mn_screen.totals[3]:.2f}')

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
        self.update_totals()

    def update_totals(self):
        grid_objects = self.grid_objects

        row_st = len(grid_objects)-4
        row_tax = len(grid_objects)-3
        row_tip = len(grid_objects)-2
        row_gt = len(grid_objects)-1

        #for range in loops
        col_btn_start = 2
        col_btn_end = len(grid_objects[1])
        row_btn_start = 1
        row_btn_end = len(grid_objects)-4
        
        total_subtotal = float(grid_objects[row_st][1].text)
        total_tax = float(grid_objects[row_tax][1].text)
        total_tip = float(grid_objects[row_tip][1].text)
        total_grandtotal = float(grid_objects[row_gt][1].text)

        #subtotals
        for j in range(col_btn_start,col_btn_end):
            subtotal_object = grid_objects[row_st][j]
            subtotal_price = 0.00
            for i in range(row_btn_start,row_btn_end):
                if grid_objects[i][j].text != 'Add':
                    price_text = grid_objects[i][j].text
                    price_text = price_text.replace('$','')
                    subtotal_price = subtotal_price + float(price_text)
            subtotal_object.text = f'{subtotal_price:.2f}'
        
        #tax
        tax_factor = total_tax/total_subtotal
        tax_price = 0.00
        for j in range(col_btn_start, col_btn_end):
            tax_object = grid_objects[row_tax][j]
            subtotal_price = float(grid_objects[row_st][j].text)
            tax_price = subtotal_price * tax_factor
            tax_object.text = f'{tax_price:.2f}'
                
        #tip
        tip_factor = total_tip/total_subtotal
        tip_price = 0.00
        for j in range(col_btn_start,col_btn_end):
            tip_object = grid_objects[row_tip][j]
            subtotal_price = float(grid_objects[row_st][j].text)
            tip_price = subtotal_price * tip_factor
            tip_object.text = f'{tip_price:.2f}'

        #grandtotals
        for j in range(col_btn_start,col_btn_end):
            subtotal_price = float(grid_objects[row_st][j].text)
            tax_price = float(grid_objects[row_tax][j].text)
            tip_price = float(grid_objects[row_tip][j].text)
            grandtotal_price = subtotal_price + tax_price + tip_price
            grandtotal_object = grid_objects[row_gt][j]
            grandtotal_object.text = f'{grandtotal_price:.2f}'
                

    
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
