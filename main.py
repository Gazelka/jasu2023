import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import customtkinter as ctk
import cv2
import pytesseract
import sympy
from PIL import Image,ImageTk
import os
#import text_selection
import numpy

#global
open_brackets=['(','{','[']
close_brackets=[')','}',']']
dir = r'C:/Users/Ilona/PycharmProjects/ocr_app'

root = ctk.CTk()
root.title("Proof checker")
canvas = tk.Canvas(root, bg='white')
canvas.grid(column=1, row=2, padx=10, pady=10, sticky='nswe')
window1=0


def get_type_of_brackets(c):
    if c in open_brackets:
        return open_brackets.index(c)
    elif c in close_brackets:
        return close_brackets.index(c)

def syntax_validator(s):
    a=[]
    for i in s:
        if i in open_brackets:
            a.append(i)
        elif i in close_brackets:
            if len(a)==0:
                return False
            if get_type_of_brackets(i)==get_type_of_brackets(a[len(a)-1]):
                a.pop()
            else:
                return False
    if len(a)==0:
        return True
    return False
    pass

def select_file():
    filetypes = (
        ('Images', '*.png'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=dir,
        filetypes=filetypes)
    return filename

# partial binarisation
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = numpy.ones((5, 5), numpy.uint8)
    return cv2.dilate(image, kernel, iterations=1)



def upload_click():
    path = select_file()
    img = cv2.imread(path)

    myconfig = r"--psm 11 --oem 3"
    image_to_text = pytesseract.image_to_string(img, config=myconfig, lang='eng+equ')

    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    #cv2.imshow('img', img)
    os.chdir(dir)
    cv2.imwrite('1.png',img)
    #image_to_canva('1.png')
    #entry_widg.delete(1,END)
    entry_widg.insert(1.0,image_to_text)
    #window1=text_selection.Text_selection('1.png')


def validator(list_of_equations):
    for i in range(len(list_of_equations)-1):
        print(list_of_equations[i])
        if not sympy.simplify(list_of_equations[i]-list_of_equations[i+1])==0:
            print("Error")
        else:
            print("Valid")


def ok_click():
    s=entry_widg.get(1.0, tk.END)
    s = s.rstrip(s[-1])
    list_of_equations = s.split('=')
    list_of_expr=[]
    entry_widg.delete(1.0, tk.END)
    for i in list_of_equations:
        try:
            list_of_expr.append(sympy.sympify(i))
        except SyntaxError:
            messagebox.showinfo('Error','Invalid syntax!')
            return
        except:
            messagebox.showinfo('Error','Invalid data!')
            return
    validator(list_of_expr)
    pass


def clear_click():
    entry_widg.delete(1.0, tk.END)


if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    path = (r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    pytesseract.pytesseract.tesseract_cmd = path

    # font
    comp15 = tk.font.Font(family="Computer Modern", size=15)
    #root.configure(font = ("Computer Modern",25))
    #root.geometry("1000x500")
    entry_widg = tk.Text(root, height=10, font=("Computer Modern", 20))
    entry_widg.grid(columnspan=2,column=0,row=0,padx=10, pady=10)

    # menu
    buttons_frame = tk.LabelFrame(root)
    button_ok = tk.Button(buttons_frame, text="OK", width=10, font=comp15, command= lambda :ok_click())
    #button_upload = tk.Button(buttons_frame, text="Upload", width=10, font=comp15, command=lambda: upload_click())
    button_clear = tk.Button(buttons_frame, text="Clear", width=10, font=comp15, command=lambda : clear_click())
    button_backspace = tk.Button(buttons_frame, text="Backspace", width=10, font=comp15)

    button_ok.grid(row=0, column=1, padx=10, pady=5)
    #button_upload.grid(row=0, column=0, padx=10, pady=5)
    button_clear.grid(row=0, column=2, padx=10, pady=5)
    button_backspace.grid(row=0, column=3, padx=10, pady=5)

    clicked = tk.StringVar()
    clicked.set("Basic")
    options = [
        "Basic",
        "Symbols",
        "Calculus",
        "Trigonometry"
    ]
    drop = tk.OptionMenu(buttons_frame, clicked, *options)
    drop.configure(width=20, font=comp15, height=1)

    drop.grid(row=0, column=4, padx=10, pady=10)
    buttons_frame.grid(columnspan=2,column=0,row=1)

    # calculator
    basic_calc_frame = tk.LabelFrame(root)

    button0 = tk.Button(basic_calc_frame, text="0", padx=40, pady=20, font=comp15)
    button1 = tk.Button(basic_calc_frame, text="1", padx=40, pady=20, font=comp15)
    button2 = tk.Button(basic_calc_frame, text="2", padx=40, pady=20, font=comp15)
    button3 = tk.Button(basic_calc_frame, text="3", padx=40, pady=20, font=comp15)
    button4 = tk.Button(basic_calc_frame, text="4", padx=40, pady=20, font=comp15)
    button5 = tk.Button(basic_calc_frame, text="5", padx=40, pady=20, font=comp15)
    button6 = tk.Button(basic_calc_frame, text="6", padx=40, pady=20, font=comp15)
    button7 = tk.Button(basic_calc_frame, text="7", padx=40, pady=20, font=comp15)
    button8 = tk.Button(basic_calc_frame, text="8", padx=40, pady=20, font=comp15)
    button9 = tk.Button(basic_calc_frame, text="9", padx=40, pady=20, font=comp15)

    button_dot = tk.Button(basic_calc_frame, text=".", padx=40, pady=20, font=comp15)
    button_plus = tk.Button(basic_calc_frame, text="+", padx=40, pady=20, font=comp15)
    button_minus = tk.Button(basic_calc_frame, text="-", padx=40, pady=20, font=comp15)
    button_multiply = tk.Button(basic_calc_frame, text="×", padx=40, pady=20, font=comp15)
    button_divide = tk.Button(basic_calc_frame, text="÷", padx=40, pady=20, font=comp15)
    button_percent = tk.Button(basic_calc_frame, text="%", padx=37, pady=20, font=comp15)
    buttonx = tk.Button(basic_calc_frame, text="x", padx=40, pady=20, font=comp15)
    button_equal = tk.Button(basic_calc_frame, text="=", padx=40, pady=20, font=comp15)
    button_square = tk.Button(basic_calc_frame, text="^2", padx=36, pady=20, font=comp15)
    button_brackets = tk.Button(basic_calc_frame, text="(...)", padx=30, pady=20, font=comp15)

    button0.grid(row=3, column=1, padx=10, pady=5)
    button1.grid(row=2, column=0, padx=10, pady=5)
    button2.grid(row=2, column=1, padx=10, pady=5)
    button3.grid(row=2, column=2, padx=10, pady=5)
    button4.grid(row=1, column=0, padx=10, pady=5)
    button5.grid(row=1, column=1, padx=10, pady=5)
    button6.grid(row=1, column=2, padx=10, pady=5)
    button7.grid(row=0, column=0, padx=10, pady=5)
    button8.grid(row=0, column=1, padx=10, pady=5)
    button9.grid(row=0, column=2, padx=10, pady=5)

    button_dot.grid(row=3, column=0, padx=10, pady=5)
    button_equal.grid(row=3, column=2, padx=10, pady=5)

    button_plus.grid(row=0, column=3, padx=10, pady=5)
    button_minus.grid(row=1, column=3, padx=10, pady=5)
    button_multiply.grid(row=2, column=3, padx=10, pady=5)
    button_divide.grid(row=3, column=3, padx=10, pady=5)

    buttonx.grid(row=0, column=4, padx=10, pady=5)
    button_percent.grid(row=1, column=4, padx=10, pady=5)
    button_square.grid(row=2, column=4, padx=10, pady=5)
    button_brackets.grid(row=3, column=4, padx=10, pady=5)

    basic_calc_frame.grid(column=0,row=2)

    root.mainloop()