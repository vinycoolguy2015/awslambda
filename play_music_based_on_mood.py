import cv2
import boto3
import subprocess

def main():
    capture = capture_write()
    play_music()

def capture_write(filename="image.jpeg", port=0, ramp_frames=30, x=1280, y=720):
    camera = cv2.VideoCapture(port)
    # Set Resolution
    camera.set(3, x)
    camera.set(4, y)
    # Adjust camera lighting
    for i in range(ramp_frames):
        temp = camera.read()
    retval, im = camera.read()
    cv2.imwrite(filename,im)
    del(camera)
    return True

def play_music(filename="image.jpeg",bucket="vinytest1989"):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket)
    s3.Bucket(bucket).upload_file(filename ,"image.jpeg")
    rek = boto3.client('rekognition')
    response_face = rek.detect_faces(Image={'S3Object': {'Bucket': bucket,'Name': filename,}},Attributes = ['ALL'])
    if response_face['FaceDetails'][0]['Smile']['Value'] == False:
        subprocess.Popen(["afplay", "Jaanan.mp3"])
    else:
        subprocess.Popen(["afplay", "Aaankh_Uthi.mp3"])

if __name__ == '__main__':
    main()
