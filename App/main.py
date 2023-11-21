from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout  
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from functools import partial
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config

# To update for app deployment
# buildozer -v android debug
# Config.set('graphics', 'width', '540')
# Config.set('graphics', 'height', '1200')
# Config.write()
# print("WindowSize: " + str(Window.size))

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.input_items = []
        self.input_persons= []
        self.totals = {'subtotal':0.00, 'tax':0.00,'tip':0.00, 'grandtotal':0.00}

        window_width, window_height = Window.size
        self.height_item = window_height * 0.05
        self.width_item = window_width * 0.18519

    def add_to_right(self):
        data_grid = self.ids.mn_right_scview_grdlt
        height_item = self.height_item
        txtinput_pers = TextInput(hint_text='Person', size_hint=(1, None), height=height_item)
        txtinput_pers.background_color = [0.2,0.2,0.2,1]
        txtinput_pers.foreground_color=[1,1,1,1]

        data_grid.add_widget(txtinput_pers)
        self.input_persons.append(txtinput_pers)

    def add_to_left(self):
        data_grid = self.ids.mn_left_scview_grdlt
        
        txtinput_item = TextInput(hint_text='Item', size_hint=(1, None), height=self.height_item)
        label_mid = Label(text='$', size_hint=(0.1,None), height=self.height_item)
        txtinput_price = CurrencyTextInput(hint_text='Price', multiline=False, size_hint=(0.6, None), height=self.height_item)
        txtinput_price.bind(text=self.update_totals)
        
        data_grid.add_widget(txtinput_item)
        data_grid.add_widget(label_mid)
        data_grid.add_widget(txtinput_price)

        self.input_items.append([txtinput_item, txtinput_price])
        
    def add_to_left_preset(self):
        for i in range(10):
            self.add_to_left()
  
        for i in range(10):
            self.add_to_right()

        items = []
        prices = []
        for i in range(len(self.input_items)):
            items.append(self.input_items[i][0])
            prices.append(self.input_items[i][1])

        persons = self.input_persons

        for i in range(len(self.input_items)):
            items[i].text = f'Item {i+1}'
        
        prices[0].text = "10.00"
        prices[1].text = "10.00"
        prices[2].text = "10.00"
        prices[3].text = "10.00"
        prices[4].text = "10.00"
        prices[5].text = "10.00"
        prices[6].text = "10.00"
        prices[7].text = "10.00"
        prices[8].text = "10.00"
        prices[9].text = "10.00"

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

        self.ids.mn_left_tax_txinput.text = '10.00'
        self.ids.mn_left_tip_txinput.text = '20.00'

    #Need this function in case tax/tip is entered before items are inputted
    def update_taxtip(self):
        tax_txtinput = self.ids.mn_left_tax_txinput
        tip_txtinput = self.ids.mn_left_tip_txinput
        tax_txtinput.bind(text=self.update_totals)
        tip_txtinput.bind(text=self.update_totals)

    def update_totals(self, instance, text):
        prices = []
        for i in range(len(self.input_items)):
            prices.append(self.input_items[i][1])

        subtotal = 0.00
        grandtotal = 0.00
        tax = 0.00
        tip = 0.00
        
        tax_txtinput = self.ids.mn_left_tax_txinput
        tip_txtinput = self.ids.mn_left_tip_txinput

        for p in prices:
            if p.text != "":
                subtotal = subtotal + float(p.text)

        if subtotal != 0:
            if tax_txtinput.text != "":
                tax = float(tax_txtinput.text)
            if tip_txtinput.text != "":
                tip = float(tip_txtinput.text)
            
        if tax != 0:
            grandtotal = grandtotal + tax
        if tip != 0:
            grandtotal = grandtotal + tip
        
        if subtotal != 0:
            grandtotal = grandtotal + subtotal

            tax_factor = tax/subtotal
            tip_factor = tip/subtotal
            tax = tax_factor*100
            tip = tip_factor*100

        self.ids.mn_left_sbtotal_label_price.text = f'{subtotal:.2f}'
        self.ids.mn_left_tax_label_desc.text = f'Tax ({tax:.2f}%)'
        self.ids.mn_left_tip_label_desc.text = f'Tip ({tip:.2f}%)'
        self.ids.mn_left_grtotal_label_price.text = f'{grandtotal:.2f}'

        self.totals['subtotal'] = subtotal
        self.totals['tax'] = tax
        self.totals['tip'] = tip
        self.totals['grandtotal'] = grandtotal
        
class GridScreen(Screen):
    def __init__(self, **kwargs):
        super(GridScreen, self).__init__(**kwargs)
        self.button_grid = []
        self.grid_objects = []

    def on_enter(self):
        mn_screen = self.manager.get_screen("main_screen")
        grd_screen = self.manager.get_screen("grid_screen")

        items = mn_screen.input_items
        persons = mn_screen.input_persons

        layout_left = self.ids.grd_left_scview_grdlt
        layout_right = self.ids.grd_right_scview_grdlt
        layout_right_hdr = self.ids.grd_right_hdr_scview_grdlt
        layout_right_btm = self.ids.grd_right_ftr_scview_grdlt

#Need to add: save state of children

        #clears widgets
        layout_left.clear_widgets()
        layout_right.clear_widgets()
        layout_right_hdr.clear_widgets()
        layout_right_btm.clear_widgets()
        
        height_item = mn_screen.height_item
        width_item = mn_screen.width_item


        layout_left.cols = 3
        layout_right.cols = len(persons)

        layout_right_hdr.cols = len(persons)
        layout_right_hdr.size_hint = (None, None)
        
        layout_right_btm.cols = len(persons)
        layout_right_btm.size_hint = (None, None)

        #Adds persons
        row_objects = []
        for i in range(len(persons)):
            label_item = Label(text=f'{persons[i].text}',size_hint=(None,None), height=height_item, width = width_item)
            row_objects.append(label_item)
            layout_right_hdr.add_widget(label_item)
        
        #Add items
        for i in range(len(items)):
            row_objects = []
            label_item = Label(text=f'{items[i][0].text}', size_hint_x=0.5, size_hint_y=None, height=height_item)
            label_price = Label(text=f'{float(items[i][1].text):.2f}', size_hint_x=0.25, size_hint_y=None, height=height_item)
            label_qty = Label(text='0', size_hint_x=0.25, size_hint_y=None, height=height_item)
            
            layout_left.add_widget(label_item)
            layout_left.add_widget(label_price)
            layout_left.add_widget(label_qty)

            #Add Buttons
            for j in range(len(persons)):
                button = Button(text='Add', size_hint=(None, None), height=height_item, width = width_item)
                button.bind(on_press=self.change_color)
                layout_right.add_widget(button)
                
        #Subtotal/Tax/Tip/Grandtotal
        row = 4
        for i in range(len(persons)*row):
            label_item = Label(text=f'0.00',size_hint=(None,None), height=height_item, width = width_item)
            layout_right_btm.add_widget(label_item)
        
        self.update_ftr_totals()
    
    def change_color(self, instance):
        if instance.background_color == [0, 1, 0, 1]:
            instance.background_color = [1, 1, 1, 1]
        else:
            instance.background_color = [0, 1, 0, 1]
        self.update_btn_totals()

    def update_btn_totals(self):
        layout_right = self.ids.grd_right_scview_grdlt
        layout_right_hdr = self.ids.grd_right_hdr_scview_grdlt
        layout_left = self.ids.grd_left_scview_grdlt

        item_prices = []
        item_qtys = []

        #Get item prices and qty
        for i in range(len(layout_left.children)-2,0,-3):
            item_prices.append(layout_left.children[i])
            item_qtys.append(layout_left.children[i-1])
        
        mark = len(layout_right.children)-1
        for i in range(len(item_prices)):
            btn_grns = []
            for j in range(len(layout_right_hdr.children)):
                btn = layout_right.children[mark]
                if btn.background_color == [0, 1, 0, 1]:
                    btn_grns.append(btn)
                else:
                    btn.text = 'Add'
                mark -= 1
            
            item_qtys[i].text = str(len(btn_grns))

            if len(btn_grns) > 0:
                balance = float(item_prices[i].text)
                price = balance/len(btn_grns)
                price = int(price * 10**2)/(10**2)
                btn_prices = []
                for btn in btn_grns:
                    if balance >= price:
                        btn_prices.append(price)
                        balance = round(balance - price,2)

                #If remainder, spread out evenly
                if balance != 0:
                    #Floating limitation so need to convert to int
                    count = int(balance * 100)
                    p = 0
                    while count > 0:
                        btn_prices[p] = btn_prices[p] + 0.01
                        count -= 1
                        if p == len(btn_prices)-1:
                            p = 0
                        else:
                            p += 1

                for i in range(len(btn_prices)):
                    btn = btn_grns[i]
                    btn.text = f'{btn_prices[i]:.2f}'  

        self.update_ftr_totals()

    def update_ftr_totals(self):
        layout_right = self.ids.grd_right_scview_grdlt
        layout_right_hdr = self.ids.grd_right_hdr_scview_grdlt
        layout_right_ftr = self.ids.grd_right_ftr_scview_grdlt
        layout_left = self.ids.grd_left_scview_grdlt

        size_col = len(layout_right_hdr.children)
        size_row = 4
        #Person Totals
        for j in range(size_col):

            #Subtotals
            subtotal = 0.00
            start = len(layout_right.children) - 1 - j
            step = size_col*-1
            for b in range(start,0,step):
                btn = layout_right.children[b]
                if btn.text.replace('.','').isnumeric():
                    subtotal = round(subtotal + float(btn.text), 2)
            
            start = (len(layout_right_ftr.children)-1) - j
            layout_right_ftr.children[start].text = f'{subtotal:.2f}'

            #GrandTotal
            grandtotal = 0.00
            for i in range(3):
                start = (len(layout_right_ftr.children)-1) - j
                index = start + (step*i)
                print(layout_right_ftr.children[index].text)
                grandtotal = grandtotal + float(layout_right_ftr.children[index].text)

            index = size_col - 1 - j
            layout_right_ftr.children[index].text = f'{grandtotal:.2f}'
        
        
        #Left Totals
        label_totals = []
        label_totals.append(self.ids.grd_left_ftr_sbtotal_label_bal)
        label_totals.append(self.ids.grd_left_ftr_tax_label_bal)
        label_totals.append(self.ids.grd_left_ftr_tip_label_bal)
        label_totals.append(self.ids.grd_left_ftr_grtotal_label_bal)
        
        for i in range(size_row):
            total = 0.00
            start = len(layout_right_ftr.children) - 1 - (size_col*i)
            for p in range(start, start-size_col,-1):
                label = layout_right_ftr.children[p]
                total = total + float(label.text)

            label_totals[i].text = f'{total:.2f}'



                
class CurrencyTextInput(TextInput):
    def on_text(self, inst6ance, value):
        value = value.replace('.','')
        value = str(int(value))

        # Adds a period before the last two digits
        if len(value) >= 3:
            formatted_text = value[:-2] + '.' + value[-2:]
        else:
            if len(value) > 0:
                if len(value) == 2:
                    formatted_text = '0.' + value
                elif len(value) == 1:
                    formatted_text = '0.0' + value
            else: 
                formatted_text = value

        # Updates the text and cursor position
        self.text = formatted_text
        Clock.schedule_once(partial(self.do_cursor_movement, 'cursor_end'))
    
    def insert_text(self, substring, from_undo=False):
        # Allow only digits
        allowed_chars = set('0123456789')
        if all(char in allowed_chars for char in substring):
            return super(CurrencyTextInput, self).insert_text(substring, from_undo)
        else:
            return super(CurrencyTextInput, self).insert_text('', from_undo)


    
class SplitReceipt(App):
    def build(self):
        
        sm = ScreenManager()
        main_screen = MainScreen(name='main_screen')
        grid_screen = GridScreen(name='grid_screen')
        sm.add_widget(main_screen)
        sm.add_widget(grid_screen)
        return sm

if __name__ == '__main__':
    SplitReceipt().run()
