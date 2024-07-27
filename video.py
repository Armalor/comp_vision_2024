import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')

ranges = {
    'min_h1': {'current': 70, 'max': 180},
    'max_h1': {'current': 82, 'max': 180},
}


def trackbar_handler(name):
    def handler(x):
        global ranges
        ranges[name]['current'] = x

    return handler


for name in ranges:
    cv2.createTrackbar(name,
                       'result',
                       ranges[name]['current'],
                       ranges[name]['max'],
                       trackbar_handler(name)
                       )



while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    min_ = (ranges['min_h1']['current'], 0, 0)
    max_ = (ranges['max_h1']['current'], 255, 255)

    mask = cv2.inRange(frame_hsv, min_, max_)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Ищем контуры
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Сами структуры контуров хранятся в начальном элементе возвращаемого значения:
    contours = contours[0]

    # Их, кстати, может и не быть:
    if contours:

        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Третий аргумент — это индекс контура, который мы хотим вывести. Мы хотим самый большой.
        # Вывести все можно, передав -1 вместо 0:
        cv2.drawContours(result, contours, 0, (255, 0, 0), 1)

        # Получаем прямоугольник, обрамляющий наш контур:
        (x, y, w, h) = cv2.boundingRect(contours[0])

        # И выводим его:
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 1)

        # Аналогично строим минимальную описанную вокруг наибольшего контура окружность:
        (x1, y1), radius = cv2.minEnclosingCircle(contours[0])
        center = (int(x1), int(y1))
        radius = int(radius)
        cv2.circle(result, center, radius, (0, 255, 0), 1)


    cv2.imshow('mask', mask)
    cv2.imshow('result', result)




    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()