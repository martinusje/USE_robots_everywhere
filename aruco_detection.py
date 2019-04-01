import cv2
from cv2 import aruco
import numpy as np
import serial, time
import struct

arduino = serial.Serial('COM9', 9600, timeout=.1)
time.sleep(4) #give the connection a second to settle

pos_x = 90
pos_y = 0

def __draw_label(img, scale, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

cap = cv2.VideoCapture(1)

framewidth = 1280
frameheight = 720

cap.set(3,framewidth) #Setting webcam's image width 
cap.set(4,frameheight) #Setting webcam' image height

while(True):
    ret, frame = cap.read()

    # Our operations on the frame come here
    if frame is not None:
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        for c in corners:
            x = (c[0][0][0] + c[0][1][0] + c[0][2][0] + c[0][3][0]) / 4
            x_error = x - framewidth/2
            y = (c[0][0][1] + c[0][1][1] + c[0][2][1] + c[0][3][1]) / 4
            y_error = y - frameheight/2

            pos_x -= (x_error/3000*180)
            pos_x = max(0, min(pos_x, 180))
            pos_y -= (y_error/5000*180)
            pos_y = max(0, min(pos_y, 180))

            print(pos_x, pos_y)

            arduino.write(str(round(pos_x)))
            time.sleep(0.5)
            arduino.write(str(round(pos_y + 180)))

    cv2.imshow('frame',frame_markers)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break