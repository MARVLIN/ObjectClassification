import numpy as np
import numpy

from json import JSONEncoder

import cv2

import socket
import json
import sys



thres = 0.45  # Threshold to detect object
nms_threshold = 0.2
cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)
# cap.set(10,150)

classNames = []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('n').split('n')

    # print(classNames)
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    while True:
        success, img = cap.read()
        classIds, confs, bbox = net.detect(img, confThreshold=thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))
        # print(type(confs[0]))
        # print(confs)

        indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
        # print(indices)

        # LOOP for detection from the camera
        try:
            i = indices[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]

            cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classIds[i] - 1].upper(), (box[0] + 10, box[1] + 30),
            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Output', img)
            cv2.waitKey(1)


            # retrieving JSON from ndarray
            class NumpyArrayEncoder(JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, numpy.ndarray):
                        return obj.tolist()
                    return JSONEncoder.default(self, obj)


            numpyArray = numpy.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])

            numpyData = {'array': numpyArray}
            encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
            # print('Printing JSON')
            # print(encodedNumpyData) json array of coordinates


            HOST, PORT = '23.254.176.188:22', 22

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                sock.connect((HOST, PORT))
                sock.sendall(bytes(encodedNumpyData,encoding='utf-8'))

                received = sock.recv(1024)
                received = received.decode('utf-8')
            finally:
                sock.close()

            print("Sent:     {}".format(encodedNumpyData))
            print("Received: {}".format(received))



        # If no objects in ndarray: indices
        except:
            print('No objects detected')




