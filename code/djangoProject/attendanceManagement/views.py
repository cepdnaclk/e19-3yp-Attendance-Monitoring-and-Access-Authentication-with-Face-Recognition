import json
import os
import time

from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from attendanceManagement.models import Face_Data, Employee
from attendanceManagement.mqtt import publish_msg
from attendanceManagement.control_logic import request_handler
from django.conf import settings
from attendanceManagement.face_detection import recognize_faces_image, encode_faces


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ConfigureDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            publish_msg.run(request.data)

            return Response({'message': 'Configuration sent to MQTT'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to send configuration to MQTT: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
class ActiveDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            publish_msg.run(request.data)

            return Response({'message': 'Activation sent to MQTT'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to send activation to MQTT: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Storing the photo and mark attendance REST endpoint
class MarkAttendanceView(APIView):



    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            image_file = request.data.get('image')

            if not image_file:
                return Response({'error': 'Image file is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the image to a folder
            image_path = self.save_image(image_file)
            print(image_path)
            emp_id = self.get_name(image_path)

            return Response({
                'message': f'Image saved successfully for Employee ID: {emp_id}',
                'image_path': image_path,
                'emp_id': emp_id
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_image(self, image_file):
        save_path = 'captured'  # Folder name
        file_name = 'capture.jpg'  # Fixed filename

        # Full path where the image will be saved
        full_path = os.path.join(settings.MEDIA_ROOT, save_path, file_name)

        os.makedirs(os.path.join(settings.MEDIA_ROOT, save_path), exist_ok=True)

        with default_storage.open(full_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        return full_path

    def get_name(self, image_file):

        id_arr = recognize_faces_image.recognize_face(image_file)

        if len(id_arr) == 1:
            return id_arr[0]


class StoreFacesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            image_file = request.data.get('image')
            emp_id_value = request.data.get('emp_id')

            if not image_file or not emp_id_value:
                return Response({'error': 'Image file and Employee ID are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                emp_id = int(emp_id_value)
                employee = get_object_or_404(Employee, emp_id=emp_id)
            except ValueError:
                return Response({'error': 'Invalid emp_id format'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the image to the specified path using the upload_to function
            face_data = Face_Data(emp_id=employee, face=image_file)
            face_data.save()

            # Get the saved image path
            image_path = face_data.face.url

            return Response({'message': 'Image saved successfully', 'image_path': image_path}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EncodeFaces(APIView):
    def get(self, request, *args, **kwargs):
        try:
            message = encode_faces.quantify_faces()
            return Response({'message': message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
