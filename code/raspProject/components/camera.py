import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import requests
import base64
import time
from datetime import datetime


def camera_setup():
    camera = PiCamera()
    camera.rotation = 90
    camera.brightness = 70
    camera.contrast = 20
    camera.resolution = (640, 480)
    return camera


def detect_bounding_box(frame):
    cascade_path = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    face_classifier = cv2.CascadeClassifier(cascade_path)
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 15, minSize=(150, 150))
    return len(faces) > 0  # return True if a face was detected, False otherwise


def capture_face_detection():
    backend_url = "https://facesecure.azurewebsites.net/attendanceManagement/mark-attendance/"
    camera = camera_setup()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    emp_id = 0

    camera.start_preview()
    for frame_count, frame in enumerate(camera.capture_continuous(rawCapture, format="bgr"), 1):
        video_frame = frame.array  # Access the BGR image from the PiRGBArray

        if detect_bounding_box(video_frame):  # if a face was detected
            _, img_buffer = cv2.imencode('.jpg', video_frame)
            img_base64 = base64.b64encode(img_buffer).decode('utf-8')
            current_time = datetime.now().strftime("%H:%M:%S")[:-3]
            
            camera.stop_preview()
            cv2.destroyAllWindows()

            payload = {
                'in_time': str(current_time),
                'image': img_base64,
            }

            response = requests.post(backend_url, json=payload)

            if response.status_code == 200:
                print(f"Image {frame_count} uploaded successfully")
                emp_id = response.json().get('emp_id')
                print(f"Employee ID: {emp_id}")
            else:
                print(f"Error uploading image {frame_count}: {response.status_code}")
                print(response.text)
                # If there's an error, return False immediately
                camera.stop_preview()
                camera.close()
                cv2.destroyAllWindows()
                return 0, False

            rawCapture.truncate(0)
            break

        rawCapture.truncate(0)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.stop_preview()
    camera.close()
    cv2.destroyAllWindows()

    return emp_id, True



def capture_face_sending(emp_id):
    backend_url = "https://facesecure.azurewebsites.net/attendanceManagement/store-faces/"

    camera = camera_setup()
    time.sleep(0.1)
    rawCapture = PiRGBArray(camera)
    frame_count = 0
    max_frames = 3

    camera.start_preview()
    for frame in camera.capture_continuous(rawCapture, format="bgr"):
        video_frame = frame.array

        if detect_bounding_box(video_frame):  # if a face was detected
            # Encode image to base64
            _, img_buffer = cv2.imencode('.jpg', video_frame)
            img_base64 = base64.b64encode(img_buffer).decode('utf-8')

            # Send image to the backend
            payload = {
                'emp_id': emp_id,
                'image': img_base64,
            }

            response = requests.post(backend_url, json=payload)

            if response.status_code == 200:
                print(f"Image {frame_count + 1} uploaded successfully")
                frame_count += 1
            else:
                print(f"Error uploading image {frame_count + 1}: {response.status_code}")
                print(response.text)
                # If there's an error, return False immediately
                camera.stop_preview()
                camera.close()
                cv2.destroyAllWindows()
                return False

        #cv2.imshow("Face Detection", video_frame)  # display the processed frame
        rawCapture.truncate(0)  # clear the stream in preparation for the next frame

        if frame_count >= max_frames or cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.stop_preview()
    camera.close()
    cv2.destroyAllWindows()

    # If the loop completes successfully, return True
    return frame_count == max_frames
