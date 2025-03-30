import cv2 #Handles Graphics- Reading, Writing, Drawing
import numpy as np #General Computational Tools
from pynput import keyboard #Keyboard Control

#Setting up Camera
cam = cv2.VideoCapture(0)
result, frame = cam.read();

#Initializing Variables for Frame and Search
(HEIGHT,WIDTH) = frame.shape[0:2]
X,Y = int(WIDTH/2),int(HEIGHT/2);
searchLimit = int(0.01*WIDTH);
dX,dY = searchLimit,searchLimit

#Function to search complete Frame
def resetSpot():
    global X,Y,searchLimit
    Y,X = np.unravel_index(np.argmax(frame[:,:,0]),frame[:,:,0].shape)
    searchLimit = int(0.01*WIDTH)

#Event Handler
def on_press(key):
    print("Pressed: ",type(key));
    key = key.char
    if(key == 'q'):
        cam.release()
        print("PROGRAM COMPLETE");
        exit();
    if(key == 'r'):
        resetSpot();
    if(key == 'w'):
        input();
        return;

listener = keyboard.Listener(on_press=on_press)
listener.start()


print("STARTING")
resetSpot()
while(True):
    #Reading Frame
    result, frame = cam.read()
    frame = cv2.flip(frame,1);

    #Finding search limit and getting area to search
    searchLimit = int(np.clip(2.5*(dX**2 + dY**2)**0.5,0.02*WIDTH,HEIGHT))
    if(searchLimit > 0.9*HEIGHT):
        resetSpot();
    intensity = frame[max(0,Y-searchLimit):min(Y+searchLimit,HEIGHT),
                      max(0,X-searchLimit):min(X+searchLimit,WIDTH),
                      0]
    
    #Finding the Brightest Spot
    dY,dX = np.unravel_index(np.argmax(intensity),intensity.shape)
    dX -= 0.5*intensity.shape[0];
    dY -= 0.5*intensity.shape[1];
    X = int(np.clip((X + dX),0,WIDTH))
    Y = int(np.clip((Y + dY),0,HEIGHT))   

    #Drawing and displaying
    cv2.rectangle(frame,(X - searchLimit,Y - searchLimit),(X+searchLimit,Y+searchLimit),1)
    cv2.circle(frame,(X,Y),int(0.01*WIDTH),(0,0,0))
    cv2.imshow("myImg",frame);
    
    cv2.waitKey(1)
    print("RUNNING");

print("OUT OF LOOP");



