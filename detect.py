import cv2
import numpy as np
import pyautogui as pg

screen_size = pg.size()
AREA_SIZE_RED = 10
AREA_SIZE_WHITE = 10

# write function which detect red rectangles
def detect_red_rectangles(img):
    # define range of red color in HSV
    lower_red = np.array([0, 210, 130], np.uint8)
    upper_red = np.array([0, 255, 255], np.uint8)
    # lower_red = np.array([136, 87, 111], np.uint8)
    # upper_red = np.array([180, 255, 255], np.uint8)


    # convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    # apply morphology close
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # get contours and filter on area
    result = img.copy()
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    result = img.copy()
    counturs_what_we_need = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > AREA_SIZE_RED:
            cv2.drawContours(result, [c], -1, (0, 255, 0), 1)
            counturs_what_we_need.append(c)
    return counturs_what_we_need, result

def detect_white_rectangles(img):
    # hsv
    lower_white = np.array([0, 0, 165], np.uint8)
    upper_white = np.array([173, 32,255], np.uint8)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    # apply morphology close
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # show_result(thresh)
    # get contours and filter on area
    result = img.copy()
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    result = img.copy()
    counturs_what_we_need = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > AREA_SIZE_WHITE:
            cv2.drawContours(result, [c], -1, (0, 255, 0), 1)
            counturs_what_we_need.append(c)
    return counturs_what_we_need, result

# write function which transform HEX to HSV
def hex_to_hsv(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

# funciton which resize image to 300x300
def resize_image(img):
    # resize image
    # img = cv2.resize(img, (int(screen_size.width / 2), int(screen_size.height / 2)))
    return img

def show_result(img):
    # show result
    cv2.imshow('result', resize_image(img))
    # wait to close
    cv2.waitKey(0)

# get centroid of counturs
def get_centroid(countur):
    M = cv2.moments(countur)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx, cy)

# print(get_centroid(red_counturs[0]))
# print(get_centroid(white_countrs[0]))
# print(get_centroid(white_countrs[1]))

# write function which check counturs intersection
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