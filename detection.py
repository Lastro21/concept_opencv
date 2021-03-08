import cv2  # импорт модуля cv2
import time

cap = cv2.VideoCapture(0)  # видео поток с камеры

ret, frame1 = cap.read()
ret, frame2 = cap.read()

last_motion_time = int(time.time())

while True:  # метод isOpened() выводит статус видеопотока

    diff = cv2.absdiff(frame1,
                       frame2)  # нахождение разницы двух кадров, которая проявляется лишь при изменении одного из них, т.е. с этого момента наша программа реагирует на любое движение.

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию

    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # метод для выделения кромки объекта белым цветом

    dilated = cv2.dilate(thresh, None, iterations=3)

    сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #

    for contour in сontours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 1000:  # условие при котором площадь выделенного объекта меньше 700 px
            continue
        print('Motion Detected!')

    frame1 = frame2  #
    ret, frame2 = cap.read()  #

cap.release()