import cv2
import time
import requests

count = 0

x_begin = 20
y_begin = 200
x_end = 620
y_end = 200

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

cap = cv2.VideoCapture(0)

frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:

        cv2.line(frame1, (x_begin, y_begin+10), (x_end, y_end+10), (0, 0, 255), 3)
        cv2.line(frame1, (x_begin, y_begin), (x_end, y_end), (0, 255, 0), 3)
        cv2.line(frame1, (x_begin, y_begin-10), (x_end, y_end-10), (0, 0, 255), 3)

        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 5000:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.line(frame1, (int(((x + w)-x)/2+x), int(((y + h)-y)/2+y)), (int(((x + w)-x)/2+x), int(((y + h)-y)/2+y)), (0, 0, 255), 18)

        if int(((y + h)-y)/2+y) > y_begin - 10 and int(((y + h)-y)/2+y) < y_begin + 10:
            count += 1
            if count % 2 != 0:
                print("Вошел")
                requests.get('http://localhost:9009/enter')
            else:
                print("Вышел")
                requests.get('http://localhost:9009/exit')
                count = 0
            time.sleep(3)
            print(count)

        # print("Обнаружено движение объекта !!!")
        # print(x)
        # print(x + w)
        # print(y)
        # print(y + h)
        # print(w)
        # print(h)

    cv2.imshow("view", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
