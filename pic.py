# Исп
import cv2
import os

img = cv2.imread('./data/road-signs/footpath.jpg')

if img is None:
    print('ФАЙЛ НЕ НАЙДЕН')
    os._exit(1)


cv2.imshow('img', img)


while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()