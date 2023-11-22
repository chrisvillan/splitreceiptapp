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
from kivy.uix.popup import Popup
from kivy.factory import Factory

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
    
    def add_item_left(self, text_item, text_price):
        data_grid = self.ids.mn_left_scview_grdlt
        
        txtinput_item = TextInput(text=text_item, size_hint=(1, None), height=self.height_item)
        label_mid = Label(text='$', size_hint=(0.1,None), height=self.height_item)
        txtinput_price = CurrencyTextInput(text=text_price, multiline=False, size_hint=(0.6, None), height=self.height_item)
        txtinput_price.bind(text=self.update_totals)
        
        data_grid.add_widget(txtinput_item)
        data_grid.add_widget(label_mid)
        data_grid.add_widget(txtinput_price)

        self.input_items.append([txtinput_item, txtinput_price])
        self.update_totals(txtinput_price, txtinput_price.text)
        
    def add_to_left_popup(self):
        popup = AddItemPopup(on_dismiss_callback=self.on_popup_dismiss, size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_popup_dismiss(self, text_item, text_price):
        print(f'Item: {text_item} | Price: {text_price}')
        self.add_item_left(text_item, text_price)

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

        self.ids.mn_left_tax_txinput.text = '7.75'
        self.ids.mn_left_tip_txinput.text = '15.00'

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
        
class GridScreen(Screen):
    def __init__(self, **kwargs):
        super(GridScreen, self).__init__(**kwargs)
        self.button_grid = []
        self.grid_objects = []

    def on_enter(self):
        mn_screen = self.manager.get_screen("main_screen")

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
                
        #Right Subtotal/Tax/Tip/Grandtotal
        row = 4
        for i in range(len(persons)*row):
            label_item = Label(text=f'0.00',size_hint=(None,None), height=height_item, width = width_item)
            layout_right_btm.add_widget(label_item)

        self.import_mnscreen_totals()
        self.update_ftr_totals()

    def import_mnscreen_totals(self):
        mn_screen = self.manager.get_screen("main_screen")
        #Import Left Subtotal/Tax/Tip/Grandtotal
        self.ids.grd_left_ftr_sbtotal_label_total.text = mn_screen.ids.mn_left_sbtotal_label_price.text
        self.ids.grd_left_ftr_tax_label_desc.text = mn_screen.ids.mn_left_tax_label_desc.text
        self.ids.grd_left_ftr_tax_label_total.text = mn_screen.ids.mn_left_tax_txinput.text
        self.ids.grd_left_ftr_tip_label_desc.text = mn_screen.ids.mn_left_tip_label_desc.text
        self.ids.grd_left_ftr_tip_label_total.text = mn_screen.ids.mn_left_tip_txinput.text
        self.ids.grd_left_ftr_grtotal_label_total.text = mn_screen.ids.mn_left_grtotal_label_price.text

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
        grd_right = self.grd_to_arr(self.ids.grd_right_scview_grdlt)
        grd_right_hdr = self.grd_to_arr(self.ids.grd_right_hdr_scview_grdlt)
        grd_right_ftr = self.grd_to_arr(self.ids.grd_right_ftr_scview_grdlt)
        
        grd_left = self.grd_to_arr(self.ids.grd_left_scview_grdlt)
        grd_left_ftr = self.get_left_ftr_arr()

        #Get factor
        tax_factor = self.extract_number(self.ids.grd_left_ftr_tax_label_desc.text)
        tax_factor = round(tax_factor/100,4)
        tip_factor = self.extract_number(self.ids.grd_left_ftr_tip_label_desc.text)
        tip_factor = round(tip_factor/100,4)

        #Person Totals
        for j in range(len(grd_right_hdr)):
            #Sub Totals
            subtotal = 0.00

            for i in range(len(grd_right)):
                item = grd_right[i][j]
                if item.text.replace('.','').isnumeric():
                    subtotal = round(subtotal + float(item.text), 2)
            
            label = grd_right_ftr[0][j]
            label.text = f'{subtotal:.2f}'

            #Tax
            row_tax = 1
            tax = round(subtotal * tax_factor, 2)
            label = grd_right_ftr[row_tax][j]
            label.text = f'{tax:.2f}'

            #Tip
            row_tip = 2
            tip = round(subtotal * tip_factor, 2)
            label = grd_right_ftr[row_tip][j]
            label.text = f'{tip:.2f}'

#Left Bottom Total called twice - need to update
        #Left Bottom Totals
        for i in range(len(grd_left_ftr)):
            total = 0.00
            for j in range(len(grd_right_hdr)):
                item = grd_right_ftr[i][j]
                if item.text.replace('.','').isnumeric():
                    total = round(total + float(item.text), 2)
            label = grd_left_ftr[i][2]
            label.text = f'{total:.2f}'

        #Balance tax and tip totals
        tax_total = float(self.ids.grd_left_ftr_tax_label_total.text)
        tax_bal = float(self.ids.grd_left_ftr_tax_label_bal.text)
        tip_total = float(self.ids.grd_left_ftr_tip_label_total.text)
        tip_bal = float(self.ids.grd_left_ftr_tip_label_bal.text)

        tax_arr = []
        tax_obj = grd_right_ftr[row_tax]
        for item in tax_obj:
            tax_arr.append(float(item.text))

        tip_arr = []
        tip_obj = grd_right_ftr[row_tip]
        for item in tip_obj:
            tip_arr.append(float(item.text))
			
        size_col = len(grd_left[0])
        qty_arr =[]
        for i in range(len(grd_left)):
            label = grd_left[i][size_col - 1]
            qty_arr.append(label.text)
            
        is_full = True
        for i in qty_arr:
            if i == '0':
                is_full = False
                break
        
        if is_full == True:
            tax_arr = self.balance_ftr_totals(tax_total, tax_bal, tax_arr)
            for i in range(len(tax_obj)):
                item = tax_obj[i]
                item.text = f'{tax_arr[i]:.2f}'      
            tip_arr = self.balance_ftr_totals(tip_total, tip_bal, tip_arr)
            for i in range(len(tip_obj)):
                item = tip_obj[i]
                item.text = f'{tip_arr[i]:.2f}'

        
        for j in range(len(grd_right_hdr)):
            #Grand Totals
            grandtotal = 0.00
            for i in range(len(grd_right_ftr)-1):
                item = grd_right_ftr[i][j]
                if item.text.replace('.','').isnumeric():
                    grandtotal = round(grandtotal + float(item.text), 2)
            
            label = grd_right_ftr[3][j]
            label.text = f'{grandtotal:.2f}'

        #Left Bottom Totals
        for i in range(len(grd_left_ftr)):
            total = 0.00
            for j in range(len(grd_right_hdr)):
                item = grd_right_ftr[i][j]
                if item.text.replace('.','').isnumeric():
                    total = round(total + float(item.text), 2)
            label = grd_left_ftr[i][2]
            label.text = f'{total:.2f}'
        
    def balance_ftr_totals(self, total, bal, arr):
        remainder = round(total - bal, 2)
        remainder = int(abs(remainder * 100))
        #Tax balance
        if bal < total:	
            t = len(arr) - 1
            while remainder != 0:
                if arr[t] != 0:
                    arr[t] = round(arr[t] + 0.01, 2)
                    remainder -= 1
                if t == 0:
                    t = len(arr) - 1
                else:
                    t -= 1
        elif bal > total:
            t = 0
            while remainder != 0:
                if arr[t] != 0:
                    arr[t] = round(arr[t] - 0.01, 2)
                    remainder -= 1
                if t == len(arr) - 1:
                    t = 0
                else:
                    t += 1
        return arr
    def grd_to_arr(self, Widget):
		#assumes 'lr-tb' orientation
        grd_lt = Widget
        grd_arr = []
        row_arr = []
        start = len(grd_lt.children)
        c = 0

        if len(grd_lt.children) > grd_lt.cols:
            is_multi = True
        else:
            is_multi = False

        for i in range(start, 0, -1):
            row_arr.append(grd_lt.children[i-1])
            c += 1
            if grd_lt.cols == c:
                c = 0
                if is_multi == True:
                    grd_arr.append(row_arr)
                    row_arr = []
                else:
                    grd_arr = row_arr	
                    row_arr = []

        return grd_arr

    def get_left_ftr_arr(self):
        ftr_bxlt = self.ids.grd_left_ftr_bxlt
        ftr_arr = []

        for i in range(len(ftr_bxlt.children), 0, -1):
            row = []
            bxlt = ftr_bxlt.children[i-1]
            for j in range(len(bxlt.children), 0, -1):
                row.append(bxlt.children[j-1])
            ftr_arr.append(row)

        return ftr_arr
    
    def print_grd_arr(self, Widget):
        layout = self.grd_to_arr(Widget)
        for row in layout:
            str_row = ""
            for item in row:
                str_row = str_row + " | " + item.text
            print(str_row)
            
    def extract_number(self, str_val):
        str_num = ''
        for char in str_val:
            if char.isdigit() or char =='.':
                str_num += char
        
        return float(str_num) if str_num else None
    
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

class AddItemPopup(Popup):
    def __init__(self,on_dismiss_callback, **kwargs):
        super(AddItemPopup, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.title = 'Enter Text'

        bxlt_top = BoxLayout(orientation='horizontal')
        self.txtinput_item = TextInput(hint_text='Item Description', size_hint_x=0.6)
        label = Label(text='$', font_size=24, size_hint_x=0.1)
        self.txtinput_price = CurrencyTextInput(hint_text='0.00', multiline='False', size_hint_x=0.3)
        bxlt_top.add_widget(self.txtinput_item)
        bxlt_top.add_widget(label)
        bxlt_top.add_widget(self.txtinput_price)


        bxlt_bot = BoxLayout(orientation='horizontal')
        btn_add = Button(text='Add Item', size_hint_x=0.8, on_press=self.dismiss_popup)
        btn_cancel = Button(text='Cancel', size_hint_x=0.2, on_release=self.close_popup)
        bxlt_bot.add_widget(btn_add)
        bxlt_bot.add_widget(btn_cancel)

        content_layout = BoxLayout(orientation='vertical')
        content_layout.add_widget(bxlt_top)
        content_layout.add_widget(bxlt_bot)

        self.content = content_layout

    def dismiss_popup(self, instance):
        # Call the on_dismiss_callback and pass the entered text
        self.on_dismiss_callback(self.txtinput_item.text, self.txtinput_price.text)
        self.dismiss()
    
    def close_popup(self, instance):
        self.dismiss()

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
