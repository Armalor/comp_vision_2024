import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')


while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    frame_h = frame_hsv[:, :, 0]
    frame_s = frame_hsv[:, :, 1]
    frame_v = frame_hsv[:, :, 2]

    min_ = (40, 0, 0)
    max_ = (75, 255, 255)

    mask = cv2.inRange(frame_hsv, min_, max_)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('mask', mask)
    cv2.imshow('result', result)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()