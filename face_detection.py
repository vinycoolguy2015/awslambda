import face_recognition
import cv2
import time
import sys
import subprocess
video_capture = cv2.VideoCapture(0)
count=1
known_image=face_recognition.load_image_file("Known/modified.jpg")
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
                        print("Hey Vinayak")
                        break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        if found==False:
                                print("Not found")
                        break
        except IndexError:
                print("Not found")
                subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend',shell=True)
                sys.exit()
        if found==False:
                print("Not found")
                subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend',shell=True)

video_capture.release()
cv2.destroyAllWindows()
