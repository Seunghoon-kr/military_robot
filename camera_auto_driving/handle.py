import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)
tracker = cv2.TrackerCSRT_create()


def handle_box():
    ret, frame = cap.read()
    height, width, channel = frame.shape
    return frame, width, height

def drawBox(img,boxx):
    x,y,width,height = int(boxx[0]), int(boxx[1]), int(boxx[2]), int(boxx[3])
    cv2.rectangle(img, (x,y), ((x+width), (y+height)), (255,0,255),3,1)

'''
def init_frame(x1, y1, x2, y2):
    
    ret,frame = cap.read()

    x,y,width,height = min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2)
    boxx = (x,y,width,height)
    tracker.init(frame,boxx)
    return cap , tracker;
''' 


def handle_flow(x1,y1,x2,y2,imput_frame):
    
    imput_frame = np.array(imput_frame).astype(np.uint8)
    x,y,width,height = min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2)
    boxx = (x,y,width,height)
    tracker.init(imput_frame,boxx)
    
    ret,frame = cap.read()
    img_h, img_w, channel = frame.shape
    raw_img = frame
    success, box = tracker.update(frame)
    a,b,w,h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    mid_x, mid_y = a+w//2, b+h//2
    if success:
        drawBox(frame, box)
        cv2.arrowedLine(frame, (mid_x, mid_y), (img_w//2, img_h//2), (255,0,0), 2)
    return frame,a,b,a+w,b+h, raw_img
    

'''
def handle_flow(box):
    
    ret,frame = cap.read()
    

    tracker.init(frame,box)

    #while True:
    ret,frame = cap.read()
    success, box = tracker.update(frame)
    if success:
        drawBox(frame, box)
    return frame, box



#handle_box()

box = [100, 100, 100, 100]

while cv2.waitKey(33) < 0:
    frame, box = handle_flow(box)
    cv2.imshow("frame", frame)
    print(box)
    
cap.release()
cv2.destroyAllWindows()

'''