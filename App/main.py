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
from kivy.core.text import Label as CoreLabel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, BoxShadow, RoundedRectangle, Ellipse
from kivy.core.clipboard import Clipboard
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder

import os
import sys
import pprint
import json
# To update for app deployment
# buildozer -v android debug
# Config.set('graphics', 'width', '540')
# Config.set('graphics', 'height', '1200')
# Config.write()
# print("WindowSize: " + str(Window.size))


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        window_width, window_height = Window.size
        self.height_item = window_height * 0.05
        self.width_item = window_width * 0.18519
        self.items = []
        self.persons = []
        self.add_init = False
        self.checkbox_mode = False
        
        

    def on_enter(self):
        if self.name == 'main_screen':
            if self.add_init == False:
                Clock.schedule_once(lambda dt: self.additem_left_init(), 0.05)
                Clock.schedule_once(lambda dt: self.addperson_right_init(), 0.05)
                self.add_init = True

    def switch_to_grid_screen(self):
        if len(self.items) >= 2 and len(self.persons) >=2:
            self.manager.current = 'grid_screen'
            self.manager.transition.direction = "left"
        else:
            popup = WarningPopup(label_text='Please add more items/person\nMinimum of 2 items and 2 persons')
            popup.open()

    #Preset
    def add_preset_auto(self):
        preset_item = []
        preset_person = []

        preset_item.append(['Item A', '50.00'])
        preset_item.append(['Item B', '30.00'])
        preset_item.append(['Item C', '20.00'])

        preset_person.append('Alex')
        preset_person.append('Bob')
        preset_person.append('Chris')

        for item in preset_item:
            self.additem_left(item[0],item[1])
            
        for person in preset_person:
           self.addperson_right(person)

        tax_btn = self.ids.mn_left_tax_txinput
        tip_btn = self.ids.mn_left_tip_txinput
        tax_btn.text = "7.75"
        tip_btn.text = "15.00"
        
        self.update_totals()
 
    # Add Item
    def additem_left(self, text_item, text_price):
        left_grid = self.ids.mn_left_scview_grdlt
    
        bxlt = left_grid.children[0]
        bxlt_item = bxlt.children[0]
        txtinput_item = bxlt_item.children[2]
        txtinput_price = bxlt_item.children[0]

        txtinput_item.focus = True
        txtinput_item.text = text_item
        txtinput_price.focus = True
        txtinput_price.text = text_price
        txtinput_price.focus = False
  
    def additem_left_init(self):
        data_grid = self.ids.mn_left_scview_grdlt
        bxlt = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height_item)
        bxlt_item = ItemBoxLayoutAuto(on_dismiss_callback=self.additem_left_auto_dismiss, orientation='horizontal',size_hint=(1, None), height=self.height_item, item_height=self.height_item)
        
        bxlt.add_widget(bxlt_item)
        data_grid.add_widget(bxlt)

        txtinput_item = bxlt_item.children[2]
        txtinput_price = bxlt_item.children[0]
        
        my_dict ={
            'id': bxlt_item,
            'item_id': txtinput_item,
            'price_id': txtinput_price,
            'item_val': '',
            'price_val': 0.0,
            'row': 0
            }    
    
        self.items.append(my_dict)
        
    def additem_left_auto_dismiss(self, state):
        
        data_grid = self.ids.mn_left_scview_grdlt
        bxlt_prev = data_grid.children[0]
        bxlt_item_prev = bxlt_prev.children[0]
        txtinput_item = bxlt_item_prev.children[2]
        txtinput_price = bxlt_item_prev.children[0]
        price = 0.00

        self.change_dict_val(bxlt_item_prev, 'item_val',txtinput_item.text,self.items)

        if txtinput_price.text != '':
            price = float(txtinput_price.text)
        
        self.change_dict_val(bxlt_item_prev, 'price_val',price,self.items)

        bxlt = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height_item)
        bxlt_item = ItemBoxLayoutAuto(on_dismiss_callback=self.additem_left_auto_dismiss, orientation='horizontal',size_hint=(1, None), height=self.height_item, item_height=self.height_item)
        
        bxlt.add_widget(bxlt_item)
        data_grid.add_widget(bxlt)

        txtinput_item = bxlt_item.children[2]
        txtinput_price = bxlt_item.children[0]

        my_dict ={
            'id': bxlt_item,
            'item_id': txtinput_item,
            'price_id': txtinput_price,
            'item_val': '',
            'price_val': 0.0,
            'row': 0
            }    
    
        self.items.append(my_dict)

        if state == "Enter":
            txtinput = bxlt_item.children[2]
            txtinput.focus = True

        self.update_totals()

         
    # Add Person
    def addperson_right(self, text_person):
        right_grid = self.ids.mn_right_scview_grdlt

        bxlt = right_grid.children[0]
        bxlt_pers = bxlt.children[0]
        txtinput_person = bxlt_pers.children[0]

        txtinput_person.focus = True
        txtinput_person.text = text_person
        txtinput_person.focus = False

    def addperson_right_init(self):
        data_grid = self.ids.mn_right_scview_grdlt
        
        bxlt = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height_item)
        bxlt_pers = BoxLayoutType2(orientation='horizontal',size_hint=(1, None), height=self.height_item)
        txtinput_pers = PersonTextInputAuto(on_dismiss_callback=self.addperson_right_auto_dismiss, size_hint=(1, None), height=self.height_item)
        
        bxlt_pers.add_widget(txtinput_pers)
        bxlt.add_widget(bxlt_pers)
        data_grid.add_widget(bxlt)

        my_dict = {
            'id': bxlt_pers,
            'person_id': txtinput_pers,
            'value': '',
            'row': 0
        }
        self.persons.append(my_dict)

    def addperson_right_auto_dismiss(self,state):
        data_grid = self.ids.mn_right_scview_grdlt
        bxlt = data_grid.children[0]
        bxlt_pers_prev = bxlt.children[0]
        txtinput_pers = bxlt_pers_prev.children[0]

        self.change_dict_val(bxlt_pers_prev,'value',txtinput_pers.text,self.persons)
        
        bxlt = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height_item)
        bxlt_pers = BoxLayoutType2(orientation='horizontal',size_hint=(1, None), height=self.height_item)
        txtinput_pers = PersonTextInputAuto(on_dismiss_callback=self.addperson_right_auto_dismiss,  multiline=False, size_hint=(1, None), height=self.height_item)
        
        bxlt_pers.add_widget(txtinput_pers)
        bxlt.add_widget(bxlt_pers)
        data_grid.add_widget(bxlt)

        my_dict = {
            'id': bxlt_pers,
            'person_id': txtinput_pers,
            'value': '',
            'row': 0
        }
        self.persons.append(my_dict)

        if state == "Enter":
            txtinput_pers.focus = True

    # Price calculations
    def update_tax_popup(self):
        taxtip_prices = []
        taxtip_prices.append(self.ids.mn_left_tax_txinput.text)
        taxtip_prices.append(self.ids.mn_left_tip_txinput.text)
        popup = TaxTipPopup(on_dismiss_callback=self.update_taxtip_popup_dismiss, prices=taxtip_prices)
        popup.txtinput_tax_price.focus = True
        popup.open()    
    
    def update_tip_popup(self):
        taxtip_prices = []
        taxtip_prices.append(self.ids.mn_left_tax_txinput.text)
        taxtip_prices.append(self.ids.mn_left_tip_txinput.text)
        popup = TaxTipPopup(on_dismiss_callback=self.update_taxtip_popup_dismiss, prices=taxtip_prices)
        popup.txtinput_tip_price.focus = True
        popup.open() 

    def update_taxtip_popup_dismiss(self,tax_desc, tax_price, tip_desc, tip_price):
        tax_btn = self.ids.mn_left_tax_txinput
        tip_btn = self.ids.mn_left_tip_txinput
        tax_btn.text = tax_price.text
        tip_btn.text = tip_price.text
        self.update_totals()

    def update_totals(self):

        items_arr = []
        for my_dict in self.items:
            if my_dict['item_val'] != '':
                if my_dict['price_val'] != 0.0:
                    items_arr.append([my_dict['item_val'], my_dict['price_val']])
                else:
                    items_arr.append([my_dict['item_val'], 0.0])
            else:
                if my_dict['price_val'] != 0.0:
                    items_arr.append([my_dict['item_val'], my_dict['price_val']])
        
        prices = []
        for i in range(len(items_arr)):
            prices.append(items_arr[i][1])

        subtotal = 0.00
        grandtotal = 0.00
        tax = 0.00
        tip = 0.00

        tax_txtinput = self.ids.mn_left_tax_txinput
        tip_txtinput = self.ids.mn_left_tip_txinput

        for p in prices:
            subtotal = subtotal + p

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

    # data dict functions
    def print_dict(self):
        print('\n--------------------ITEMS--------------------\n')
        for my_dict in self.items:
            pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
            print('\n')

        print('\n--------------------PERSON--------------------\n')
        for my_dict in self.persons:
            pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
            print('\n')

    def change_dict_val(self, id, key, val, grid):
        for my_dict in grid:
            if my_dict['id'] == id:
                my_dict[key] = val
                break
    
    def get_dict_val(self,id,key, grid):
        for my_dict in grid:
            if my_dict['id'] == id:
                return my_dict[key]
            
    def delete_dict(self, id, grid):
        for i in range(len(grid)):
            my_dict = grid[i]
            if my_dict['id'] == id:
                grid.pop(i)
                break

    # Edit Items/Persons
    def add_checkbox(self):
        data_grid_left = self.ids.mn_left_scview_grdlt
        data_grid_right = self.ids.mn_right_scview_grdlt

        mn_left_bxlt = self.ids.mn_left_bxlt
        mn_right_bxlt = self.ids.mn_right_bxlt
        mn_left_bxlt.size_hint_x = 0.6
        mn_right_bxlt.size_hint_x = 0.4

        if self.checkbox_mode == False:
            for i in range(len(data_grid_left.children)):
                bxlt = data_grid_left.children[i]
                bxlt.spacing = 10
                if i != 0:
                    chkbox = CheckBox(size_hint_x=0.1)
                    bxlt.add_widget(chkbox,1)
                else:
                    bxlt_empty = BoxLayout(size_hint_x=0.1)
                    bxlt.add_widget(bxlt_empty,1)
            
            for i in range(len(data_grid_right.children)):
                bxlt = data_grid_right.children[i]
                bxlt.spacing = 10
                # bxlt.padding = (10,0,10,0)
                if i != 0:
                    chkbox = CheckBox(size_hint_x=0.1)
                    bxlt.add_widget(chkbox)
                else:
                    bxlt_empty = BoxLayout(size_hint_x=0.1)
                    bxlt.add_widget(bxlt_empty)

            mn_bxlt = self.ids.mn_bxlt
            self.bxlt_btn = BoxLayout(orientation='horizontal', size_hint_y=0.05, padding=(0,10,0,0))
            self.btn_clear_chkbox = ButtonType3(text='Clear Selected', size_hint_x=0.7)
            self.btn_clear_chkbox.bind(on_release=self.clear_selected)

            btn_clear_all = ButtonType3(text='Select All', size_hint_x=0.2)

            self.bxlt_btn.add_widget(self.btn_clear_chkbox)
            self.bxlt_btn.add_widget(btn_clear_all)
            mn_bxlt.add_widget(self.bxlt_btn, len(mn_bxlt.children)-1)
            self.checkbox_mode = True
        else:
            #unselect checkboxes
            for bxlt in data_grid_left.children:
                wdgt = bxlt.children[1]
                if isinstance(wdgt, CheckBox):
                    if wdgt.active == True:
                        wdgt.active = False

            for bxlt in data_grid_right.children:
                wdgt = bxlt.children[0]
                if isinstance(wdgt, CheckBox):
                    if wdgt.active == True:
                        wdgt.active = False

            self.btn_clear_chkbox.trigger_action(duration=0.05)
            self.checkbox_mode = False

    def clear_selected(self, instance):
        data_grid_left = self.ids.mn_left_scview_grdlt
        data_grid_right = self.ids.mn_right_scview_grdlt

        #remove selected items
        bxlt_delete = []
        for bxlt in data_grid_left.children:
            wdgt = bxlt.children[1]
            if isinstance(wdgt, CheckBox):
                if wdgt.active == True:
                    bxlt_delete.append([bxlt, bxlt.children[0]])

        for i in range(len(bxlt_delete)):
            data_grid_left.remove_widget(bxlt_delete[i][0])
            self.delete_dict(bxlt_delete[i][1], self.items)

        #remove selected persons
        bxlt_delete = []
        for bxlt in data_grid_right.children:
            wdgt = bxlt.children[0]
            if isinstance(wdgt, CheckBox):
                if wdgt.active == True:
                    bxlt_delete.append([bxlt, bxlt.children[1]])

        for i in range(len(bxlt_delete)):
            data_grid_right.remove_widget(bxlt_delete[i][0])
            self.delete_dict(bxlt_delete[i][1], self.persons)

        #remove button
        mn_bxlt = self.ids.mn_bxlt
        mn_bxlt.remove_widget(self.bxlt_btn)

        #remove checkboxes
        for bxlt in data_grid_left.children:
            wdgt = bxlt.children[1]
            bxlt.remove_widget(wdgt)

        for bxlt in data_grid_right.children:
            wdgt = bxlt.children[0]
            bxlt.remove_widget(wdgt)
        
        self.checkbox_mode = False

        mn_left_bxlt = self.ids.mn_left_bxlt
        mn_right_bxlt = self.ids.mn_right_bxlt
        mn_left_bxlt.size_hint_x = 0.7
        mn_right_bxlt.size_hint_x = 0.3
        self.update_totals()

    # Clear Items
    def clear_all_items(self):
        self.persons= []
        self.ids.mn_right_scview_grdlt.clear_widgets()
        self.items = []
        self.ids.mn_left_scview_grdlt.clear_widgets()

        tax_btn = self.ids.mn_left_tax_txinput
        tip_btn = self.ids.mn_left_tip_txinput
        tax_btn.text = '0.00'
        tip_btn.text = '0.00'

        self.additem_left_init()
        self.addperson_right_init()
        self.update_totals()

    def clear_all_items_popup(self):
        popup = ConfirmPopup(on_dismiss_callback=self.clear_all_items, label_text='Clear all?')
        popup.open()

    def clear_left_items_popup(self):
        popup = ConfirmPopup(on_dismiss_callback=self.clear_left_items, label_text='Clear all items?')
        popup.open()

    def clear_left_items(self):
        self.input_items = []
        self.ids.mn_left_scview_grdlt.clear_widgets()
    
    def clear_right_items_popup(self):
        popup = ConfirmPopup(on_dismiss_callback=self.clear_right_items, label_text='Clear all persons?')
        popup.open()

    def clear_right_items(self):
        self.input_persons= []
        self.ids.mn_right_scview_grdlt.clear_widgets()

class GridScreen(Screen):
    def __init__(self, **kwargs):
        super(GridScreen, self).__init__(**kwargs)
        self.button_grid = []
        self.grid_objects = []
        self.items = []
        self.persons = []
        
    def on_enter(self):
        mn_screen = self.manager.get_screen("main_screen")

        #Remove empty values in dict array
        self.items = []
        for my_dict in mn_screen.items:
            if my_dict['item_val'] == '' and my_dict['price_val'] == 0.0:
                pass
            else:
                self.items.append(my_dict)
        
        self.persons = []
        for my_dict in mn_screen.persons:
            if my_dict['value'] != '':
                self.persons.append(my_dict)


        self.print_dict()
        new_btn_grd = []

        layout_left = self.ids.grd_left_scview_grdlt
        layout_right = self.ids.grd_right_scview_grdlt
        layout_right_hdr = self.ids.grd_right_hdr_scview_grdlt
        layout_right_btm = self.ids.grd_right_ftr_scview_grdlt

        #clears widgets
        layout_left.clear_widgets()
        layout_right.clear_widgets()
        layout_right_hdr.clear_widgets()
        layout_right_btm.clear_widgets()
        
        self.height_item = mn_screen.height_item
        self.width_item = mn_screen.width_item

        layout_right.cols = len(self.persons)

        layout_right_hdr.cols = len(self.persons)
        layout_right_hdr.size_hint = (None, None)
        
        layout_right_btm.cols = len(self.persons)
        layout_right_btm.size_hint = (None, None)

        #Adds self.persons
        row_objects = []
        for i in range(len(self.persons)):
            label_item = ButtonType4(text=self.persons[i]['value'],size_hint=(None,None), height=self.height_item, width = self.width_item)
            label_item.bind(on_release=self.generate_summary)
            row_objects.append(label_item)
            layout_right_hdr.add_widget(label_item)
        
        #Add self.items
        for i in range(len(self.items)):
            row_objects = []
            bxlt = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.height_item)
            
            label_item = Label(text=self.items[i]['item_val'], size_hint_x=0.5)
            label_price = Label(text=str(self.items[i]['price_val']), size_hint_x=0.25)
            label_qty = Label(text='0', size_hint_x=0.25)
            
            bxlt.add_widget(label_item)
            bxlt.add_widget(label_price)
            bxlt.add_widget(label_qty)
            layout_left.add_widget(bxlt)

            Clock.schedule_once(lambda dt, bxlt=bxlt: self.align_label_bxlt(bxlt), 0.05)
            
            #Add Buttons
            for j in range(len(self.persons)):

                bxlt = RelativeLayout(size_hint=(None, None), height=self.height_item, width = self.width_item)
                button = ButtonType4(text='Add' )
                button.bind(on_press=self.change_color)
                label_qty = Label(text='1')
                
                # label_qty.halign = 'right'
                # label_qty.valign = 'top'
                
                bxlt.add_widget(button)
                bxlt.add_widget(label_qty)
                
                layout_right.add_widget(bxlt)

                my_dict = {
                    'id': button,
                    'state': False,
                    'lock': False,
                    'modifier': 1,
                    'modifier_id': label_qty,
                    'modifier_texture_size': [0,0],
                    'value': 0.00,
                    'row': i,
                    'col': j,
                    'item_bxlt': self.items[i]['id'],
                    'person_bxlt': self.persons[j]['id']
                }
                new_btn_grd.append(my_dict)
        
        Clock.schedule_once(lambda dt, bxlt=bxlt: self.align_label_btn(layout_right), 0.05)

        merge_btn_grd = self.merge_btn_grd(self.button_grid, new_btn_grd)
        self.button_grid = []
        self.button_grid = merge_btn_grd


        # print('\n--------------------MERGED GRID--------------------\n')
        # for my_dict in merge_btn_grd:
        #     pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
        #     print('\n')
        #     label = my_dict['modifier_id']
        #     label.color = [1,1,1,1]

        #Right Subtotal/Tax/Tip/Grandtotal
        row = 4
        label_total = self.ids.grd_left_ftr_sbtotal_label_total

        for i in range(len(self.persons)*row):
            label_item = Label(text=f'0.00',size_hint=(None,None), height=label_total.height, width = self.width_item)
            layout_right_btm.add_widget(label_item)
        
        self.import_mnscreen_totals()
        self.update_ftr_totals()
        Clock.schedule_once(lambda dt: self.load_btn_state(), 0.05)
    
    def print_dict(self):
        print('\n--------------------ITEMS--------------------\n')
        for my_dict in self.items:
            pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
            print('\n')

        print('\n--------------------PERSON--------------------\n')
        for my_dict in self.persons:
            pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
            print('\n')

    def merge_btn_grd(self, old_grd, new_grd):
        if len(old_grd) > 0:
            for old_dict in old_grd:
                old_item_bxlt = old_dict['item_bxlt']
                old_person_bxlt = old_dict['person_bxlt']

                for new_dict in new_grd:
                    new_item_bxlt = new_dict['item_bxlt']
                    new_person_bxlt = new_dict['person_bxlt']

                    if old_item_bxlt == new_item_bxlt and old_person_bxlt == new_person_bxlt:
                        new_dict['state'] = old_dict['state']
                        new_dict['lock'] = old_dict['lock']
                        new_dict['modifier'] = old_dict['modifier']
                        new_dict['value'] = old_dict['value']
                        new_dict['modifier_texture_size'] = old_dict['modifier_texture_size']
        
        return new_grd
    
    def load_btn_state(self):
        btn_grd = self.button_grid
        
        for my_dict in btn_grd:
            # pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
            # print('\n')
            if my_dict['state'] == True:
                btn = my_dict['id']
                self.change_color(btn)

            if my_dict['modifier'] != 1:
                btn = my_dict['id']
                label = my_dict['modifier_id']
                label.text = str(my_dict['modifier'])
                label.color = [1,1,1,1]

                row = self.get_dict_val(btn,'row')
                self.update_label_row(row)
            
            if my_dict['modifier'] == 'C':
                label = my_dict['modifier_id']
                label.text = str(my_dict['modifier'])
                btn = my_dict['id']
                btn.text = my_dict['value']
                self.show_label_modifier(btn, label)

    def align_label_btn(self, layout_right):
        btn_arr = []
        for ftlt in layout_right.children:
            # ftlt = bxlt.children[i-1]
            label = ftlt.children[0]
            btn = ftlt.children[1]
            label.text_size = label.size
            
            x_pos = ftlt.width-label.texture_size[0]
            y_pos = ftlt.height-label.texture_size[1]
            label.pos = (x_pos, y_pos)
            label.color = [1,1,1,0]

            self.change_dict_val(btn, 'modifier_texture_size', label.texture_size)
            btn_arr.append(btn)

        # count = 0
        # for my_dict in self.button_grid:
        #     pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(my_dict)
        #     print('\n')
        #     label = self.get_dict_val(btn_arr[count],'modifier_id')
        #     label.color = [1,1,1,1]
        #     count += 1

    def align_label_bxlt(self, bxlt):
        label_item = bxlt.children[len(bxlt.children)-1]
        label_price = bxlt.children[len(bxlt.children)-2]
        label_qty = bxlt.children[len(bxlt.children)-3]

        label_item.text_size = label_item.size
        label_price.text_size = label_price.size
        label_qty.text_size = label_qty.size

        label_item.halign = 'center'
        label_price.halign = 'right'
        label_qty.halign = 'center'

        label_item.valign = 'middle'
        label_price.valign = 'middle'
        label_qty.valign = 'middle'

        # label_qty.padding = 0,0,20,0
        # bxlt.padding = 5,0,5,0

    def import_mnscreen_totals(self):
        mn_screen = self.manager.get_screen("main_screen")
        #Import Left Subtotal/Tax/Tip/Grandtotal
        self.ids.grd_left_ftr_sbtotal_label_total.text = mn_screen.ids.mn_left_sbtotal_label_price.text
        self.ids.grd_left_ftr_tax_label_desc.text = mn_screen.ids.mn_left_tax_label_desc.text
        self.ids.grd_left_ftr_tax_label_total.text = mn_screen.ids.mn_left_tax_txinput.text
        self.ids.grd_left_ftr_tip_label_desc.text = mn_screen.ids.mn_left_tip_label_desc.text
        self.ids.grd_left_ftr_tip_label_total.text = mn_screen.ids.mn_left_tip_txinput.text
        self.ids.grd_left_ftr_grtotal_label_total.text = mn_screen.ids.mn_left_grtotal_label_price.text

    def change_dict_val(self, id, key, val):
        for my_dict in self.button_grid:
            if my_dict['id'] == id:
                my_dict[key] = val
                break
    
    def get_dict_val(self,id,key):
        for my_dict in self.button_grid:
            if my_dict['id'] == id:
                return my_dict[key]

    def get_all_instance(self, key, val):
        arr = []
        for my_dict in self.button_grid:
            if my_dict[key] == val:
                arr.append(my_dict)
        return arr

    def change_color(self, instance):
        grdlayout = instance.parent
        index = instance.parent.children.index(instance)
        instance.parent.remove_widget(instance)
        
        if isinstance(instance, ButtonType4):
            new_button = ButtonType6(on_dismiss_callback=self.get_btn_state, text='', size_hint=(None, None), height=self.height_item, width = self.width_item)
            # new_button.bind(on_release = self.change_color)
            self.change_dict_val(instance, 'id', new_button)
            self.change_dict_val(new_button,'state', True)
            # row = self.get_dict_val(new_button,'row')
            # self.update_label_row(row)
        else:
            new_button = ButtonType4(text='Add', size_hint=(None, None), height=self.height_item, width = self.width_item)
            new_button.bind(on_press=self.change_color)

            self.change_dict_val(instance, 'id', new_button)
            self.change_dict_val(new_button,'state', False)
            self.change_dict_val(new_button, 'value', '0.00')
            self.change_dict_val(new_button, 'modifier', '1')
            self.change_dict_val(new_button, 'lock', False)
            label = self.get_dict_val(new_button, 'modifier_id')
            label.text = '1'
            label.color = [1,1,1,0]
            label.canvas.before.clear()

        row = self.get_dict_val(new_button,'row')
        self.update_label_row(row)

        grdlayout.add_widget(new_button, index)
        # for btn in self.button_grid:
        #     # pprint.pprint(btn)
        #     pprint.PrettyPrinter(indent=4,sort_dicts=False).pprint(btn)
        self.update_btn_totals()

    def get_btn_state(self, id, state):
        if state == 'LONG PRESS':
            label = self.get_dict_val(id, 'modifier_id')
            popup = ButtonPopup(on_dismiss_callback=self.update_btn, btn_id=id, lbl_id=label)
            popup.open() 
        else:
            self.change_color(id)
    
    def show_label_modifier(self, btn, label):
        lbl_texture_size = self.get_dict_val(btn, 'modifier_texture_size')
        max_size = max(lbl_texture_size[0],lbl_texture_size[1])
        x_pos = btn.width-lbl_texture_size[0]
        y_pos = btn.height-lbl_texture_size[1]
        # label.pos = (x_pos, y_pos)
        
        circle_pos = [x_pos-(lbl_texture_size[0]/2),y_pos]
        circle_size = [max_size,max_size]

        label.canvas.before.clear()
        label.color = [1,1,1,1]
        
        with label.canvas.before:
            Color(245/255,73/255,156/255,1)  # Set the color of the circle (red in this case)
            circle = Ellipse(size=[max_size,max_size], pos=(x_pos-(lbl_texture_size[0]/2),y_pos))

    def update_label_row(self, row):
        row_arr = self.get_all_instance('row', row)
        label_on = False
        label_lock = False
        for my_dict in row_arr:
            if my_dict['state'] == True:
                label = my_dict['modifier_id']
                if label.color == [1,1,1,1]:
                    label_on = True
            if my_dict['lock'] == True:
                label_lock = True

        if label_on == True:
            for my_dict in row_arr:
                if my_dict['state'] == True:
                    btn = my_dict['id']
                    label = my_dict['modifier_id']
                    # label.color = [1,1,1,1]
                    self.show_label_modifier(btn,label)            

    def update_btn(self, btn_id, price_text, count_text):
        price_change = False
        count_change = False
        label = self.get_dict_val(btn_id, 'modifier_id')
        if btn_id.text != price_text:
            price_change = True
        if label.text != count_text:
            count_change = True
        
        if price_change == True:
            # print('PRICE_CHANGE')
            btn_id.text = price_text
            self.change_dict_val(btn_id, 'value', price_text)
            self.change_dict_val(btn_id, 'lock', True)
            self.change_dict_val(btn_id, 'modifier', 'C')
            label.color=(1,1,1,1)
            label.text = 'C'
            row = self.get_dict_val(btn_id,'row')
            self.update_label_row(row)
        if count_change == True:
            # print('COUNT_CHANGE')
            label.text = count_text
            self.change_dict_val(btn_id, 'modifier', count_text)
            if label.text != 1:
                label.color=(1,1,1,1)
                row = self.get_dict_val(btn_id,'row')
                self.update_label_row(row)
            else:
                label.color = (1,1,1,0)
            
        if price_change == True or count_change == True:
            self.update_btn_totals()

        if price_change == False and count_text == '1':
            if self.get_dict_val(btn_id, 'lock') == True:
                label.color=(1,1,1,1)
                label.text = 'C'
                row = self.get_dict_val(btn_id,'row')
                self.update_label_row(row)

    def update_btn_totals(self):
        #self.button_grid
        grd_right = self.get_btn_arr()
        layout_left = self.get_left_arr()

        item_prices = []
        item_qtys = []

        #Get item prices and qty
        for i in range(len(layout_left)):
            row = layout_left[i]
            item_prices.append(row[len(row)-2])
            item_qtys.append(row[len(row)-1])
        
        for i in range(len(item_prices)):
            btn_active = []
            btn_lock_price_total = 0.00
            btn_modifier_count = 0
            for j in range(len(grd_right[i])):
                btn = grd_right[i][j][0]
                btn_lock = self.get_dict_val(btn, 'lock')
                if type(btn) is ButtonType6:
                    if btn_lock == False:
                        btn_active.append(btn)
                    else:
                        if btn.text != '':
                            btn_lock_price_total = btn_lock_price_total + float(btn.text)
                else:
                    btn.text = 'Add'
            
            item_qtys[i].text = str(len(btn_active))

            if len(btn_active) > 0:
                balance = float(item_prices[i].text)
                balance = balance - btn_lock_price_total
                for btn in btn_active:
                    count = int(self.get_dict_val(btn, 'modifier'))
                    btn_modifier_count = btn_modifier_count + count

                price = balance/btn_modifier_count
                price = int(price * 10**2)/(10**2)
                btn_prices = []
                btn_modifier_count = 0
                
                for btn in btn_active:
                    if balance >= price:
                        modifier = int(self.get_dict_val(btn, 'modifier'))
                        btn_price = price * modifier
                        btn_prices.append(btn_price)
                        balance = round(balance - btn_price,2)

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
                    btn = btn_active[i]
                    btn.text = f'{btn_prices[i]:.2f}'  
                    self.change_dict_val(btn,'value', btn_prices[i])

        self.update_ftr_totals()
    
    def update_ftr_totals(self):
        grd_right = self.get_btn_arr()
        grd_right_hdr = self.grd_to_arr(self.ids.grd_right_hdr_scview_grdlt)
        grd_right_ftr = self.grd_to_arr(self.ids.grd_right_ftr_scview_grdlt)
        
        grd_left = self.get_left_arr()
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
                item = grd_right[i][j][0]
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
    
    def get_btn_arr(self):
        bxlt = self.ids.grd_right_scview_grdlt
        arr = []
        row = []
        col_size = self.ids.grd_right_scview_grdlt.cols
        count = 0

        for i in range(len(bxlt.children), 0, -1):
            ftlt = bxlt.children[i-1]
            btn = ftlt.children[len(ftlt.children)-1]
            lbl = ftlt.children[0]
            count += 1
        
            row.append([btn,lbl])
            if count == col_size:
                arr.append(row)
                row = []
                count = 0
        # print(arr)
        return(arr)

    def get_left_arr(self):
        left_bxlt = self.ids.grd_left_scview_grdlt
        arr = []
        row = []

        
        for i in range(len(left_bxlt.children), 0, -1):
            bxlt = left_bxlt.children[i-1]
            for c in range(len(bxlt.children), 0, -1):
                row.append(bxlt.children[c-1])
            arr.append(row)
            row = []
        
        return(arr)
    
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
    
    def generate_summary(self,btn):
        index = 0
        grd_right_hdr = self.grd_to_arr(self.ids.grd_right_hdr_scview_grdlt)

        for i in range(len(grd_right_hdr)):
            if btn == grd_right_hdr[i]:
                index = i
        
        summary = self.get_person_total(index)

        popup = SummaryPopup(label_text=summary)
        popup.open()
    
    def generate_all_summary(self):
        index = 0
        grd_right_hdr = self.grd_to_arr(self.ids.grd_right_hdr_scview_grdlt)
        summary = ''
        for i in range(len(grd_right_hdr)):
            if i == 0:
                summary = self.get_person_total(i)
            else:
                summary = summary + '\n\n' + self.get_person_total(i)

        popup = SummaryPopup(label_text=summary)
        popup.open()

    def get_person_total(self,index_pers):
        grd_right = self.get_btn_arr()
        grd_right_hdr = self.grd_to_arr(self.ids.grd_right_hdr_scview_grdlt)
        grd_right_ftr = self.grd_to_arr(self.ids.grd_right_ftr_scview_grdlt)

        grd_left = self.get_left_arr()
        grd_left_ftr = self.get_left_ftr_arr()

        items = []
        prices = []

        for i in range(len(grd_right)):
                item = grd_right[i][index_pers][0]
                if item.text.replace('.','').isnumeric():
                    item_desc = grd_left[i][0]
                    items.append(item_desc.text)
                    prices.append(item.text)
                    
        subtotal = grd_right_ftr[0][index_pers].text
        tax_desc = grd_left_ftr[1][0].text
        tax = grd_right_ftr[1][index_pers].text
        tip_desc = grd_left_ftr[2][0].text
        tip = grd_right_ftr[2][index_pers].text
        grandtotal = grd_right_ftr[3][index_pers].text

        summary = grd_right_hdr[index_pers].text + ':'
        for i in range(len(items)):
            summary = summary + f'\n{items[i]}: ${prices[i]}'
        summary = summary + f'\nSubTotal: ${subtotal}'
        summary = summary + f'\n{tax_desc}: ${tax}'
        summary = summary + f'\n{tip_desc}: ${tip}'
        summary = summary + f'\nGrandTotal: ${grandtotal}'

        return summary

class ButtonType6(Button):
    def __init__(self, on_dismiss_callback, **kwargs):
        super(ButtonType6, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.scheduled_event = None
        self.my_state = False
        self.my_press = ''
    def on_press(self):
        self.scheduled_event = Clock.schedule_once(lambda dt: self.my_function(), 0.5)

    def on_release(self):
        if self.my_state == False:
            self.my_press = 'SHORT PRESS'
            self.on_dismiss_callback(self, self.my_press)

        if self.my_press == 'LONG PRESS':
            self.my_state = False
        self.scheduled_event.cancel()
 
    def my_function(self):
        self.my_state = True
        self.my_press = 'LONG PRESS'
        self.on_dismiss_callback(self, self.my_press)

#ButtonPopup - need to prevent custom input from over total
#if custom input is the total = make popup warning and delete all other buttons
class ButtonPopup(Popup):
    def __init__(self, on_dismiss_callback, btn_id, lbl_id, **kwargs):
        super(ButtonPopup, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.original_btn_id = btn_id
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.9, 0.3)
        self.pos_hint = {"top": 0.7}
        self.initial_val = btn_id.text
        if lbl_id.text == 'C':
            self.initial_modifer = '1'
        else:
            self.initial_modifer = lbl_id.text
        bxlt = BoxLayoutType1(orientation='vertical', spacing=10, padding =10)
        bxlt_top = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        bxlt_mid = BoxLayout(orientation = 'vertical', size_hint_y=0.6, spacing=10)
        bxlt_mid_top = BoxLayout(orientation='horizontal', spacing=10)
        bxlt_mid_bot = BoxLayout(orientation='horizontal')
        bxlt_bot = BoxLayout(orientation='horizontal', size_hint_y=0.2)

        autofit_txtinput = MyFunctions()

        #bxlt_top
        label_name = Label(text="Name")
        label_item = Label(text='Item')
        label_price = Label(text='Price')
        
        #bxlt_mid_top
        self.btn_txtinput = CurrencyTextInput(text=self.initial_val, size_hint_x = 0.4, readonly=True)
        self.btn_txtinput.foreground_color=[0.5,0.5,0.5,1]
        btn_minus = Button(text='-', size_hint_x=0.2, on_press=self.number_minus)
        
        self.txtinput_count = ClearTextInput(text=self.initial_modifer, size_hint_x=0.2, readonly=True)
        
        Clock.schedule_once(lambda dt: autofit_txtinput.txtinput_autofit_number(self.txtinput_count), 0.05)

        btn_plus = Button(text = '+', size_hint_x=0.2, on_press=self.number_plus)
        
        #bxlt_mid_bot
        btn_custom = Button(text='Custom', on_release=self.btn_custom)

        #bxlt_bot
        btn_ok = Button(text='Okay', on_press=self.dismiss_popup)
        btn_cancel = Button(text='Cancel', on_press=self.dismiss_popup)

        bxlt_top.add_widget(label_name)
        bxlt_top.add_widget(label_item)
        bxlt_top.add_widget(label_price)

        bxlt_mid_top.add_widget(self.btn_txtinput)
        bxlt_mid_top.add_widget(btn_minus)
        bxlt_mid_top.add_widget(self.txtinput_count)
        bxlt_mid_top.add_widget(btn_plus)
        
        bxlt_mid_bot.add_widget(btn_custom)

        bxlt_mid.add_widget(bxlt_mid_top)
        bxlt_mid.add_widget(bxlt_mid_bot)

        bxlt_bot.add_widget(btn_ok)
        bxlt_bot.add_widget(btn_cancel)

        bxlt.add_widget(bxlt_top)
        bxlt.add_widget(bxlt_mid)
        bxlt.add_widget(bxlt_bot)

        self.content = bxlt
    
    def number_plus(self, instance):
        if self.txtinput_count.foreground_color == [0.5,0.5,0.5,1]:
            self.txtinput_count.foreground_color=[1,1,1,1]
            self.btn_txtinput.text = self.initial_val
            self.btn_txtinput.readonly = True
            self.btn_txtinput.foreground_color=[0.5,0.5,0.5,1]

        new_val = str(int(self.txtinput_count.text) + 1)
        self.txtinput_count.text = new_val

    def number_minus(self, instance):
        if self.txtinput_count.foreground_color == [0.5,0.5,0.5,1]:
            self.txtinput_count.foreground_color=[1,1,1,1]
            self.btn_txtinput.text = self.initial_val
            self.btn_txtinput.readonly = True
            self.btn_txtinput.foreground_color=[0.5,0.5,0.5,1]
        
        new_val = str(int(self.txtinput_count.text) - 1)
        self.txtinput_count.text = new_val
    
    def btn_custom(self,instance):
        self.txtinput_count.text = '1'
        self.txtinput_count.foreground_color=[0.5,0.5,0.5,1]
        self.btn_txtinput.text ='0.00'
        self.btn_txtinput.readonly = False
        self.btn_txtinput.focus = True
        self.btn_txtinput.foreground_color=[1,1,1,1]

    def dismiss_popup(self, instance):
        self.on_dismiss_callback(self.original_btn_id, self.btn_txtinput.text, self.txtinput_count.text)
        self.dismiss()
    
    def close_popup(self, instance):
        self.dismiss()
        
class MyFunctions:
    def __init__(self):
        pass
    def txtinput_autofit_font_size(self, txtinput, max_text):
        curr_font_size = txtinput.font_size
        max_width = 0.9 * txtinput.width
        # txtinput.text = max_text
        label = Label(text=max_text, font_size=curr_font_size)
        label.texture_update()
        label.size = label.texture_size
        # print(f'TxtInput | size: {txtinput.size}')
        # print(f'Label Pre| size: {label.size} | text_size: {label.text_size} | texture_size: {label.texture_size}')
        #Keep increasing font_size if label.width < max_width
        while label.width < max_width:
            curr_font_size += 1
            label.font_size = curr_font_size
            label.texture_update()
            label.size = label.texture_size

        #if font_size increase update is greater than max_width
        while label.width > max_width:
            curr_font_size -= 1
            label.font_size = curr_font_size
            label.texture_update()
            label.size = label.texture_size

        # print(f'Label Post| size: {label.size} | text_size: {label.text_size} | texture_size: {label.texture_size}')
        txtinput.font_size = curr_font_size
        
    def txtinput_valign(self, txtinput, max_text):
        label = Label(text=max_text, font_size=txtinput.font_size)
        label.texture_update()
        label.size = label.texture_size
        #Adjust Padding
        padding_top = (txtinput.height - label.height)/2
        txtinput.padding = [txtinput.padding[0], padding_top, txtinput.padding[2], 0]

    def txtinput_autofit_currency(self, txtinput):
        self.txtinput_autofit_font_size(txtinput, '0000.00')
        self.txtinput_valign(txtinput, '0000.00')
        txtinput.multiline = False
        txtinput.halign = 'center'
    
    def txtinput_autofit_number(self, txtinput):
        self.txtinput_autofit_font_size(txtinput, '000')
        self.txtinput_valign(txtinput, '000')
        txtinput.multiline = False
        txtinput.halign = 'center'

    def txtinput_autofit_item(self, txtinput):
        max_text = 'ABCDEFGHIJKLMNO'
        self.txtinput_autofit_font_size(txtinput, max_text)
        self.txtinput_valign(txtinput, max_text)
        txtinput.multiline = False
        txtinput.hint_text = 'Item Description'

    def txtinput_autofit_person(self, txtinput):
        max_text = 'ABCDEFGHIJ'
        txtinput.multiline = False
        txtinput.halign = 'center'
        txtinput.hint_text = 'Person'
        self.txtinput_autofit_font_size(txtinput, max_text)
        self.txtinput_valign(txtinput, max_text)

class AddItemPopup(Popup):
    def __init__(self,on_dismiss_callback, **kwargs):
        super(AddItemPopup, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.9, 0.2)
        self.pos_hint = {"top": 0.7}
        bxlt_top = BoxLayoutType1(orientation='horizontal')
        self.txtinput_item = ClearTextInput(size_hint_x=0.6, multiline=False, on_text_validate=self.txtinput_item_validate)
        label = Label(text='$', font_size=24, size_hint_x=0.1)
        label.color = 1,1,1,1
        self.txtinput_price = CurrencyTextInput(size_hint_x=0.3, on_text_validate=self.dismiss_popup)

        bxlt_top.add_widget(self.txtinput_item)
        bxlt_top.add_widget(label)
        bxlt_top.add_widget(self.txtinput_price)


        bxlt_bot = BoxLayout(orientation='horizontal', spacing=10)
        btn_add = ButtonType2(text='Add Item', size_hint_x=0.8, on_press=self.dismiss_popup)
        btn_cancel = ButtonType2(text='Cancel', size_hint_x=0.2, on_release=self.close_popup)
        bxlt_bot.add_widget(btn_add)
        bxlt_bot.add_widget(btn_cancel)

        content_layout = PopupBoxLayout(orientation='vertical')
        content_layout.add_widget(bxlt_top)
        content_layout.add_widget(bxlt_bot)

        self.txtinput_item.focus = True
        self.content = content_layout

    # def on_open(self):
    #     autofit_txtinput = MyFunctions()
    #     autofit_txtinput.txtinput_autofit_currency(self.txtinput_price)
    #     autofit_txtinput.txtinput_autofit_item(self.txtinput_item)


    def txtinput_item_validate(self,instance):
        self.txtinput_price.focus = True

    def dismiss_popup(self, instance):
        # Call the on_dismiss_callback and pass the entered text
        self.on_dismiss_callback(self.txtinput_item.text, self.txtinput_price.text)
        self.dismiss()
    
    def close_popup(self, instance):
        self.dismiss()

class AddPersonPopup(Popup):
    def __init__(self,on_dismiss_callback, **kwargs):
        super(AddPersonPopup, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.7, 0.2)
        self.pos_hint = {"top": 0.7}
        bxlt_top = BoxLayoutType1(orientation='vertical')
        self.txtinput_person = PersonTextInput(background_color=(0,0,0,0), foreground_color=(1,1,1,1), on_text_validate=self.dismiss_popup)
        
        bxlt_top.add_widget(self.txtinput_person)
        
        bxlt_bot = BoxLayout(orientation='horizontal', spacing=10)
        btn_add = ButtonType2(text='Add Person', size_hint_x=0.7, on_press=self.dismiss_popup)
        btn_cancel = ButtonType2(text='Cancel', size_hint_x=0.3, on_release=self.close_popup)
        bxlt_bot.add_widget(btn_add)
        bxlt_bot.add_widget(btn_cancel)

        content_layout = PopupBoxLayout(orientation='vertical')
        content_layout.add_widget(bxlt_top)
        content_layout.add_widget(bxlt_bot)
        
        self.txtinput_person.focus = True
        self.content = content_layout

    def dismiss_popup(self, instance):
        # Call the on_dismiss_callback and pass the entered text
        self.on_dismiss_callback(self.txtinput_person.text)
        self.dismiss()
    
    def close_popup(self, instance):
        self.dismiss()

class TaxTipPopup(Popup):
    def __init__(self,on_dismiss_callback, prices, **kwargs):
        super(TaxTipPopup, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.prices = prices
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.9, 0.3)
        self.pos_hint = {"top": 0.7}
        bxlt_top = BoxLayoutType1(orientation='horizontal')
        self.label_tax_desc = Label(text='Tax', size_hint_x=0.3)
        label = Label(text='$', font_size=24, size_hint_x=0.1)
        self.txtinput_tax_price = CurrencyTextInput(size_hint_x=0.6)
        self.txtinput_tax_price.text=self.prices[0]
        bxlt_top.add_widget(self.label_tax_desc)
        bxlt_top.add_widget(label)
        bxlt_top.add_widget(self.txtinput_tax_price)

        bxlt_mid = BoxLayoutType1(orientation='horizontal')
        self.label_tip_desc = Label(text='Tip', size_hint_x=0.3)
        label = Label(text='$', font_size=24, size_hint_x=0.1)
        self.txtinput_tip_price = CurrencyTextInput(size_hint_x=0.6)
        self.txtinput_tip_price.text=self.prices[1]
        bxlt_mid.add_widget(self.label_tip_desc)
        bxlt_mid.add_widget(label)
        bxlt_mid.add_widget(self.txtinput_tip_price)

        bxlt_bot = BoxLayout(orientation='horizontal', spacing=10)
        btn_update = ButtonType1(text='Update', size_hint_x=0.8, on_press=self.dismiss_popup)
        btn_cancel = ButtonType1(text='Cancel', size_hint_x=0.2, on_release=self.close_popup)
        bxlt_bot.add_widget(btn_update)
        bxlt_bot.add_widget(btn_cancel)

        content_layout = PopupBoxLayout(orientation='vertical')
        content_layout.add_widget(bxlt_top)
        content_layout.add_widget(bxlt_mid)
        content_layout.add_widget(bxlt_bot)

        self.content = content_layout

    # def on_open(self):
    #     autofit_txtinput = MyFunctions()
    #     autofit_txtinput.txtinput_autofit_currency(self.txtinput_tax_price)
    #     autofit_txtinput.txtinput_autofit_currency(self.txtinput_tip_price)
        
    def dismiss_popup(self, instance):
        tax_desc = self.label_tax_desc
        tax_price = self.txtinput_tax_price
        tip_desc = self.label_tip_desc
        tip_price = self.txtinput_tip_price
        self.on_dismiss_callback(tax_desc, tax_price, tip_desc, tip_price)
        self.dismiss()

    def close_popup(self, instance):
        self.dismiss()

class WarningPopup(Popup):
    def __init__(self, label_text, **kwargs):
        super(WarningPopup, self).__init__(**kwargs)
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.7, 0.2)
        self.pos_hint = {"top": 0.7}
        
        bxlt = BoxLayoutType1(orientation='vertical', padding=10)
        label = Label(text=label_text)
        btn = ButtonType2(text='Okay', on_press=self.dismiss)
        
        bxlt.add_widget(label)
        bxlt.add_widget(btn)

        content_layout = BoxLayout(orientation='vertical')
        content_layout.add_widget(bxlt)

        self.content = content_layout

class ConfirmPopup(Popup):
    def __init__(self, on_dismiss_callback, label_text, **kwargs):
        super(ConfirmPopup, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.7, 0.2)
        self.pos_hint = {"top": 0.7}
        
        bxlt = BoxLayout(orientation='vertical')
        label = Label(text=label_text)

        bxlt_btn = BoxLayout(orientation='horizontal', spacing=10)
        btn = ButtonType2(text='Okay', on_release=self.dismiss_popup)
        btn_cancel = ButtonType2(text='Cancel', on_release=self.close_popup)
        bxlt_btn.add_widget(btn)
        bxlt_btn.add_widget(btn_cancel)
        bxlt.add_widget(label)
        bxlt.add_widget(bxlt_btn)

        content_layout = BoxLayoutType1(orientation='vertical', padding=10)
        content_layout.add_widget(bxlt)

        self.content = content_layout
    def dismiss_popup(self, instance):
        self.on_dismiss_callback()
        self.dismiss()
    def close_popup(self, instance):
        self.dismiss()

class SummaryPopup(Popup):
    def __init__(self, label_text, **kwargs):
        super(SummaryPopup, self).__init__(**kwargs)
        self.background_color = (0,0,0,0)
        self.title = ''
        self.separator_color = 0,0,0,0
        self.size_hint = (0.7, 0.5)
        self.pos_hint = {"top": 0.8}
        self.mytext = label_text
        bxlt = BoxLayoutType1(orientation='vertical', padding=10)
        scroll_view = ScrollView(do_scroll_y=True,do_scroll_x=False, effect_cls='ScrollEffect')
        label = Label(text=label_text, size_hint_y= None)
        label.height = label.texture_size[1]
        label.padding = 10,10
        
        label.bind(texture_size=label.setter('size'))
        scroll_view.add_widget(label)
        bxlt_bot = BoxLayoutType1(orientation='horizontal', spacing=10, size_hint_y=0.2)
        btn = ButtonType2(text='Okay', on_press=self.dismiss, size_hint_x=0.7)
        self.btn_copy = ButtonType2(text='Copy', on_press=self.copy_to_clipboard, size_hint_x=0.3)
        bxlt_bot.add_widget(btn)
        bxlt_bot.add_widget(self.btn_copy)
        bxlt.add_widget(scroll_view)
        bxlt.add_widget(bxlt_bot)

        content_layout = BoxLayout(orientation='vertical')
        content_layout.add_widget(bxlt)

        self.content = content_layout

    def copy_to_clipboard(self, instance):
        self.btn_copy.text = 'Copied!'
        Clipboard.copy(self.mytext)

class PopupBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(PopupBoxLayout, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0.3)
            self.shadow = BoxShadow(pos=[0,0],size=self.size,offset=(0,-10),spread_radius=(-10,-10),border_radius=(10,10,10,10),blur_radius=20)
            Color(61/255,71/255,106/255,1)
            self.roundrect = RoundedRectangle(pos=[0,0], size=self.size, radius=[10])
        self.spacing = 10
        self.padding = 10
        self.bind(pos=self.update_shadow, size=self.update_shadow)

    def update_shadow(self,*args):
        self.shadow.pos = self.pos
        self.roundrect.pos = self.pos
        self.shadow.size = self.size
        self.roundrect.size = self.size

class PersonTextInput(TextInput):
     def __init__(self, **kwargs):
        super(PersonTextInput, self).__init__(**kwargs)
        self.background_color=(0,0,0,0)
        self.foreground_color=(1,1,1,1)

        autofit_txtinput = MyFunctions()
        Clock.schedule_once(lambda dt: autofit_txtinput.txtinput_autofit_person(self), 0.05)

class PersonTextInputAuto(TextInput):
    def __init__(self, on_dismiss_callback, **kwargs):
        super(PersonTextInputAuto, self).__init__(**kwargs)
        self.on_dismiss_callback = on_dismiss_callback
        self.background_color=(0,0,0,0)
        self.foreground_color=(1,1,1,1)
        self.multiline = False
        self.hint_text = 'Person'
        self.bind(on_text_validate=self.txtinput_item_validate, focus=self.on_text_input_focus)
        
        autofit_txtinput = MyFunctions()
        Clock.schedule_once(lambda dt: autofit_txtinput.txtinput_autofit_person(self), 0.05)

    def txtinput_item_validate(self,instance):
        self.unbind(focus=self.on_text_input_focus)
        self.unbind(on_text_validate=self.txtinput_item_validate)
        self.on_dismiss_callback('Enter')

    def on_text_input_focus(self, instance, value):
        if value == False:
            if self.text != '':
                self.unbind(focus=self.on_text_input_focus)
                self.unbind(on_text_validate=self.txtinput_item_validate)
                self.on_dismiss_callback('Unfocus')

class ClearTextInput(TextInput):
    def __init__(self, **kwargs):
        super(ClearTextInput, self).__init__(**kwargs)
        self.background_color=(0,0,0,0)
        self.foreground_color=(1,1,1,1)

        autofit_txtinput = MyFunctions()
        Clock.schedule_once(lambda dt: autofit_txtinput.txtinput_autofit_item(self), 0.05)

class ItemBoxLayoutAuto(BoxLayout):
    def __init__(self, on_dismiss_callback, item_height, **kwargs):
        super(ItemBoxLayoutAuto, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0.3)
            self.shadow = BoxShadow(pos=[0,0],size=self.size,offset=(0,-10),spread_radius=(-10,-10),border_radius=(10,10,10,10),blur_radius=20)
            Color(1, 1, 1, 1)
            self.roundrect = RoundedRectangle(source='imgs/layout_color_1.png', pos=[0,0], size=self.size, radius=[10])

        self.bind(pos=self.update_shadow, size=self.update_shadow)

        self.on_dismiss_callback = on_dismiss_callback
        self.background_color=(0,0,0,0)
        self.foreground_color=(1,1,1,1)
        self.orientation = 'horizontal'
        self.still_input = False
        self.txtinput_item = ClearTextInput(multiline=False, size_hint=(0.6, None), height=item_height)
        self.txtinput_item.bind(on_text_validate=self.go_to_next, focus=self.on_text_input_focus)
        label_mid = Label(text='$', size_hint=(0.1,None), height=item_height)
        label_mid.color = 1,1,1,1
        self.txtinput_price = CurrencyTextInput(multiline=False, size_hint=(0.3, None), height=item_height)
        self.txtinput_price.bind(on_text_validate=self.txtinput_item_validate, focus=self.on_text_input_focus)
        
        self.add_widget(self.txtinput_item)
        self.add_widget(label_mid)
        self.add_widget(self.txtinput_price)

    def update_shadow(self,*args):
        self.shadow.pos = self.pos
        self.roundrect.pos = self.pos
        self.shadow.size = self.size
        self.roundrect.size = self.size

    def go_to_next(self, instance):
        # if self.txtinput_price.text == '':
        self.txtinput_price.focus = True

    def txtinput_item_validate(self,instance):
        self.txtinput_item.unbind(focus=self.on_text_input_focus)
        self.txtinput_item.unbind(on_text_validate=self.txtinput_item_validate)

        self.txtinput_price.unbind(focus=self.on_text_input_focus)
        self.txtinput_price.unbind(on_text_validate=self.txtinput_item_validate)

        self.on_dismiss_callback('Enter')

    def on_text_input_focus(self, instance, value):
        if value == False:
            if self.txtinput_item.text != '' or self.txtinput_price.text != '':
                if self.txtinput_price.focus == False and self.txtinput_item.focus == False:
                    self.txtinput_item.unbind(focus=self.on_text_input_focus)
                    self.txtinput_item.unbind(on_text_validate=self.txtinput_item_validate)

                    self.txtinput_price.unbind(focus=self.on_text_input_focus)
                    self.txtinput_price.unbind(on_text_validate=self.txtinput_item_validate)
                    self.on_dismiss_callback('Unfocus')
        
class CurrencyTextInput(TextInput):
    def __init__(self, **kwargs):
        super(CurrencyTextInput, self).__init__(**kwargs)
        self.multiline = False
        self.halign = 'center'
        self.hint_text = '0.00'
        self.input_type = 'number'
        self.background_color = [0,0,0,0]
        self.foreground_color = [1,1,1,1]

        autofit_txtinput = MyFunctions()
        Clock.schedule_once(lambda dt: autofit_txtinput.txtinput_autofit_currency(self), 0.05)

    def on_text(self, instance, value):
        if not value:
            formatted_text = ''
        else:
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
                    if float(value) == 0.00:
                        formatted_text =''
                    else:
                        formatted_text = '0.0' + value
            else: 
                formatted_text = value

        
        # Updates the text and cursor position
        self.multiline = False
        self.text = formatted_text
        Clock.schedule_once(partial(self.do_cursor_movement, 'cursor_end'))
    
    def insert_text(self, substring, from_undo=False):
        # Allow only digits
        allowed_chars = set('0123456789')
        if substring =='' or all(char in allowed_chars for char in substring):
            return super(CurrencyTextInput, self).insert_text(substring, from_undo)
        else:
            return super(CurrencyTextInput, self).insert_text('', from_undo)

class BoxLayoutType1(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayoutType1, self).__init__(**kwargs)

class BoxLayoutType2(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayoutType2, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0.3)
            self.shadow = BoxShadow(pos=[0,0],size=self.size,offset=(0,-10),spread_radius=(-10,-10),border_radius=(10,10,10,10),blur_radius=20)
            Color(1, 1, 1, 1)
            self.roundrect = RoundedRectangle(source='imgs/layout_color_1.png', pos=[0,0], size=self.size, radius=[10])

        self.bind(pos=self.update_shadow, size=self.update_shadow)

    def update_shadow(self,*args):
        self.shadow.pos = self.pos
        self.roundrect.pos = self.pos
        self.shadow.size = self.size
        self.roundrect.size = self.size
        
class ButtonType1(Button):
    def __init__(self, **kwargs):
        super(ButtonType1, self).__init__(**kwargs)
    
class ButtonType2(Button):
    def __init__(self, **kwargs):
        super(ButtonType2, self).__init__(**kwargs)

class ButtonType3(Button):
    def __init__(self, **kwargs):
        super(ButtonType3, self).__init__(**kwargs)

class ButtonType4(Button):
    def __init__(self, **kwargs):
        super(ButtonType4, self).__init__(**kwargs)

class ButtonType5(Button):
    def __init__(self, **kwargs):
        super(ButtonType5, self).__init__(**kwargs)
    
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
