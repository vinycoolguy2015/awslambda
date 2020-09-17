import face_recognition
import cv2
import time
import sys
import subprocess
video_capture = cv2.VideoCapture(0)
count=1
#known_image=face_recognition.load_image_file("/Users/viny/Downloads/Python/VK.jpg")
known_image=face_recognition.load_image_file("/Users/viny/Downloads/Python/vinayak.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]
found=False
while count<3:
        count+=1
        time.sleep(1)
        try:
                ret, frame = video_capture.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                face_encoding = face_recognition.face_encodings(small_frame)[0]
                match = face_recognition.compare_faces([known_face_encoding], face_encoding)
                if match[0]:
                        found=True
                        print("Hey Dude")
                        break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        if found==False:
                                print("Unknown user")
                        break
        except:
                print("Unknown user")
                #subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend',shell=True)
                subprocess.call(['sh', '/Users/viny/Downloads/Python/lock_system.sh'])
                sys.exit()
        if found==False:
                print("Unknown user")
                #subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend',shell=True)
                subprocess.call(['sh', '/Users/viny/Downloads/Python/lock_system.sh'])
video_capture.release()
cv2.destroyAllWindows()
