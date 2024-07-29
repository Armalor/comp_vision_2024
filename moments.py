# считаем моменты контура:
M = cv2.moments(contour)

# Центр тяжести это первый момент (сумма радиус-векторов), отнесенный к нулевому (площади-массе)
if 0 != M['m00']:
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    cv2.circle(result_copy, (cx, cy), 5, 255, 2)
    cv2.line(result_copy, (start_y, start_x), (cx, cy), (255,), 2)
    tangen = start_x - cx
    normal = start_y - cy

    if normal != 0:
        angle = np.degrees(np.arctan(tangen / normal))
    else:
        angle = None

cv2.line(result_copy, (start_y, start_x), (start_y, y + h // 2), (255,), 2)