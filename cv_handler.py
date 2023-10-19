import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui as pg
import time
from detect import detect_red_rectangles, detect_white_rectangles, check_intersection
import win32api





class CVHandler:
    def __init__(self, qt_parent):
        DELAY = 4
        screen = pg.size()
        sct = mss()
        bounding_box = {'top': int(screen.height * 0.3), 'left': int(screen.width / 3), 'width': int(screen.width / 3), 'height': int(screen.height * 0.6)}
        start_time = time.time()
        fps = 0
        delay_frames = DELAY
        contr_white = []

        while True:
            sct_img = sct.grab(bounding_box)
            contr_red, result = detect_red_rectangles(np.array(sct_img))

            if(delay_frames == DELAY):
                contr_white, result = detect_white_rectangles(result)
                delay_frames = 0
            else:
                delay_frames += 1

            if(time.time() - start_time > 1):
                # print('FPS: {}'.format(fps))
                qt_parent.progress.emit(fps)
                fps = 0
                start_time = time.time()

            fps += 1

            state_left_button = win32api.GetKeyState(0x01)
            if state_left_button < 0:
                for countur in contr_red:
                    for countur2 in  contr_white:
                        if check_intersection(countur, countur2):
                            print('red and white intersect')
                            pg.press('space')
                    
                        

    # def detect_person(): 