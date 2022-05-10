import cv2
import numpy as np

cap = cv2.VideoCapture(0)
tracker = cv2.TrackerCSRT_create()
    

def Lane_detect(mid_y=0, now_angle=0, tar_angle=0):
    ret,frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2_imshow(gray)
        frame = cv2.GaussianBlur(frame, (15, 15), 0)
        height, width, channel = frame.shape

        b, g, r = cv2.split(frame)
        ret, r_th = cv2.threshold(r, 60,1,cv2.THRESH_BINARY)
        ret, g_th = cv2.threshold(g, 70,1,cv2.THRESH_BINARY)
        ret, b_th = cv2.threshold(b, 100,1,cv2.THRESH_BINARY)

        #RGB to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #채널 분리
        h, s, v = cv2.split(hsv)
        #분리 후 각 채널의 threshold
        ret, h_th = cv2.threshold(h, 100,1,cv2.THRESH_BINARY)
        ret, s_th = cv2.threshold(s, 40,1,cv2.THRESH_BINARY)
        ret, v_th = cv2.threshold(v, 80,1,cv2.THRESH_BINARY)
        #hbsg
        rgbhsv = [v_th,h_th,b_th,s_th,g_th,r_th]  #choise : r_th,g_th,b_th,h_th,s_th,v_th
        threshold_img = np.ones((height,width), dtype='uint8')
        for item in rgbhsv:
            threshold_img *= item
        threshold_img *= 255

        canny = cv2.Canny(threshold_img, 30, 130)
        #cv2_imshow(canny)

        mask = np.zeros((height,width), dtype='uint8')
        poly_heigh = int(height)
        poly_left = int(0.5 * width)
        poly_right = int(width)
        #polygons = np.array([[(poly_left,height), (poly_left, 0), (poly_right, 0), (width, height)]])
        polygons = np.array([[(width//3,height*2//3),(width//3,0),(width,0), (width,height*2//3)]])
        cv2.fillPoly(mask, polygons, 255)

        # Bitwise operation between poly and mask
        masked = cv2.bitwise_and(canny, mask)
        #cv2_imshow(masked)
        lines = cv2.HoughLinesP(masked, 2, np.pi / 180, 80, np.array([]), 30, 50)
        #lines = cv2.HoughLinesP(r_th, 0.8, np.pi / 180, 70, minLineLength = 10, maxLineGap = 500)
        if lines is not None:
            
            for line in lines:
                for x1, y1, x2, y2 in line:
                    if (abs(y2 - y1) / abs(x2 - x1)) < 1:
                        if width//3 < x1 < width*2//3 and width//3 < x2 < width*2//3:
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                            mid_y = np.max([mid_y,abs(y2-y1)])
                            now_angle = np.max([now_angle, (abs(y2 - y1) / abs(x2 - x1))])
                        elif width*2//3 < x1 < width and width*2//3 < x2 < width:
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            tar_angle = np.max([tar_angle, (abs(y2 - y1) / abs(x2 - x1))])
        frame = cv2.putText(frame, "Distance : {}, Current Angle : {}, Target Angle : {}".format(180-mid_y,np.arctan(now_angle)*180//np.pi,np.arctan(tar_angle)*180//np.pi), (40, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA).astype(np.uint8)
        return frame, threshold_img, mid_y, now_angle, tar_angle
    
def handle_box():
    ret, frame = cap.read()
    height, width, channel = frame.shape
    return frame, width, height

def drawBox(img,boxx, box_color=(255,0,255)):
    x,y,width,height = int(boxx[0]), int(boxx[1]), int(boxx[2]), int(boxx[3])
    cv2.rectangle(img, (x,y), ((x+width), (y+height)), box_color,3,1)


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
    box_mid_x, box_mid_y = a+w//2, b+h//2
    to_mid_x,to_mid_y=0,0
    if success:
        drawBox(frame, box)
        cv2.arrowedLine(frame, (box_mid_x, box_mid_y), (img_w//2, img_h//2), (255,0,0), 2)
        to_mid_x,to_mid_y = (img_w//2 - box_mid_x), (img_h//2 - box_mid_y) 
        if abs(to_mid_x) < 15 and abs(to_mid_y) < 15:
            cv2.rectangle(frame, (img_w//2-20,img_h//2-20), (img_w//2+20, img_h//2+20), (0,0,255),3,1)
            # 이미지에 글자 합성하기
            img = cv2.putText(frame, "Safe Zone", (img_w//2-100, img_h//2-100), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 1, cv2.LINE_AA)
    else : frame = raw_img
    return frame,a,b,a+w,b+h, raw_img ,to_mid_x,to_mid_y
