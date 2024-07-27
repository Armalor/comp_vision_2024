# Исп
import cv2
import os

img = cv2.imread('./data/road-signs/footpath.jpg')
# img2 = cv2.imread('./data/road-signs/left-turn.jpg')

if img is None:
    print('ФАЙЛ НЕ НАЙДЕН')
    os._exit(1)






# cv2.imshow('img2', img2)

print(img.shape)
print(img.size)
# uint8:
print(img.dtype)

x_max, y_max, _ = img.shape

x = x_max // 3
y = y_max // 3

img[x, y] = [0, 0, 255]
tpl = (img.item(x, y, 0), img.item(x, y, 1), img.item(x, y, 2))

print(tpl)

roi = img[50:150, 20:200]


cv2.imshow('img', img)
while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()