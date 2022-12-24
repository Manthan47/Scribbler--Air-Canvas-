import time
import cv2
import os
from HandTracker import HandDetector
from dottedline import drawrect, drawline
import numpy as np
from tkinter import messagebox
import pyautogui

def ppt_main():

    width, height = 1366, 768
    #frames_folder = r"D:\SEM VII\CP III\Final project\Images"
    frames_folder = r"Images"
    slide_num = 0
    hs, ws = int(120 * 1.2), int(213 * 1.2)

    ge_thresh_y = 400
    ge_thresh_x = 750
    # ge_thresh_y = 200
    # ge_thresh_x = 375
    gest_done = False
    gest_counter = 0
    delay = 15
    annotations = [[]]
    annot_num = 0
    annot_start = False

    path_imgs = sorted(os.listdir(frames_folder), key=len)
    print(path_imgs)

    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while True:

        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        pathFullImage = os.path.join(frames_folder, path_imgs[slide_num])
        slide_current = cv2.imread(pathFullImage)
        slide_current = cv2.resize(slide_current, (1366, 768)) 

        hands, frame =  detector.findHands(frame)  

        # Gesture threshold line
        drawrect(frame, (width, 0), (ge_thresh_x, ge_thresh_y), (0, 255, 0), 5,'dotted')

        if hands and gest_done is False:  

            hand = hands[0]
            cx, cy = hand["center"]
            lm_list = hand["lmList"] 
            fingers = detector.fingersUp(hand)  

            x_val = int(np.interp(lm_list[8][0], [width//32, w], [0, width]))
            y_val = int(np.interp(lm_list[8][1], [150, height - 150], [0, height]))
            index_fing = x_val, y_val

            if cy < ge_thresh_y and cx > ge_thresh_x :  
                annot_start = False

                # gest_1 (previous)
                if fingers == [1, 0, 0, 0, 0]:
                    # print("Left")
                    annot_start = False
                    if slide_num > 0:
                        gest_done = True
                        slide_num -= 1
                        annotations = [[]]
                        annot_num = 0

                # gest_2 (next)
                if fingers == [0, 0, 0, 0, 1]:
                    # print("Right")
                    annot_start = False
                    if slide_num < len(path_imgs) - 1:
                        gest_done = True
                        slide_num += 1
                        annotations = [[]]
                        annot_num = 0
                
                # gest_3 (clear screen)
                if fingers == [1, 1, 1, 1, 1]:
                    if annotations:
                        annot_start = False
                        if annot_num >= 0:
                            annotations.clear()
                            annot_num = 0
                            gest_done = True 
                            annotations = [[]]
                # gest_7 (screenshot)
                if fingers == [0, 1, 0, 0, 1]:
                    print("SS")
                    random = int(time.time())
                    filename = "ss/" + str(random) + ".jpg"
                    screenshot = pyautogui.screenshot()
                    screenshot.save(filename)
                    messagebox.showinfo("Screenshot", "Screenshot Taken!!!")
                    
                        
            # gest_4 (show pointer)
            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(slide_current, index_fing, 4, (0, 0, 255), cv2.FILLED)
                annot_start = False

            # gest_5 (draw)
            if fingers == [0, 1, 0, 0, 0]:
                if annot_start is False:
                    annot_start = True
                    annot_num += 1
                    annotations.append([])
                # print(annot_num)
                annotations[annot_num].append(index_fing)
                cv2.circle(slide_current, index_fing, 4, (0, 0, 255), cv2.FILLED)

            else:
                annot_start = False

            # gest_6 (erase)
            if fingers == [0, 1, 1, 1, 0]:
                if annotations:
                    annot_start = False
                    if annot_num >= 0:
                        annotations.pop(-1)
                        annot_num -= 1
                        gest_done = True 

        else:
            annot_start = False

        if gest_done:
            gest_counter += 1
            if gest_counter > delay:
                gest_counter = 0
                gest_done = False

        for i, annotation in enumerate(annotations):
            for j in range(len(annotation)):
                if j != 0:
                    cv2.line(slide_current, annotation[j - 1], annotation[j], (0, 0, 255), 6)

        # small cam in corner
        img_small = cv2.resize(frame, (ws, hs))
        h, w, _ = slide_current.shape
        slide_current[h-hs:h, w-ws:w] = img_small

        cv2.imshow("Slides", slide_current)
        # cv2.imshow("Image", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break