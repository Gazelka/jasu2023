import numpy
import cv2

def deskew(image):
    coords = numpy.column_stack(numpy.where(image > 0))
    angle = cv2.minAreaRect(coords)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

img = cv2.imread('img1.png')
cv2.imshow(deskew(img))