import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')


while True:
    ret, frame = cap.read()
    frame_copy = frame.copy()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('result', frame_hsv)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()