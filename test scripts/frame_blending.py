import cv2
import numpy as np
import os
   
# Create a VideoCapture object and read from input file
f = '../test_clips/C0214-4.2.2.10bit.MP4'
if os.path.isfile(f):
    print("IS FILE")
else:
    print("NOT FILE")
cap = cv2.VideoCapture(f,cv2.CAP_FFMPEG)
#cap = cv2.VideoCapture('C:/Users/elvin/Downloads/IF-RC01_0000.MP4')
#cap.set(cv2.CAP_PROP_POS_FRAMES, 60 * 10)

ret, frame_out = cap.read()

frame_out = (frame_out * 0).astype(np.float64)

mult = 3
num_blend = 3

i = 1

# Read until video is completed
while(cap.isOpened()):
        
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(frame.shape)
    if ret == True:
        
        # Display the resulting frame
        


        if (i-1) % mult == 0:
            # Reset frame at beginning of hyperlapse range
            print("reset")
            frame_out = frame_out * 0.0

        if (i-1) % mult < num_blend:
            print(f"adding {i}")
            frame_out += 1/(num_blend) * frame.astype(np.float64)


        if ((i-1) - num_blend + 1) % mult == 0:
            cv2.imshow('Frame', frame_out.astype(np.uint8))

            cv2.waitKey(5)


        i += 1
        # Press Q on keyboard to  exit
        if 0xFF == ord('q'):
            break
    else: 
        break

cap.release()
cv2.destroyAllWindows()