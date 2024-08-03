import cv2
import numpy as np
from typing import Tuple, Optional


def single_contour(contours, result_copy) -> Optional[Tuple[float, float]]:

    angle = None
    radius = None

    if contours:
        # Сортируем по убыванию площади контура — хотим один самый большой:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Третий аргумент — это индекс контура, который мы хотим вывести. Мы хотим самый большой.
        # Вывести все можно, передав -1 вместо 0:
        cv2.drawContours(result_copy, contours, 0, (255,), 4)
        contour = contours[0]

        # Получаем прямоугольник, обрамляющий наш контур:
        (x, y, w, h) = cv2.boundingRect(contour)

        # И выводим его:
        cv2.rectangle(result_copy, (x, y), (x + w, y + h), (255,), 1)

        # ВНИМАНИЕ! В «.shape» первый параметр — ВЫСОТА!
        max_y, max_x, = result_copy.shape

        max_x //= 2

        # считаем моменты контура:
        M = cv2.moments(contour)

        # Центр тяжести это первый момент (сумма радиус-векторов), отнесенный к нулевому (площади-массе)
        if 0 != M['m00']:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(result_copy, (cx, cy), 5, 255, 2)
            cv2.line(result_copy, (max_x, max_y), (cx, cy), (255,), 2)
            tangen = max_x - cx
            normal = max_y - cy

            if normal != 0:
                angle = np.degrees(np.arctan(tangen / normal))
            else:
                angle = 0

            radius = np.sqrt((cx - max_x) ** 2 + (cy - max_y) ** 2)

        cv2.line(result_copy, (max_x, max_y), (max_x, y + h // 2), (255,), 2)

    return angle, radius


def multiply_contours(contours, result_copy) -> Tuple[Optional[float], Optional[float]]:
    angle = None
    radius = None

    if contours:
        # Сортируем по убыванию площади контура — хотим один самый большой:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        x_avg = 0
        y_avg = 0
        cnt = 0
        # ВНИМАНИЕ! В «.shape» первый параметр — ВЫСОТА!
        max_y, max_x, = result_copy.shape
        max_x //= 2

        for idx, contour in enumerate(contours[0:10]):
            # Третий аргумент — это индекс контура, который мы хотим вывести. Мы хотим самый большой.
            # Вывести все можно, передав -1 вместо 0:
            cv2.drawContours(result_copy, contours, idx, (255,), 1)

            # Получаем прямоугольник, обрамляющий наш контур:
            (x, y, w, h) = cv2.boundingRect(contour)

            # считаем моменты контура:
            M = cv2.moments(contour)

            # Центр тяжести это первый момент (сумма радиус-векторов), отнесенный к нулевому (площади-массе)
            if 0 != M['m00']:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                # cv2.circle(result_copy, (cx, cy), 5, 255, 2)

                tangen = max_x - cx
                normal = max_y - cy
                radius = np.sqrt((cx - max_x) ** 2 + (cy - max_y) ** 2)

                if True or radius <= max_y*1.3:
                    cv2.line(result_copy, (max_x, max_y), (cx, cy), (255,), 1)
                    # И выводим его:
                    cv2.rectangle(result_copy, (x, y), (x + w, y + h), (255,), 1)
                    x_avg += cx
                    y_avg += cy
                    cnt += 1

            cv2.line(result_copy, (max_x, max_y), (max_x, y + h // 2), (255,), 1)

        if cnt:
            x_avg = int(x_avg / cnt)
            y_avg = int(y_avg / cnt)
        else:
            x_avg = max_x
            y_avg = max_y

        cv2.line(result_copy, (max_x, max_y), (x_avg, y_avg), (255,), 2)
        cv2.circle(result_copy, (x_avg, y_avg), 1, 255, 5)

        tangen = max_x - x_avg
        normal = max_y - y_avg

        if normal != 0:
            angle = np.degrees(np.arctan(tangen / normal))
        else:
            angle = 0

    return angle, radius