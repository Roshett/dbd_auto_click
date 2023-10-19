import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui as pg
import time
from detect import detect_red_rectangles, detect_white_rectangles

# get centroid of counturs
def get_centroid(countur):
    M = cv2.moments(countur)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx, cy)

# function which check counturs intersection
def check_intersection(countur1, countur2):
    
    # get centroid of counturs
    centroid1 = get_centroid(countur1)
    centroid2 = get_centroid(countur2)
    
    # get distance between centroids
    dist = np.sqrt((centroid1[0] - centroid2[0])**2 + (centroid1[1] - centroid2[1])**2)
    
    # get counturs area
    area1 = cv2.contourArea(countur1)
    area2 = cv2.contourArea(countur2)
    
    # get counturs radius
    radius1 = np.sqrt(area1 / np.pi)
    radius2 = np.sqrt(area2 / np.pi)
    
    # check if counturs intersect
    if dist < radius1 + radius2:
        return True
    else:
        return False

#red image from file imgs/screenshot.png
# img = cv2.imread('imgs/screenshot.jpg')

# coords = detect_red_color(img)
# red_counturs = detect_red_rectangles(img)
# white_countrs = detect_white_rectangles(img)

# print(len(red_counturs))
# print(red_counturs[0])
# print(len(white_countrs))

# for countur in red_counturs:
#     for countur2 in white_countrs:
#         if check_intersection(countur, countur2):
#             print('red and white intersect')
