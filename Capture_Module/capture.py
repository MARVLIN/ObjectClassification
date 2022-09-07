import cv2
from time import sleep
import requests


def capture():
    cam = cv2.VideoCapture(0)
    sleep(1.5)

    cv2.namedWindow("capture")

    img_counter = 0

    while True:
        ret, frame = cam.read()

        cv2.imshow("capturing", frame)

        k = cv2.waitKey(1)

        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        cam.release()
        img_counter += 1
        if img_counter == 1:
            cv2.destroyAllWindows()
            url = 'http://art1x.pythonanywhere.com/snippets/1/'
            files = {'image': open('opencv_frame_0.png', 'rb')}
            #headers = {'Authorization': 'Token a50ad9e5ff215abd67028a8bd904a11ac0b1409f'}
            r = requests.put(url, files=files)
            print(r)

            return True