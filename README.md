# Projet_RossiniEnergy_Vehicle-Number-Plate-Recognition


## 0) L'idée du projet - l'architecture

Lorsque la caméra prend la photo d'un automobile. La reconnaissance de plaque de l'automobile implique trois étapes principales : 
 - La détection de plaque : Une fonction de contour sera utilisée pour détecter les objets rectangulaires dans l'image pour trouver la plaque de l'automobile
 - La segmentation des caractères sur plaque:  Une fois que Contour détecte la plaque, je dois la recadrer et l'enregistrer en tant que nouvelle image. 
 - La reconnaissance de caractères : Je prévoir à utiliser une fonction comme une reconnaissance optique de caractères sur l'image recadrée pour détecter le nombre.

## I) Hardwares 
- Raspberry Pi 
- Une Pi Camera ( ou une caméra normal : webcam Logitech)
- Environnement : Linus OS 
- Language programmation: Python
- LCD Display
- Transistors, Diodes

Schéma du circuit branché :![ShémaBranché](https://user-images.githubusercontent.com/46745468/151795175-a00502ff-0e06-4457-9038-ba68d9aa8d1b.png)


## II) Installer le système d'exploitation pour Pi et les bibliothèques utilisés: 

Je prévois à utiliser la bibliothèque **OpenCV** ( Open Computer Vision) pour détecter et reconnaître les plaques d'immatriculation, et la bibliothèque **Tesseract** est utilisée pour lire les caractères. Donc, avant de continuer, j'installe d'abord OpenCV, Tesseract et les autres bibliothèques requises.

Pour installer OpenCV sur Raspberry Pi
```
pip3 install opencv-contrib-python
```

Pour installer Tesseract et ses bibliothèques

```
sudo apt-get install tesseract-ocr
pip install pytesseract
pip install pyttsx3
```
## III) Demo la programmation

Importe les packages , les bibliothèques requis pour ce projet.

```
import numpy as np
import cv2
import imutils
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
```

Initialise le caméra et définis la résolution.

```
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
```

J'utilise la fonction **capture_continuous** pour commencer à capturer les images de la caméra Raspberry Pi. Et j'utilise la touche "S" du clavier pour capturer une image particulière.

```
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
```

### La 1ère étape : La détection de plaque
J'affiche l'image origine 
```
cv2.imshow('image origine',img)
```

![1](https://user-images.githubusercontent.com/46745468/151800939-3d0b7f51-f9e6-4b49-8e31-fc001c3f9507.jpg)


Je coverte l'image au **GRIS SCALE** pour diminuer des bruits
```
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

La fonction **adaptiveThreshold** dans la bibliothèque OPEN CV pour effectuer la détection des bords du plaque sur l'image total

```
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
```

Ensuite ,je vais chercher **des contours sur l'image**. Après cela, trie les contours détectés du plus grand au plus petit.
```
contours,h = cv2.findContours(thresh,1,2)
largest_rectangle = [0,0]
```

Le Raspberry Pi peut trouver plusieurs contours, je dois donc **filtrer le contour de la plaque d'immatriculation** en recherchant un contour en forme de rectangle à quatre côtés et une figure fermée parmi les résultats obtenus.

```
for cnt in contours :
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx)==4:
        area = cv2.contourArea(cnt)
        if area > largest_rectangle[0]:
            largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
```

Trouver et afficher l'image avec la plaque contourée 

```
x,y,w,h = cv2.boundingRect(largest_rectangle[1])

image = img[y:y+h,x:x+w]
cv2.drawContours(img,[largest_rectangle[1]],0,(0,255,0),8)

cropped = img[y:y+h,x:x+w]
cv2.imshow('TROUVER LA PLAQUE',img)
```

Résultat : 

![trouver la plaque](https://user-images.githubusercontent.com/46745468/151801510-21a569cb-f358-4010-b183-9a0e1180b294.png)

### La 2ème étape : Je dois recadrer et enregistrer en tant que nouvelle image en masquant tout de l'image total sauf la plaque d'immatriculation

```
cv2.drawContours(img,[largest_rectangle[1]],0,(255,255,255),18)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# covertir au GRIS SCALE
blur = cv2.GaussianBlur(gray, (3,3), 0) # Flou l'image pour réduire le bruit
thresh = cv2.threshold(blur,0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imshow('PHOTO OBTENU',thresh)
```
Résultat obtenu :

![photo obtenu](https://user-images.githubusercontent.com/46745468/151802240-0d14640d-a9a4-400a-bda4-83c06baeed62.png)

### La 3ème étape : La reconnaissance de caractères et stocker les caractères reconnus dans la variable 'text'

Lire les caractères de l'image de la plaque d'immatriculation à l'aide de la bibliothèque Tesseract et stocker les caractères reconnus dans la variable 'text'

```
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\quang\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
print("LA VALEUR DU PLAQUE TROUVE:")
print(data)
cv2.waitKey()
```

Résultat obtenu : 

![ChiffreReconnaissanceParProgram](https://user-images.githubusercontent.com/46745468/151803275-642a99ff-63fd-4042-9d24-5ff413f03111.png)








