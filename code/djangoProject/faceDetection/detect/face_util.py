import cv2
from skimage.metrics import structural_similarity as ssim


def detect_faces(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haarcascades face classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    # Extract faces from the image
    face_images = [image[y:y+h, x:x+w] for (x, y, w, h) in faces]

    return face_images


def compare_faces_similarity(faces_existing, faces_uploaded):
    # Calculate similarity scores for each pair of faces using SSIM or other measures
    similarity_scores = []

    for face_existing in faces_existing:
        for face_uploaded in faces_uploaded:
            # Resize faces to have the same dimensions
            face_existing_resized = cv2.resize(face_existing, (face_uploaded.shape[1], face_uploaded.shape[0]))

            # Convert faces to grayscale
            gray_face_existing = cv2.cvtColor(face_existing_resized, cv2.COLOR_BGR2GRAY)
            gray_face_uploaded = cv2.cvtColor(face_uploaded, cv2.COLOR_BGR2GRAY)

            # Calculate the SSIM score
            ssim_score, _ = ssim(gray_face_existing, gray_face_uploaded, full=True)

            similarity_scores.append(ssim_score)

    return similarity_scores
