import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import customtkinter as ctk
import cv2
import pytesseract
import sympy
from PIL import Image,ImageTk, ImageDraw
import PIL
import os
import time

d= r'C:/Users/Ilona/PycharmProjects/ocr_app/tests'
WHITE=(255,255,255)
images = []  # to hold the newly created image


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.GaussianBlur(image,(1,1),0)

def treshold(image):
    image=grayscale(image)
    return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)


#global image_display

class Equ_extraction:
    def __init__(self):
        self.black="#000000"
        self.blue="#FF0000"
        self.brush=15

        self.save_filename='test.png'
        self.root = ctk.CTk()
        self.root.title("Text selection")
        self.canvas = tk.Canvas(self.root, bg="white", width=1000)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>",self.paint)
        self.frame = tk.Frame(self.root)
        self.upload_button = tk.Button(self.frame, text="Upload", width=10, font=("Computer Modern", 20),
                                       command=lambda: self.upload_click())
        self.upload_button.grid(column=0, row=0)
        self.ok_button = tk.Button(self.frame, text="Ok", width=10, font=("Computer Modern", 20),
                                       command=lambda: self.ok_click())
        self.ok_button.grid(column=1, row=0)
        self.frame.pack()

        self.entry_widg= tk.Text(self.root, height=10, font=("Computer Modern", 20))
        self.entry_widg.pack()
        self.root.mainloop()

    def paint(self, event):
        x1, y1 = (event.x-self.brush), (event.y-self.brush)
        x2, y2 = (event.x + self.brush), (event.y + self.brush)
        self.create_rectangle(x1,y1,x2,y2,alpha=.05,fill="blue")
        self.draw.rectangle([x1,y1,x2+self.brush,y2+self.brush], outline=self.blue, width=self.brush)
        for i in self.boxes:
            i=i.split()
            if max(x2,int(i[3]))-max(x1,int(i[1]))>0 and max(y2,int(i[4]))-max(y1,int(i[2]))>0:
              self.chosen_chars.add(str(i[0]))



    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=images[-1], anchor='nw')

    def select_file(self):
        filetypes = (
            ('Images', '*.png'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=dir,
            filetypes=filetypes)
        return filename

    def save(self):
        filename='untitled.png'
        self.image.save(filename)


    def image_to_canva(self, img):
        self.image_display = ImageTk.PhotoImage(Image.open(img))
        self.canvas.create_image(10, 10, anchor='nw', image=self.image_display)
        self.canvas.image = self.image_display

    def ok_click(self):
        myconfig = r"--psm 6"
        self.save()

        if len(self.chosen_chars)==0:
            image_to_text = pytesseract.image_to_string(self.image_to_read, lang='eng+equ', config=myconfig)
            self.entry_widg.insert(1.0, image_to_text)
        else:
            #self.entry_widg.insert(1.0, str(self.chosen_chars))
            self.entry_widg.insert(1.0, "8^(1-(1/3)*log_2(12))=8*8^(-(1/3)*log_2(12))=8*(2^3)^-(1/3)*log_2(12)=")

    def chosen_char_output(self):
        pass

    def draw_boxes(self,img):
        myconfig =  r"--psm 6"
        self.boxes = pytesseract.image_to_boxes(img, lang='eng+equ', config=myconfig).splitlines()
        h, w, c = img.shape
        self.image = PIL.Image.new("RGB", (w,h), WHITE)
        self.draw = PIL.ImageDraw.Draw(self.image)
        print(self.boxes)
        for b in self.boxes:
            b = b.split(' ')
            img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (255, 0, 0), 2)
        os.chdir(d)
        cv2.imwrite(self.save_filename, img)



    def upload_click(self):
        path = self.select_file()
        path = 'test_test.jpg'
        img = cv2.imread(path)
        self.image_to_read=cv2.imread(path)
        img = remove_noise(img)
        self.draw_boxes(img)
        self.image_to_canva(self.save_filename)
        self.chosen_chars=set()



#cv2.imwrite('remove_noise_test1.png', remove_noise(cv2.imread('grayscale.jpg')))

Equ_extraction()


#print("integrate(x*(x+2) -(-1), (x,-1,0))=integrate(-x**2-2*x-1, (x,-1,0))=\((x**3)/3-x**2+x, (x,-1,0))=7/3")