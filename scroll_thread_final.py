import pyautogui as gui

from imutils.video import WebcamVideoStream
from imutils.video import FPS

import  cv2
import  dlib
import  numpy
import imutils



PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

vs = WebcamVideoStream(src=0).start()

counter = 0 
temp  =0 
 
gui.FAILSAFE  = False

while not vs.stopped:
    
    frame = vs.read()    
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
            if pointer[1] - intial[1] > 30:
              gui.scroll(-1)

            elif pointer[1] - intial[1] < -30:
              gui.scroll(1)

            elif pointer[0] - intial[0] > 60 : 
              gui.press('left')
              cv2.waitKey(1000)       
            elif pointer[0] - intial[0] < -60 :
              gui.press('right' )  
              cv2.waitKey(1000)
          break    
        counter = counter + 1
        
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
#cap.release()
cv2.destroyAllWindows()
