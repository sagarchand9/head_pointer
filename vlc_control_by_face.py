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




vs = WebcamVideoStream(src=0).start()

#cap = cv2.VideoCapture(0)


frame = None  

#while(cap.isOpened()):
while not vs.stopped:
		frame = vs.read()
				
		#ret, frame = cap.read()   
		
		rects = detector(frame, 0)


		if len(rects) >= 1: 
			#TODO:play here 
			os.system("vlc-ctrl play")   
			landmarks1 = get_landmarks(frame)
			for i in  predictor(frame, rects[0]).parts() :
			 	cv2.circle(frame,tuple([i.x,i.y]), 3, (0,0,255), -1)
				
			
		else:
			#TODO:pause here	
			os.system("vlc-ctrl pause")
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
				break

				
#cap.release()
cv2.destroyAllWindows()
