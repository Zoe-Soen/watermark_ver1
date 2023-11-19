from tkinter import Button, Image, END
import tkinter as tk
import ttkbootstrap
from ttkbootstrap.constants import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import pandas as pd
import re

COLORS_FP = "assets/colors/rgb_colors.csv"
df = pd.read_csv(COLORS_FP)
COLOR_LIST = df['hex'].values.tolist()
ALL_COLOR = df.to_dict('records')

FONT_FAMILIES = [
    {'font_name': 'Arial', 'path': 'assets/fonts/Arial.ttf'},
    {'font_name': 'Degreco', 'path': 'assets/fonts/degreco-condensed-regular.otf'},
    {'font_name': 'Eagle Lake', 'path': 'assets/fonts/EagleLake-Regular.ttf'},
    {'font_name': 'IBM Plex Mono', 'path': 'assets/fonts/IBMPlexMono-Regular.ttf'},
    {'font_name': 'Jacques Francois', 'path': 'assets/fonts/JacquesFrancois-Regular.ttf'},
    {'font_name': 'Quando', 'path': 'assets/fonts/Quando-Regular.ttf'},
    {'font_name': 'Racing Sans One', 'path': 'assets/fonts/RacingSansOne-Regular.ttf'},
    {'font_name': 'Sacramento', 'path': 'assets/fonts/Sacramento-Regular.ttf'},
    {'font_name': 'Sail', 'path': 'assets/fonts/Sail-Regular.ttf'},
    {'font_name': 'Trade Winds', 'path': 'assets/fonts/TradeWinds-Regular.ttf'},
    {'font_name': 'Verdana', 'path': 'assets/fonts/verdana.ttf'},
    {'font_name': 'ZCOOL KuaiLe', 'path': 'assets/fonts/ZCOOLKuaiLe-Regular.ttf'},
    ]
OPEN_COLSE_BTN_IMG = [
        'assets/icons/up-arrow.png',
        'assets/icons/right-arrow.png'
    ]
POSITIONS = ['Top Center', 'Top Left', 'Top Right', 'Middle Center', 'Middle Left', 'Middle right', 'Bottom Center', 'Bottom Left', 'Bottom Right']


class AddTextMenu(ttkbootstrap.Frame):
    def __init__(self, win, watermark, photo_box):
        self.watermark = watermark 
        self.photo_box = photo_box
        
        super().__init__(win)
        self.sub_win = ttkbootstrap.Toplevel() 
        self.sub_win.title('Properties')
        self.sub_win.geometry(f'420x700+1000+140')

        self.text_entry = TextEntry(self.sub_win, self.on_text_change)
        self.text_entry.grid(row=2, column=0, padx=15, pady=(15,5), sticky=NSEW)

        self.font_widget = FontWidget(self.sub_win, self.on_font_change)
        self.font_widget.grid(row=3, column=0, padx=15, pady=5, sticky=NSEW)

        self.color_widget = ColorWidget4(self.sub_win, self.on_color_change)
        self.color_widget.grid(row=4, column=0, padx=15, pady=5, sticky=NSEW)

        self.size_widget = SizeWidget(self.sub_win, self.on_size_change)
        self.size_widget.grid(row=5, column=0, padx=15, pady=5, sticky=NSEW)

        self.opacity_widget = OpacityWidget(self.sub_win, self.on_opacity_change)
        self.opacity_widget.grid(row=6, column=0, padx=15, pady=5, sticky=NSEW)

        self.position_widget = PositionWidget(self.sub_win, self.watermark, self.on_position_set, self.on_position_change)
        self.position_widget.grid(row=7, column=0, padx=15, pady=5, sticky=NSEW)

        self.rotation_widget = RotationWidget2(self.sub_win, self.on_rotation_change)
        self.rotation_widget.grid(row=8, column=0, padx=15, pady=5, sticky=NSEW)

        self.copy_save_widget = ClearSaveWidget(self.sub_win, self.clear, self.save)
        self.copy_save_widget.grid(row=9, column=0, padx=15, pady=(35,15))

    def on_text_change(self, sv):
        self.watermark.text = sv.get()
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def on_font_change(self, font):
        self.font_widget.show_font_effect.configure(image=font['photo'])
        self.font_widget.show_font_name.configure(text=font['font_name'])
        self.watermark.change_font(font)
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)
        self.font_widget.toggle_open_close()

    def on_color_change(self, color):
        self.color_widget.show_color_hex.configure(text=color, background=color)
        self.watermark.change_color(color)
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)
        self.color_widget.toggle_open_close()

    def on_size_change(self, event):
        self.watermark.change_size(event, self.size_widget.selected_size.get())
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def on_opacity_change(self, event):
        self.watermark.change_opacity(event, self.opacity_widget.slider.get())
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def on_position_set(self):
        selected_pos = self.position_widget.var_radio.get()
        self.watermark.selected_pos = selected_pos
        watermark_xy = self.watermark.get_position(self.photo_box.im_width, self.photo_box.im_height, self.photo_box.text_w, self.photo_box.text_h)
        self.watermark.x = watermark_xy[0]
        self.watermark.y = watermark_xy[1]
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def on_position_change(self, direction):
        print(self.watermark.x, self.watermark.y)
        new_xy = self.watermark.move(direction)
        self.watermark.x = new_xy[0]
        self.watermark.y = new_xy[1]
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def on_rotation_change(self, event, var_scale): # Scale version
        self.watermark.rotate(event, var_scale)
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def clear(self):
        self.photo_box.remove()
        self.text_entry.sv.set(self.watermark.text)
        self.text_entry.ent.focus()
        self.opacity_widget.slider.set(self.watermark.opacity)
        self.on_font_change([font for font in FONT_FAMILIES if font['font_name']==self.watermark.font['font_name']][0])
        self.font_widget.toggle_open_close()
        self.on_color_change(self.watermark.color)
        self.color_widget.toggle_open_close()
        self.size_widget.selected_size.set(self.watermark.font_size)
        self.rotation_widget.slider.set(self.watermark.rotation)
        self.photo_box.update_watermark(self.watermark.x, self.watermark.y)

    def save(self):
        self.photo_box.save()

# ==============================================================
class TextEntry(ttkbootstrap.Frame):
    def __init__(self, win, on_text_change):
        super().__init__(win)
        ttkbootstrap.Label(self, text='Text:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.sv = ttkbootstrap.StringVar()
        self.sv.set('Your Text')
        self.sv.trace('w', lambda name, index, mode, sv=self.sv: on_text_change(sv))
        self.ent = ttkbootstrap.Entry(self, textvariable=self.sv, width=32)
        self.ent.focus()
        self.ent.grid(row=0, column=1)

class FontWidget(ttkbootstrap.Frame):
    def __init__(self, win, on_font_change, **kwargs):
        super().__init__(win, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        self.base_frm = ttkbootstrap.Frame(self) 
        self.base_frm.grid(row=0, column=0, sticky=NSEW)
        
        self.up_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[0])
        self.right_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[1])

        ttkbootstrap.Label(self.base_frm, text='Font: ', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        frm = ttkbootstrap.Frame(self.base_frm, width=26)
        frm.grid(row=0, column=1, sticky=EW)
        self.show_font_effect = ttkbootstrap.Label(frm, text='') 
        self.show_font_effect.grid(row=0, column=0)
        self.show_font_name = ttkbootstrap.Label(frm, text='', width=23, anchor=CENTER) 
        self.show_font_name.grid(row=0, column=1, padx=(1,2))
        self.btn = Button(frm, text='', image=self.right_arrow_img, width=20, command=self.toggle_open_close) 
        self.btn.grid(row=0, column=2, sticky=E)

        self.canvas = ttkbootstrap.Canvas(self.base_frm, highlightthickness=0)        
        self.scrollbar = ttkbootstrap.Scrollbar(self.base_frm, orient=tk.VERTICAL, command=self.canvas.yview)        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.font_families = FONT_FAMILIES
        
        self.style = ttkbootstrap.Style()
        self.font_group = ttkbootstrap.Frame(self, padding=(20,5,0,0))
        self.font_group.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.font_group, anchor=NW)

        for num, font in enumerate(self.font_families):
            width, height = (60, 60)
            text_1 = 'Ag'
            d_font_1 = ImageFont.truetype(font['path'], size=26)
            d_fill = (77, 77, 77)

            font_txt = Image.new('RGB', (width, height), (256, 256, 256))
            d = ImageDraw.Draw(font_txt)
            _, _, w, h = d.textbbox((0, 0), text=text_1, font=d_font_1) 
            d.text(xy=((width-w)/2, (height-h)/2), text=text_1, font=d_font_1, fill=d_fill) 
            
            font_photo = ImageTk.PhotoImage(font_txt)
            font['photo'] = font_photo 
            font_btn = Button(self.font_group, image=font_photo, command=lambda font=font: on_font_change(font)) 
            font_btn.grid(row=int(num/5)+1, column=num%5, padx=1, pady=1, sticky=W) 

        self.show_font_effect.configure(image=self.font_families[0]['photo'])
        self.show_font_name.configure(text=self.font_families[0]['font_name'])
        
    def toggle_open_close(self):
        if self.font_group.winfo_viewable():
            self.canvas.grid_remove()
            self.scrollbar.grid_remove()
            self.btn.configure(image=self.right_arrow_img)
        else:
            self.canvas.grid(row=1, column=0, columnspan=4, padx=0, sticky=EW) 
            self.scrollbar.grid(row=1, column=3, padx=0, sticky=NS+W) 
            self.btn.configure(image=self.up_arrow_img)
    

# class ColorWidget1(ttkbootstrap.Frame): # Combobox version
#     def __init__(self, win, on_color_change):
#         super().__init__(win)
#         self.color_list = ["black", "white", "blue", "yellow", "green", "red", "purple", "orange", "brown"]
#         self.selected_color = ttkbootstrap.StringVar()
#         self.selected_color.set(self.color_list[0])
#         ttkbootstrap.Label(self, text='Color:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
#         self.cob = ttkbootstrap.Combobox(self, textvariable=self.selected_color, values=self.color_list, state='readonly', width=20)
#         self.cob.current(0)
#         self.cob.bind('<<ComboboxSelected>>', on_color_change)
#         self.cob.grid(row=0, column=1)

#     def get_value(self):
#         return self.cob.get()
# class ColorWidget2(ttkbootstrap.Frame): # Listbox version：https://www.plus2net.com/python/tkinter-colors.php
#     def __init__(self, win, on_color_change):
#         super().__init__(win)
        
#         self.selected_color = ttkbootstrap.StringVar()
#         ttkbootstrap.Label(self, text='Color:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        
#         self.entry = ttkbootstrap.Entry(self, textvariable=self.selected_color, width=21)
#         self.entry.grid(row=0, column=1)
#         self.list_box = tk.Listbox(self, relief='flat', bg='SystemButtonFace',highlightcolor= 'SystemButtonFace', width=22, height=3)
        
#         self.list_box.bind('<<ListboxSelect>>', on_color_change)  
#         self.selection = 0
#         self.entry.bind('<Down>', self.move_down)
#         self.list_box.bind('<Up>', self.move_up)
#         self.list_box.bind('<Return>', self.on_return)
#         self.selected_color.trace('w', self.get_data)        

#     def get_data(self, *args):
#         search_str = self.entry.get()
#         if search_str != '':
#             self.list_box.grid(row=2, column=1)
#             self.list_box.delete(0, END)
#             for color in COLOR_LIST:
#                 if(re.match(search_str, color, re.IGNORECASE)):
#                     self.list_box.insert(END, color)
#             if self.list_box.size() > 0:
#                 self.should_able_arrow_keys = True
#             print(f'should_able_arrow_keys: {self.should_able_arrow_keys}')
  
#     def move_down(self, event):
#         self.list_box.focus()
#         if self.selection < (self.list_box.size() - 1):
#             self.list_box.select_clear(self.selection)
#             self.selection += 1
#             self.list_box.select_set(self.selection)

#     def move_up(self, event):
#         if self.selection > 0:
#             self.list_box.select_clear(self.selection)
#             self.selection -= 1
#             self.list_box.select_set(self.selection)

#     def on_return(self, event):
#         self.list_box.select_set(self.selection)
# class ColorWidget3(ttkbootstrap.Frame): # Button version with showing all contents
#     """折叠收缩格式的菜单"""
#     def __init__(self, win, on_color_change, **kwargs):
#         super().__init__(win, **kwargs)
#         self.columnconfigure(0, weight=1)
#         self.cumulative_rows = 0

#         # widget images
#         self.images = OPEN_COLSE_BTN_IMG

#         self.style = ttkbootstrap.Style()
#         self.color_group = ttkbootstrap.Frame(self, padding=(0,5,0,0))
#         for num, color in enumerate(COLOR_LIST):
#             self.style.configure(f'{color}.TButton', background=color, width=1)
#             color_btn = ttkbootstrap.Button(self.color_group, style=f'{color}.TButton', bootstyle='light-link', command=lambda color=color: on_color_change(color))
#             color_btn.grid(row=int(num/11)+1, column=num%11, padx=1,pady=1)
        
#         self.add(child=self.color_group)

#     def add(self, child, title="Color: ", initial_collapsed=True, **kwargs):
#         if child.winfo_class() != 'TFrame':
#             return
#         frm = ttkbootstrap.Frame(self)
#         frm.grid(row=self.cumulative_rows, column=0, sticky=NSEW)

#         ttkbootstrap.Label(frm, text=title, font=('', 12, 'bold'), width=8).grid(row=0, column=0)
#         show_color_hex = ttkbootstrap.Label(frm, text='hex: ', foreground='gray', width=26)
#         show_color_hex.grid(row=0, column=1, padx=(0,5))

#         def _func(c=child): return self._toggle_open_close(c)
#         btn = ttkbootstrap.Button(frm, text='Hide', width=4, command=_func) 
#         btn.grid(row=0, column=2)
        
#         child.lb = show_color_hex
#         child.btn = btn
#         child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)
        
#         if initial_collapsed:
#             child.grid_remove()
#             child.btn.configure(text='Show')
#         self.cumulative_rows += 2

#     def _toggle_open_close(self, child):
#         if child.winfo_viewable():
#             child.grid_remove()
#             child.btn.configure(text='Show')
#         else:
#             child.grid()
#             child.btn.configure(text='Hide')
class ColorWidget4(ttkbootstrap.Frame): # Canvas vs Scrollbar + Button version. This one is perfect
    def __init__(self, win, on_color_change, **kwargs): # on_color_change,
        super().__init__(win, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        self.color_families = COLOR_LIST

        self.up_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[0])
        self.right_arrow_img = ttkbootstrap.PhotoImage(file=OPEN_COLSE_BTN_IMG[1])

        self.base_frm = ttkbootstrap.Frame(self) # color widget base fram
        self.base_frm.grid(row=0, column=0, sticky=NSEW)

        ttkbootstrap.Label(self.base_frm, text='Color: ', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        frm = ttkbootstrap.Frame(self.base_frm)
        frm.grid(row=0, column=1, sticky=NSEW)

        self.show_color_hex = ttkbootstrap.Label(frm, text='hex: ', foreground='gray', background=self.color_families[0], width=30)
        self.show_color_hex.grid(row=0, column=1, padx=(0,5), sticky=EW)
        self.btn = Button(frm, text='', width=20, image=self.right_arrow_img, command=self.toggle_open_close) #, text='Show',image=self.images[1]
        self.btn.grid(row=0, column=2, sticky=NSEW)

        self.canvas = ttkbootstrap.Canvas(self.base_frm)
        self.scrollbar = ttkbootstrap.Scrollbar(self.base_frm, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.style = ttkbootstrap.Style()
        self.color_group = ttkbootstrap.Frame(self.canvas, padding=(20,5,0,0))
        self.color_group.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.color_group, anchor=NW)
        
        for num, color in enumerate(self.color_families):
            self.style.configure(f'{color}.TButton', background=color, width=1)
            color_btn = ttkbootstrap.Button(self.color_group, style=f'{color}.TButton', bootstyle='light-link', command=lambda color=color: on_color_change(color))
            color_btn.grid(row=int(num/10)+1, column=num%10, padx=1, pady=1)

    def toggle_open_close(self):
        if self.color_group.winfo_viewable():
            self.canvas.grid_remove()
            self.scrollbar.grid_remove()
            self.btn.configure(image=self.right_arrow_img)
        else:
            self.canvas.grid(row=1, column=0, columnspan=3, sticky=EW)
            self.scrollbar.grid(row=1, column=3, sticky=NS)
            self.btn.configure(image=self.up_arrow_img)

class SizeWidget(ttkbootstrap.Frame):
    def __init__(self, win, on_size_change):
        super().__init__(win)
        ttkbootstrap.Label(self, text='Size:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.selected_size = ttkbootstrap.IntVar()
        self.selected_size.set(50)
        self.scale = ttkbootstrap.Scale(self, variable=self.selected_size, from_=10, to_=200, length=260, command=lambda s:self.selected_size.set("%d" % float(s)))
        self.scale.grid(row=0, column=2)
        lb = ttkbootstrap.Label(self, textvariable=self.selected_size, width=4)
        lb.grid(row=0, column=1)
        self.scale.bind('<Motion>', on_size_change)

class OpacityWidget(ttkbootstrap.Frame):
    def __init__(self, win, on_opacity_change):
        super().__init__(win)
        ttkbootstrap.Label(self, text='Opacity:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.slider = ttkbootstrap.IntVar()
        self.slider.set(255)
        self.scale = ttkbootstrap.Scale(self, variable=self.slider, from_=0, to_=255, length=260, command=lambda s:self.slider.set("%d" % float(s)))
        self.scale.grid(row=0, column=2)
        lb = ttkbootstrap.Label(self, textvariable=self.slider, width=4)
        lb.grid(row=0, column=1)
        self.scale.bind('<Motion>', on_opacity_change)

class PositionWidget(ttkbootstrap.Frame):
    def __init__(self, win, watermark, on_position_set, on_position_change):
        super().__init__(win)
        self.watermark = watermark

        ttkbootstrap.Label(self, text='Position:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        frm = ttkbootstrap.Frame(self)
        frm.grid(row=0, column=1, sticky=NSEW)

        sub_frm1 = ttkbootstrap.Frame(frm)
        sub_frm1.grid(row=0, column=0, pady=5)

        self.var_radio = ttkbootstrap.StringVar(value=self.watermark.selected_pos)
        for num, pos in enumerate(self.watermark.positions):
            self.radio_btn = ttkbootstrap.Radiobutton(sub_frm1, text=pos, value=pos, bootstyle='danger', variable=self.var_radio, command=on_position_set)
            self.radio_btn.grid(row=num+1, column=0, pady=2, sticky=W)

        sub_frm2 = ttkbootstrap.Frame(frm)
        sub_frm2.grid(row=0, column=1, padx=80, sticky=E)
        direction_btns = [
            {'text': '▲', 'direction': 'up', 'row': 0, 'col':1},
            {'text': '◀', 'direction': 'left', 'row': 1, 'col':0},
            {'text': '▶', 'direction': 'right', 'row': 1, 'col':2},
            {'text': '▼', 'direction': 'down', 'row': 2, 'col':1},
        ]
        for btn in direction_btns:
            self.btn = ttkbootstrap.Button(sub_frm2, text=btn['text'], width=1, bootstyle='second-outline', command=lambda dir=btn['direction']: on_position_change(dir))
            self.btn.grid(row=btn['row'], column=btn['col'], padx=2, pady=2)

# class RotationWidget1(ttkbootstrap.Frame): # changing by click button
#     """
#         AddTextMenu：
#             self.rotation_widget = RotationWidget(self.sub_win, self.on_rotation_change)
            
#             Call Function：
#             def on_rotation_change(self, direction):
#                 self.watermark.rotate(direction)
#                 self.photo_box.update_watermark()

#         Watermark：
#             def rotate(self, direction):
#                 if direction == "left":
#                     if self.rotation == 355:
#                         self.rotation = 0
#                     else:
#                         self.rotation += 5
#                 else:
#                     if self.rotation == 0:
#                         self.rotation = 355
#                     else:
#                         self.rotation -= 5
                    
#                 print(self.rotation)
#     """
#     def __init__(self, win, on_rotation_change):
#         super().__init__(win)
#         ttkbootstrap.Label(self, text='Rotation', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
#         frm = ttkbootstrap.Frame(self)
#         frm.grid(row=0, column=1, padx=100, sticky=NSEW)
#         buttons = [
#             {'text': '↺', 'direction': 'left', 'row':0, 'col':1, 'padx': (0,17)},
#             {'text': '↻', 'direction': 'right', 'row':0, 'col':3, 'padx': (16,0)},
#         ]
#         for btn in buttons:
#             self.btn = ttkbootstrap.Button(frm, text=btn['text'], width=1, command=lambda dir=btn['direction']: on_rotation_change(dir))
#             self.btn.grid(row=btn['row'], column=btn['col'], padx=btn['padx'], sticky=NSEW)
class RotationWidget2(ttkbootstrap.Frame): # Changging by a scale
    def __init__(self, win, on_rotation_change):
        super().__init__(win)
        ttkbootstrap.Label(self, text='Rotation:', font=('', 12, 'bold'), width=8).grid(row=0, column=0)
        self.slider = ttkbootstrap.IntVar()
        self.slider.set(0)

        self.scale = ttkbootstrap.Scale(self, variable=self.slider, from_=-355, to_=355, length=210, command=lambda s:self.slider.set('%d' % float(s)))
        self.scale.grid(row=0, column=2)

        self.lb = ttkbootstrap.Label(self, textvariable=self.slider, width=4)
        self.lb.grid(row=0, column=1)
        self.scale.bind('<Motion>', lambda event: on_rotation_change(event, self.slider.get()))

        self.btn = ttkbootstrap.Button(self, text='Reset', bootstyle='second-outline', command=lambda s=0:self.slider.set(0))
        self.btn.grid(row=0, column=3)
        self.btn.bind('<Button-1>', lambda event: on_rotation_change(event, 0))


class ClearSaveWidget(ttkbootstrap.Frame):
    def __init__(self, win, clear, save):
        super().__init__(win)
        self.clear_btn = ttkbootstrap.Button(self, text='Clear', bootstyle=SECONDARY, width=8, command=clear)
        self.clear_btn.grid(row=0, column=0, padx=(0,50), sticky=NSEW)

        self.save = ttkbootstrap.Button(self, text='Save', bootstyle=SUCCESS, width=8 , command=save)
        self.save.grid(row=0, column=2, padx=(50,0), sticky=NSEW)



if __name__ == "__main__":
    print(COLOR_LIST)