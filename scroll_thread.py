import pyautogui as gui
from posture import posture_final 
total_len = gui.size()

from imutils.video import WebcamVideoStream
from imutils.video import FPS

import  cv2
import  dlib
import  numpy
import imutils


def get_landmarks(im):
      rects = detector(im,  0) 
      if  len(rects) !=  1  :  
            return  None    
      return  numpy.matrix([[p.x,  p.y] for p in  predictor(im,  rects[0]).parts()])


PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

vs = WebcamVideoStream(src=0).start()
#cap = cv2.VideoCapture(0)

counter = 0 
temp  =0 
 
gui.FAILSAFE  = False

while not vs.stopped:
#while(cap.isOpened()):
    # print cap.get(3), cap.get(4)
    
    frame = vs.read()
    #ret, frame = cap.read()   
    
    rects = detector(frame, 0)
    pointer=None
    counter = 0
    if len(rects) == 1:       
      for i in  predictor(frame, rects[0]).parts() :
        cv2.circle(frame,tuple([i.x,i.y]), 3, (0,0,255), -1)
        if counter == 29: 
          if temp  == 0:
            temp = 1
            intial  = tuple([i.x,i.y])
          else : 
            pointer = tuple([i.x,i.y])
            if pointer[1] - intial[1] > 20:
              # cv2.waitKey(0)       
              gui.scroll(-1)

            if pointer[1] - intial[1] < 20:
              # cv2.waitKey(0)       
              gui.scroll(1)
                      
    #       # pointer = tuple([i.x,i.y])
    #       # print pointer     
        counter = counter + 1
        


    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
#cap.release()
cv2.destroyAllWindows()
