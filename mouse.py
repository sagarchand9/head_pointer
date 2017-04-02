import pyautogui as gui

total_len = gui.size()


import  cv2
import  dlib
import  numpy

def get_landmarks(im):
      rects = detector(im,  0) 
      if  len(rects) !=  1  :  
            return  None    
      return  numpy.matrix([[p.x,  p.y] for p in  predictor(im,  rects[0]).parts()])


PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
# detector2= face_recognition_model_v1() 
predictor = dlib.shape_predictor(PREDICTOR_PATH)

cap = cv2.VideoCapture(0)

counter = 0 
max_len = 373 - 252
max_height = 258-209
total_len = gui.size()
desk_len = total_len[0]
desk_height = total_len[1]
ratio_len= desk_len / max_len
ratio_height =  desk_height / max_height
temp  =0 
desk_len_intial= total_len[0] /2 
desk_height_intial= total_len[1] /2 
  
while(cap.isOpened()):
    # print cap.get(3), cap.get(4)
    
    ret, frame = cap.read()   
    
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
            
            pos_len = desk_len/2 - (pointer[0] - intial[0] )* ratio_len
            pos_height = desk_height/2 + (pointer[1] - intial[1] )* ratio_height

            gui.moveTo(pos_len,pos_height , duration= 0)
          
          # pointer = tuple([i.x,i.y])
          # print pointer
        if counter== 42 or counter== 43 or counter== 44 or counter== 45 or counter== 46 or counter== 47  :
            print counter , tuple([i.x,i.y])        
        counter = counter + 1
        
    else :
      print "==========="    

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
cap.release()
cv2.destroyAllWindows()
