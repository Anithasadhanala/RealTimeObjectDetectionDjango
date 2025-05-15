from ultralytics import YOLO
import cv2
import numpy as np
import math
import os

from gtts import gTTS
from playsound import playsound

audio_file = os.path.dirname(__file__) + 'appoutput.mp3'

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(audio_file)

list = []

class openCamera(object):

    
    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        #_,img = self.url.read()

        cap = cv2.VideoCapture(0)
        cap.set(3, 1600)
        cap.set(4, 400)

        # model
        model = YOLO("model/yolov8n.pt") 


        # object classes
        classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                    "teddy bear", "hair drier", "toothbrush"]
        
        COLORS = np.random.uniform(0, 255, size=(len(classNames), 3))

        temp = ""
        while True:
            _, img = cap.read()
            print(img)
            overlay = img.copy()
            results = model(img, stream=True)
        
            # coordinates

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    print(x1,x2,y1,y2)
                    # put box in cam
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), COLORS[int(box.cls[0])], cv2.FILLED)
                    
                    cv2.rectangle(overlay, (x1, y1), (x2, y2), COLORS[int(box.cls[0])], 2)

                    # confidence
                    confidence = math.ceil((box.conf[0]*100))/100
                    print("Confidence --->",confidence)
                    

                    # class name
                    cls = int(box.cls[0])

                    
                    
                    
                    print("Class name -->", classNames[cls])
                    list.append(classNames[cls])
                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 0.8
                    color = (215, 0, 0)
                    thickness = 2
                    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                    

                    #cv2.putText(overlay, classNames[cls], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, fontScale , (255, 255, 255), thickness, cv2.LINE_AA)
                    frame = cv2.addWeighted(img,0.3,overlay,0.7,gamma=0)
                    

            # if classNames[cls] != temp:
            #             try:
            #                 text_to_speech(classNames[cls])
            #                 playsound(audio_file)
            #                 os.remove(audio_file)
            #             except:
            #                 pass

            temp = classNames[cls]
            cv2.imshow('Object Detection. Press q to stop', frame)
            #cv2.setWindowProperty('Object Detection. Press q to stop', cv2.WND_PROP_TOPMOST, 1)
            cv2.moveWindow("Object Detection. Press q to stop", 68, 110) 
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()




