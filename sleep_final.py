import pyautogui as gui

total_len = gui.size()

from imutils.video import WebcamVideoStream
from imutils.video import FPS

import os
import  cv2
import  dlib
import  numpy
import  sys

import imutils


PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


def get_landmarks(im):
      rects = detector(im,  0) 
      if  len(rects) !=  1  :  
            return  None    
      return  numpy.matrix([[p.x,  p.y] for p in  predictor(im,  rects[0]).parts()])
def distance(B,C):
  return (B[0]-C[0])*(B[0]-C[0]) + (B[1]-C[1])*(B[1]-C[1])  


vs = WebcamVideoStream(src=0).start()

frame = None  

temp=0
threshold=0
initial=0
z=0
#t1=0
lowest=153
highest=0
fault=0
counter=0

while not vs.stopped:
    frame = vs.read()
    rects = detector(frame, 0)
    pointer=None

    if len(rects) == 1:     
    	landmarks1 = get_landmarks(frame)
    	# for i in  predictor(frame, rects[0]).parts() :
			# cv2.circle(frame,tuple([i.x,i.y]), 3, (0,0,255), -1)    		
    	if landmarks1  != None  :
    		A = numpy.squeeze(numpy.asarray(landmarks1))
    		if temp<7 :
    			temp=temp+1
    			if ((distance(A[37] , A[41])) < lowest):
    				lowest = (distance(A[37] , A[41]))
    			
    			if ((distance(A[37] , A[41])) > highest):
    				highest = (distance(A[37] , A[41]))
    			 
    			initial = (distance(A[37] , A[41]))+initial
    		
    		# print (distance(A[37] , A[41]))
    		# print (initial)
    		    		
    		if temp==7 :
    			temp=temp+1
    			initial = (initial-lowest-highest)/5
    			if (initial<50): 
    				threshold = initial - 10
    			elif (50<initial<100): 
    				threshold = initial - 20
    			elif (100<initial): 
    				threshold = initial - 40
    				
    		
    		# print("threshold",threshold)
    			
    		if ((threshold > (distance(A[37] , A[41]))) ):
    			
    			# print("saga")
    			
    			counter=counter+1
    			# print("counter",counter)
    			# print("fault",fault)
    			
    			if(counter>=30):
    				# print("sleep")
    				#gui.hotkey('volumemute')
    				os.system("sleep 1 && xset dpms force off")
    			
    				break
#TODO: no points detected sleep    		
    		else:
    			if(counter>5):
    				fault=fault+1
    				if(fault>=3):
    					counter=0
    					fault=0
    			
    		
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
#cap.release()
cv2.destroyAllWindows()
