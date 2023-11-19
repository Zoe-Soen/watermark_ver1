from tkinter import filedialog as fd
import ttkbootstrap
from ttkbootstrap.constants import *
from watermark import *
from menu import *
from PIL import ImageTk, Image
# --------------------------------------------------
UI_FONT = 'assets/fonts/Arial.ttf'
WELCOME_MESSAGE = "Welcome to use Watermarkly!"
DES_MESSAGE = '''1. Open an image from your PC.
2. Choose 'Add Watermark', type the watermark in to the 'Text Entry', and set the font, color, size, position, opacity and rotation.
3. Or choose 'Add Logo' to upload a logo onto your image file.
4. Click 'Remove' to clear all change you made.
5. Click 'Save' to output your edition and save to your local folder as a new image file.
'''
LOGO_IMAGE = 'assets/logo/1.png'

# --------------------------------------------------
def open_file():
    file_name = fd.askopenfilename(filetypes=[
        ('jpeg', '.jpg .jpeg'),
        ('png', '.png'),
        ('bitmap', '.bmp'),
        ('gif', '.gif')])
    
    if file_name != '':
        top_frm.grid_remove()
        main_frm.grid()
    
        photo_box.update_photo(file_name)
        photo_box.update_watermark()

        photo_box.grid(row=0, column=0, padx=photo_box.new_padx, pady=photo_box.new_pady, sticky=NSEW)
        back_btn.configure(state=NORMAL)

def go_back():
    main_frm.grid_remove()
    top_frm.grid()

def open_add_text_menu():
    add_text_menu = AddTextMenu(app, watermark, photo_box)
    add_text_menu.on_text_change(add_text_menu.text_entry.sv)
    next_btn.configure(state=NORMAL)

# --------------------------------------------------
app = ttkbootstrap.Window()
app.title('Watermark')
screen_width = app.winfo_screenwidth() # 1440
screen_height = app.winfo_screenheight() # 900
app.geometry(f'{screen_width}x{screen_height}+0+5')

# --------------------------------------------------
top_frm = ttkbootstrap.Frame(app)
top_frm.grid(row=0, column=0, padx=480, pady=200, sticky=NSEW) #

logo_img = ImageTk.PhotoImage(Image.open(LOGO_IMAGE))
logo = ttkbootstrap.Label(top_frm, image=logo_img, width=10)
logo.grid(row=0, column=0, sticky=NSEW)

app_name = ttkbootstrap.Label(top_frm, font=(UI_FONT, 24, 'bold'), text='Add Watermark')
app_name.grid(row=1, column=0, pady=(80,20))

select_file_btn = ttkbootstrap.Button(top_frm, text='Select Files', bootstyle=PRIMARY, width=15, command=open_file)
select_file_btn.grid(row=2, column=0)

# --------------------------------------------------
main_frm = ttkbootstrap.Frame(app)
main_frm.grid(row=0, column=0, padx=0, pady=0, sticky=NSEW)
main_frm.grid_remove()

menu_frm = ttkbootstrap.Frame(main_frm)
menu_frm.grid(row=0, column=0, padx=50, pady=(50,0), sticky=NSEW)

back_btn = ttkbootstrap.Button(menu_frm, text='< Back', width=12, bootstyle=LIGHT, command=go_back, state=DISABLED)
back_btn.grid(row=0, column=0, sticky=W)
next_btn = ttkbootstrap.Button(menu_frm, text='Next Step >', width=12, bootstyle=PRIMARY, state=DISABLED)
next_btn.grid(row=0, column=2, sticky=E)

menu_frm2 = ttkbootstrap.Frame(menu_frm)
menu_frm2.grid(row=0, column=1, padx=325, sticky=NSEW) 

add_text_btn = ttkbootstrap.Button(menu_frm2, text='Add Text', width=12, command=open_add_text_menu, bootstyle=SUCCESS)
add_text_btn.grid(row=0, column=0, padx=(0,5), sticky=NSEW)
add_Logo_btn = ttkbootstrap.Button(menu_frm2, text='Add Logo', width=12, bootstyle=INFO)
add_Logo_btn.grid(row=0, column=1, padx=5, sticky=NSEW)
remove_btn = ttkbootstrap.Button(menu_frm2, text='Remove', width=12, bootstyle=SECONDARY, state=DISABLED)
remove_btn.grid(row=0, column=2, padx=(5,0), sticky=NSEW)

center_frm = ttkbootstrap.Frame(main_frm, border=True, borderwidth=3, relief='solid')
center_frm.grid(row=1, column=0, columnspan=4, rowspan=10, padx=50, pady=10, sticky=NSEW)

watermark = Watermark(app)
photo_box = ImageViewBox(center_frm, watermark)
photo_box.grid(row=0, column=0, sticky=NSEW)

# --------------------------------------------------
app.mainloop()
