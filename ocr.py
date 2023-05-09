import pytesseract
import re
from PIL import Image
import cv2

path = (r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = path

img = cv2.imread('img1.png')
# pass image into pytesseract module

# pytesseract is trained in many languages
myconfig = r"--psm 11 --oem 3"
image_to_text = pytesseract.image_to_string(img, config=myconfig, lang='eng+equ')


#image_to_text1 = pytesseract.image_to_string(img)

# Print the text
print(image_to_text)