import cv2

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

path = "/home/danandla/BOTAY/embedded/mk3/samples"
while(True):
    ret, frame = cap.read()  # return a single frame in variable `frame`
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite(path + '/photo/c1.jpg',frame)
        cv2.destroyAllWindows()
        break

cap.release()