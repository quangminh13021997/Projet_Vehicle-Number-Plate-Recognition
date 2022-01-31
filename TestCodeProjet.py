import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

# 1ERE ETAPE
#------------------- La détection de plaque - La segmentation des caractères sur plaque --------------------
img = cv2.imread('4.jpg')# Lire l'image
cv2.imshow('image origine',img) # Afficher l'image origine 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# covertir au GRIS SCALE

#adaptiveThreshold pour effectuer la détection des bords du plaque sur l'image total
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

# Chercher des contours sur l'image et trie les contours détectés du plus grand au plus petit
contours,h = cv2.findContours(thresh,1,2)
largest_rectangle = [0,0]

# filtrer le contour de la plaque d'immatriculation en recherchant un contour en forme de rectangle à quatre côtés
for cnt in contours :
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx)==4:
        area = cv2.contourArea(cnt)
        if area > largest_rectangle[0]:
            largest_rectangle = [cv2.contourArea(cnt), cnt, approx]

# trouver et afficher l'image avec la plaque contourée            
x,y,w,h = cv2.boundingRect(largest_rectangle[1])

image = img[y:y+h,x:x+w]
cv2.drawContours(img,[largest_rectangle[1]],0,(0,255,0),8)

cropped = img[y:y+h,x:x+w]
cv2.imshow('TROUVER LA PLAQUE',img)


# 2EME ETAPE
#recadrer et enregistrer en tant que nouvelle image en masquant tout de l'image total sauf la plaque d'immatriculation
cv2.drawContours(img,[largest_rectangle[1]],0,(255,255,255),18)

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\quang\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# covertir au GRIS SCALE
blur = cv2.GaussianBlur(gray, (3,3), 0) # Flou l'image pour réduire le bruit
thresh = cv2.threshold(blur,0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imshow('PHOTO OBTENU',thresh)

# 3EME ETAPE 
#--------------------- La reconnaissance de caractères et stocker les caractères reconnus dans la variable 'text'-------------------
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
print("LA VALEUR DU PLAQUE TROUVE:")
print(data)
cv2.waitKey()
