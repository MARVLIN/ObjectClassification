import cv2
import requests

from time import sleep

def capture():
    camera = cv2.VideoCapture(0)
    i = 0
    sleep(2)
    while i < 1:

        return_value, image = camera.read()

        cv2.imwrite('opencv.png', image)
        i += 1
        url = 'http://art1x.pythonanywhere.com/create/'
        files = {'image': open('opencv.png', 'rb')}
        r = requests.post(url, files=files)

        print(r.status_code)

    del(camera)
    return True

















