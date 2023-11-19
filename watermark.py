from tkinter import Image, filedialog as fd, messagebox, END
import ttkbootstrap
from ttkbootstrap.constants import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import pandas as pd


df = pd.read_csv("assets/colors/rgb_colors.csv")
COLOR_LIST = df['hex'].values.tolist()
ALL_COLOR = df.to_dict('records')

IMAGEBOX_WIDTH = 1320
IMAGEBOX_HEIGHT = 700


class ImageViewBox(ttkbootstrap.Canvas):
    def __init__(self, frame, watermark):
        super().__init__(frame)
        self.watermark = watermark
        self.max_width = IMAGEBOX_WIDTH
        self.max_height = IMAGEBOX_HEIGHT
        self.im_box_ratio = self.max_width / self.max_height
    
    def update_watermark(self, txt_x=None, txt_y=None): 
        img_copy = self.im.copy()
        self.im_width, self.im_height = img_copy.size
        self.new_padx = int(abs(self.max_width - self.im_width)/2)
        self.new_pady = int(abs(self.max_height - self.im_height)/2)

        txt = Image.new('RGBA', img_copy.size)
        d = ImageDraw.Draw(txt, 'RGBA')
        font = ImageFont.truetype(self.watermark.font['path'], size=self.watermark.font_size) 

        if self.watermark.text != '':
            _, _, self.text_w, self.text_h = d.textbbox((0, 0), text=self.watermark.text, font=font)
            
            txt = txt.resize((self.text_w, self.text_h))
            d = ImageDraw.Draw(txt, 'RGBA')
            d.text((0, 0), text=self.watermark.text, fill=(self.watermark.color), font=font)
        
            rotated_txt = txt.rotate(self.watermark.rotation, expand=True)
            offset_x = int((rotated_txt.width - txt.width) / 2)
            offset_y = int((rotated_txt.height - txt.height) / 2)

            if txt_x != None and txt_y != None:
                img_copy.paste(rotated_txt, (txt_x - offset_x, txt_y - offset_y), rotated_txt)  
            else:
                self.watermark.x = int((self.im_width - self.text_w) / 2)
                self.watermark.y = int((self.im_height - self.text_h) / 2)
                img_copy.paste(rotated_txt, (self.watermark.x - offset_x, self.watermark.y - offset_y), rotated_txt)
            
            self.photo = ImageTk.PhotoImage(img_copy)
            self.composite_image = img_copy
            self.create_image(0,0, anchor=NW, image=self.photo)
        else:
            self.photo = ImageTk.PhotoImage(img_copy)
            self.composite_image = img_copy
            self.create_image(0,0, anchor=NW, image=self.photo)

        return img_copy

    def update_photo(self, fp):
        try:
            self.im = Image.open(fp).convert('RGBA')
            self.origin_im_width, self.origin_im_height = self.im.size
            
            self.im.thumbnail((self.max_width, self.max_height))
            self.resized_im_width, self.resized_im_height = self.im.size

            self.photo = ImageTk.PhotoImage(self.im)
            self.configure(width=self.im.width, height=self.im.height)
            self.create_image(0,0, anchor=NW, image=self.photo)

        except PIL.UnidentifiedImageError:
            messagebox.showerror(f'Invalid Image: {fp}')

    def remove(self):
        self.watermark.font = {'font_name': 'Arial', 'path': 'assets/fonts/Arial.ttf'}
        self.watermark.font_size = 50
        self.watermark.opacity = 255
        self.watermark.color = self.watermark.color_list[0]['hex'] # black
        self.watermark.rotation = 0
        self.watermark.x = None
        self.watermark.y = None
        self.watermark.selected_pos = self.watermark.positions[3]
        self.watermark.text = ''

    def save1(self):
        image = self.im.copy()
        ratio = self.im.height / self.resized_height 

        txt = Image.new('RGBA', image.size)
        d = ImageDraw.Draw(txt, 'RGBA')
        resized_font = int(self.watermark.font_size * ratio)
        font = ImageFont.truetype(self.watermark.font['path'], size=resized_font) 
        if self.watermark.text != '':
            _, _, w, h = d.textbbox((self.watermark.x, self.watermark.y), text=self.watermark.text, font=font)
            txt = txt.resize((w,h))
        d = ImageDraw.Draw(txt, 'RGBA')
        d.text(xy=(0,0), text=self.watermark.text, fill=(self.watermark.color), font=font)

        starting_width = txt.width
        starting_height = txt.height
        rotated_txt = txt.rotate(self.watermark.rotation, expand=True)

        offset_x = int((rotated_txt.width - starting_width) / 2)
        offset_y = int((rotated_txt.height - starting_height) / 2)
        x_loc = int(self.watermark.x * ratio - offset_x)
        y_loc = int(self.watermark.y * ratio - offset_y)
        image.paste(rotated_txt, (x_loc, y_loc), rotated_txt)

        file_path = fd.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension='png',
            filetypes=[
                ('jpeg', '.jpg .jpeg'),
                ('png', '.png'),
                ('bitmap', '.bmp'),
                ('gif', '.gif'),
            ])
        if file_path is not None:
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension in ['.jpg', '.jpeg']:
                image = image.convert('RGB')
            image.save(file_path)
    def save(self):
        out_put = self.update_watermark(self.watermark.x, self.watermark.y)
        ratio = self.origin_im_height / self.resized_im_height 
        origin_size_img = out_put.resize((int(out_put.width * ratio), int(out_put.height * ratio)))

        file_path = fd.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension='png',
            filetypes=[
                ('jpeg', '.jpg .jpeg'),
                ('png', '.png'),
                ('bitmap', '.bmp'),
                ('gif', '.gif'),
            ])
        if file_path is not None:
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension in ['.jpg', '.jpeg']:
                origin_size_img = origin_size_img.convert('RGB')
            origin_size_img.save(file_path)

class Watermark():
    def __init__(self, app):
        self.app = app
        self.color_list = ALL_COLOR

        self.font = {'font_name': 'Arial', 'path': 'assets/fonts/Arial.ttf'}
        self.font_size = 50
        self.opacity = 255
        self.color = (0, 0, 0, self.opacity) # black
        self.rotation = 0
        self.positions = ['Top Center', 'Top Left', 'Top Right', 'Middle Center', 'Bottom Center', 'Bottom Left', 'Bottom Right']
        self.selected_pos = self.positions[3]
        self.x = None
        self.y = None
        self.text = ''
        
    def get_position(self, im_w, im_h, text_w, text_h):
        for pos in self.positions:
            if self.selected_pos == pos and pos == "Middle Center":
                self.x = int((im_w - text_w) / 2)
                self.y = int((im_h - text_h) / 2)
            elif self.selected_pos == pos and pos == "Top Left":
                self.x = 0
                self.y = 0
            elif self.selected_pos == pos and pos == "Top Center":
                self.x = int((im_w - text_w) / 2)
                self.y = 0
            elif self.selected_pos == pos and pos == "Top Right":
                self.x = int(im_w - text_w)
                self.y = 0
            elif self.selected_pos == pos and pos == "Bottom Left":
                self.x = 0
                self.y = im_h - text_h
            elif self.selected_pos == pos and pos == "Bottom Center":
                self.x = int((im_w - text_w) / 2)
                self.y = im_h - text_h
            elif self.selected_pos == pos and pos == "Bottom Right":
                self.x = im_w - text_w
                self.y = im_h - text_h
        return [self.x, self.y]

    def move(self, direction):
        print(f'Before: {self.x}, {self.y}')
        if direction == "up":
            self.y -= 10
        elif direction == "down":
            self.y += 10
        elif direction == "left":
            self.x -= 10
        elif direction == "right":
            self.x += 10
        return [self.x, self.y]
        
    def change_font(self, font):
        self.font = font
    
    def change_color(self, color): 
        """
        def rgb2hex(r,g,b):
            return "#{:02x}{:02x}{:02x}".format(r,g,b)

        def hex2rgb(hexcode):
            return tuple(map(ord,hexcode[1:].decode('hex')))
        """
        if color == None:
            list_color = list(self.color)[:3]  
        else:
            for item in self.color_list:
                if color == item['hex']:
                    rgb = item['rgb'].strip('()')
                    list_color = [int(i) for i in rgb.split(',')]
        list_color.append(self.opacity)
        self.color = tuple(list_color)
        print(self.color)

    def change_size(self, event, size):
        self.font_size = int(size)
        
    def change_opacity(self, event, var_scale):
        list_color = list(self.color)[:3]
        self.opacity = var_scale
        list_color.append(self.opacity)
        self.color = tuple(list_color)

    # def rotate1(self, direction): # Button version
    #     if direction == "left":
    #         if self.rotation == 355:
    #             self.rotation = 0
    #         else:
    #             self.rotation += 5
    #     else:
    #         if self.rotation == 0:
    #             self.rotation = 355
    #         else:
    #             self.rotation -= 5
            
    #     print(self.rotation)
    def rotate(self, event, var_scale): # Scale version
        self.rotation = var_scale


if __name__ == "__main__":
    # print(ALL_COLOR)
    pass
    