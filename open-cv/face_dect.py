import cv2

img = cv2.imread("img.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cascade.load("../data/haarcascade_frontalface_default.xml")
res = cascade.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3, minSize=(30,30))
for face in res:
    x, y, w, h = face
    print(x, y, w, h)