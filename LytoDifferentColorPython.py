#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Alyson Chen <qoo810823@gmail.com>
# 2020.04.27
# python LytoDifferentColorPython.py

import cv2
import numpy as np
import pyautogui
import time

def drawDifferentCircle(circlesList,image):
    circlesList = sorted(circlesList,key=lambda x:x[3],reverse=True)
    brightnesslist =[]
    for i in range(len(circlesList)):
        brightnesslist.append(circlesList[i][0])
    count=0
    for i in brightnesslist :
        count=count+1
        if brightnesslist.count(i)==1:
            count=count-1
            # cv2.circle(image, (circlesList[count][1], circlesList[count][2]), circlesList[count][3], (0, 255, 0), 4)
            cv2.putText(image, str(circlesList[count][0]), (circlesList[count][1], circlesList[count][2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(image, (circlesList[count][1] - 5, circlesList[count][2] - 5), (circlesList[count][1] + 5, circlesList[count][2] + 5), (255, 255, 255), -1)
            # pyautogui.moveTo(175+circlesList[count][1], 400+circlesList[count][2])
            # pyautogui.click()
            # time.sleep(0.5)
    return image

def findCircles(image):
    # load the image, clone it for output, and then convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    circlesList=[]
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            r,g,b=image[y,x]
            Data = [(r+g+b),x,y,r]
            circlesList.append(Data)
        image=drawDifferentCircle(circlesList,image)
    else:
        print("No circle~~")
        return None
    return circlesList
#screenshot
while True:
    # make a screenshot
    img = pyautogui.screenshot(region=(175,400, 575, 600))# X1,Y1,X2,Y2
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    # convert colors from BGR to RGB
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = np.uint8(np.clip((1.5 * img + 10), 0, 255))
    hight,width,channel = img.shape
    circlesList = findCircles(img)
    cv2.imshow("screenshot", img)
    # if the user clicks q, it exits
    if cv2.waitKey(1) == ord("q"):
        break
# make sure everything is closed when exited
cv2.destroyAllWindows()