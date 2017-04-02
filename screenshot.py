import pyautogui as gui

total_len = gui.size()


import  cv2
import  dlib
import  numpy
import  sys


PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
ALIGN_POINTS  =  (list(range(0, 68))  )

detector = dlib.get_frontal_face_detector()
# detector2= face_recognition_model_v1() 
predictor = dlib.shape_predictor(PREDICTOR_PATH)


def get_landmarks(im):
      rects = detector(im,  0) 
      if  len(rects) !=  1  :  
            return  None    
      return  numpy.matrix([[p.x,  p.y] for p in  predictor(im,  rects[0]).parts()])

def get_image_mask(im):
  #  mask = cv2.Mat(im.size(),  cv2.CV_8UC3)  # TODO: Can change  to 1 Channel
  mask = numpy.zeros((im.shape[0], im.shape[1],  3),  dtype=numpy.uint8)
  for  i  in range(im.shape[0]):
    for j in  range(im.shape[1]):
      mask_value = im[i, j,  3]/255
      mask[i,  j] = [mask_value,  mask_value,  mask_value]
  return mask
  
def distance(B,C):
  return (B[0]-C[0])*(B[0]-C[0]) + (B[1]-C[1])*(B[1]-C[1])  

      
def transformation_from_points(points1, points2):
      points1 = points1.astype(numpy.float64)
      points2 = points2.astype(numpy.float64)

      c1  =  numpy.mean(points1,  axis=0)
      c2  =  numpy.mean(points2,  axis=0)
      points1 -=  c1
      points2 -=  c2
      s1  =  numpy.std(points1)
      s2  =  numpy.std(points2)
      points1 /=  s1
      points2 /=  s2

      U,  S, Vt  =  numpy.linalg.svd(points1.T * points2)
      R = (U  *  Vt).T

      return  numpy.vstack([numpy.hstack(((s2  /  s1)  *  R,
                                                           c2.T - (s2 / s1) * R * c1.T)),
                                      numpy.matrix([0.,  0.,  1.])])

def warp_im(im, M,  dshape):
      output_im = numpy.zeros(dshape, dtype=im.dtype)
      cv2.warpAffine(im,
                             M[:2],
                             (dshape[1],  dshape[0]),
                             dst=output_im,
                             borderMode=cv2.BORDER_TRANSPARENT,
                             flags=cv2.WARP_INVERSE_MAP)
      return  output_im

def thread_start(event):
    import threading
    th = threading.Thread(target=testFunction, args=(event,))
    th.start()





cap = cv2.VideoCapture(0)

frame = None  

temp=0
initial=0
z=0
t1=0
while(cap.isOpened()):
    # print cap.get(3), cap.get(4)
    
    ret, frame = cap.read()   
    
    rects = detector(frame, 0)
    pointer=None
    counter = 0

    if len(rects) == 1:     
    	landmarks1 = get_landmarks(frame)
    	#for i in  predictor(frame, rects[0]).parts() :
		#	cv2.circle(frame,tuple([i.x,i.y]), 3, (0,0,255), -1)
    		
    	if landmarks1  != None  :
    		A = numpy.squeeze(numpy.asarray(landmarks1))
    		if temp<5 :
    			temp=temp+1
    			initial = (distance(A[37] , A[41]))+initial
    		
    		print (distance(A[37] , A[41]))
    		print (initial)
    		    		
    		if temp==5 :
    			temp=temp+1
    			initial = initial/5
    		
    			
    		if ((initial - (distance(A[37] , A[41])) ) > 55):
    			print("yo",(initial - (distance(A[37] , A[41])) ))
    			print(z)
    			#gui.typewrite('Hello world!', interval=0.25)	
    			#gui.hotkey( 'q')	
    			if(t1==1):
    				gui.screenshot('foo'+str(z)+'.png')
    				z=z+1
    				t1=0
    			t1=1
    			#break
    

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
cap.release()
cv2.destroyAllWindows()
