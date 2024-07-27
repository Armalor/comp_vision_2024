import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('result')


while True:
    ret, frame = cap.read()
    frameCopy = frame.copy()

    cv2.imshow('result', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()