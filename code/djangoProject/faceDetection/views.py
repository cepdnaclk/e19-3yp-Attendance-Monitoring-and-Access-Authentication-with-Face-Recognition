from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import os
from django.core.files.storage import default_storage
from .detect.face_util import detect_faces, compare_faces_similarity
from .mqtt.mqtt_connection import client as mqtt_client
import json


# Assuming the existing image file is in the same directory as views.py
existing_image_path = '/home/asela/Downloads/image.jpg'


# Face Detection and Recognition
@csrf_exempt
def compare_faces(request):
    if request.method == 'POST':
        # Load the existing image
        existing_image = cv2.imread(existing_image_path)

        # Check if the image is loaded successfully
        if existing_image is None:
            return JsonResponse({'result': 'Error loading the existing image'})

        # Get the uploaded image from the POST request
        uploaded_image = request.FILES.get('image')

        # Save the uploaded image temporarily
        uploaded_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded_image.jpg')
        with default_storage.open(uploaded_image_path, 'wb') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        # Load the uploaded image
        uploaded_image = cv2.imread(uploaded_image_path)

        # Check if the uploaded image is loaded successfully
        if uploaded_image is None:
            return JsonResponse({'result': 'Error loading the uploaded image'})

        # Detect faces in the existing image
        faces_existing = detect_faces(existing_image)

        # Detect faces in the uploaded image
        faces_uploaded = detect_faces(uploaded_image)

        # Compare faces using SSIM or other similarity measures
        similarity_scores = compare_faces_similarity(faces_existing, faces_uploaded)

        # Set a threshold for similarity
        similarity_threshold = 0.5  # You can adjust this value based on your requirements

        # Check if at least one face pair meets the similarity threshold
        if any(score > similarity_threshold for score in similarity_scores):
            result = 'Success'
        else:
            result = 'Failed'

        # Delete the temporarily uploaded image
        os.remove(uploaded_image_path)

        return JsonResponse({'result': result, 'similarity_scores': similarity_scores})

    else:
        return HttpResponse("Only POST requests are allowed.")


def say_hello(request):
    return render(request, 'hello.html', {'name': 'Asela H Premawansha'})


@csrf_exempt
def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})
