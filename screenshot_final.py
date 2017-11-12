import pyautogui as gui
from imutils.video import WebcamVideoStream
from imutils.video import FPS

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
initial=0
z=0
t1=0
flag=0

while not vs.stopped:
    frame = vs.read()    
    rects = detector(frame, 0)
  
    if len(rects) == 1:     
    	landmarks1 = get_landmarks(frame)
    	#for i in  predictor(frame, rects[0]).parts() :
		#	cv2.circle(frame,tuple([i.x,i.y]), 3, (0,0,255), -1)  		
    	if landmarks1  != None  :
    		A = numpy.squeeze(numpy.asarray(landmarks1))
    		if temp<5 :
    			temp=temp+1
    			initial = (distance(A[37] , A[41]))+initial
    		# print (distance(A[37] , A[41]))
    		# print (initial)
    		elif temp==5 :
    			temp=temp+1
    			initial = initial/5
    		print("yo",(initial - (distance(A[37] , A[41])) ))
        if ((initial - (distance(A[37] , A[41])) ) > 55):
    			#print("yo",(initial - (distance(A[37] , A[41])) ))
    			flag=1
    			
        elif (((initial - (distance(A[37] , A[41])) ) <= 55) and (flag==1)):
          # print("We shot you here. Ha! Ha! Ha! Ha! ","Total Kills : "+str(z))
    			gui.screenshot('foo'+str(z)+'.png')

    			z=z+1
    			flag=0
    			#break
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
#cap.release()
cv2.destroyAllWindows()
