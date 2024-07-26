# Исп
import cv2
import os

img = cv2.imread('./data/road-signs/footpath.jpg')
img2 = cv2.imread('./data/road-signs/left-turn.jpg')

if img is None:
    print('ФАЙЛ НЕ НАЙДЕН')
    os._exit(1)


cv2.imshow('img', img)
cv2.imshow('img2', img2)


while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()