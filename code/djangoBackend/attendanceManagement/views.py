# Create your views here.
import datetime
import json
import os
import base64

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from attendanceManagement.models import Department, EmployeeDetails
from attendanceManagement.mqtt import publish_msg
from django.conf import settings
from attendanceManagement.face_detection import recognize_faces_image, encode_faces
from attendanceManagement.control_logic import request_handler, serializers

# --------------- Tested --------------


# Home View
class HomeView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, 'index.html')


# Log Out REST endpoint
class LogoutView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Configure Mode REST endpoint
class ConfigureDeviceView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            publish_msg.run(request.data)

            return Response({'message': 'Configuration sent to MQTT'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to send configuration to MQTT: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Active Mode REST endpoint
class ActiveDeviceView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            publish_msg.run(request.data)

            return Response({'message': 'Activation sent to MQTT'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to send activation to MQTT: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Save & Get Topic Details
class SaveTopicView(APIView):
    serializer_class = serializers.TopicSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Topic saved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            # Call the get_all_topics function
            all_topics = request_handler.get_all_topics()

            # Serialize the topics into a JSON response using TopicSerializer
            serialized_data = self.serializer_class(all_topics, many=True).data

            return JsonResponse({'all_topics': serialized_data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid request'}, status=400)


# Save & Get Department Details
class SaveDepartmentView(APIView):
    serializer_class = serializers.DepartmentSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'saved successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_departments = request_handler.get_all_departments()
            serialized_data = self.serializer_class(all_departments, many=True).data
            return JsonResponse({'all_departments': serialized_data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid request'}, status=400)


# Save & Get Device Details
class SaveDeviceView(APIView):
    serializer_class = serializers.DeviceSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Device saved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            # Call the get_all_device function
            all_devices = request_handler.get_all_devices()

            # Serialize the devices into a JSON response using DeviceSerializer
            serialized_data = self.serializer_class(all_devices, many=True).data

            return JsonResponse({'all_devices': serialized_data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid request'}, status=400)


# Create New Employee Class
class EmployeeCreateView(APIView):
    serializer_class = serializers.EmployeeDetailsSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Employee saved successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid format', 'details': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            # Call the get_all_device function
            all_emp = request_handler.get_all_emp()

            # Serialize the devices into a JSON response using DeviceSerializer
            serialized_data = self.serializer_class(all_emp, many=True).data

            return JsonResponse({'all_emp': serialized_data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid request'}, status=400)


# Get Employee Details According to the email
class GetEmployeeDetailsView(APIView):
    serializer_class = serializers.EmployeeDetailsSerializer

    def get(self, request, emp_email):
        try:
            emp_details = request_handler.get_emp_email(emp_email=emp_email)
            serializer = self.serializer_class(emp_details)
            return JsonResponse({'Emp_detail': serializer.data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid emp_id or month'}, status=400)


# Get attendance details according to the emp_id and month
class GetAttendanceView(APIView):
    serializer_class = serializers.AttendanceDetailsSerializer

    def get(self, request, emp_id, month):
        try:
            emp_id = int(emp_id)
            month = int(month)

            attendance_details = request_handler.get_attendance_details(emp_id=emp_id, month=month)

            # Serialize the attendance details using AttendanceSerializer
            serializer = self.serializer_class(attendance_details, many=True)
            serialized_data = serializer.data

            return JsonResponse({'attendance_details': serialized_data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid emp_id or month'}, status=400)


# Get all attendance details
class GetAllAttendanceView(APIView):
    serializer_class = serializers.AttendanceDetailsSerializer

    def get(self, request):
        try:
            attendance_details = request_handler.get_all_attendance_details()
            serializer = self.serializer_class(attendance_details, many=True)
            serialized_data = serializer.data
            return JsonResponse({'attendance_details': serialized_data}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid emp_id or month'}, status=400)


class GetEmployeesWithoutFaceView(APIView):
    serializer_class = serializers.EmployeeDetailsSerializer

    def get(self, request):
        try:
            employees_without_face = request_handler.get_emp_face_false()
            serializer = self.serializer_class(employees_without_face, many=True)
            serialized_data = serializer.data

            return Response({'employees_without_face': serialized_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetEmployeesWithoutFPView(APIView):
    serializer_class = serializers.EmployeeDetailsSerializer

    def get(self, request):
        try:
            employees_without_fp = request_handler.get_emp_fp_false()
            serializer = self.serializer_class(employees_without_fp, many=True)
            serialized_data = serializer.data

            return Response({'employees_without_fp': serialized_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Save the face images of employees
class StoreFacesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            image_file_64 = request.data.get('image')
            emp_id_value = request.data.get('emp_id')

            if not image_file_64 or not emp_id_value:
                return Response({'error': 'Image file and Employee ID are required'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                emp_id = int(emp_id_value)
                employee = request_handler.get_emp_id(emp_id)
            except ValueError:
                return Response({'error': 'Invalid emp_id format'}, status=status.HTTP_400_BAD_REQUEST)

            # Decode the image file
            image_file = base64.b64decode(image_file_64)

            # Save the image using a function similar to save_image
            image_path = self.save_face_image(image_file, employee)
            request_handler.set_face(emp_id)

            return Response({'message': 'Image saved successfully', 'image_path': image_path},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_face_image(self, image_file, employee):

        save_path = 'datasets'
        folder_path = os.path.join(settings.MEDIA_ROOT, save_path, str(employee.emp_id))
        os.makedirs(folder_path, exist_ok=True)

        # Count the existing files in the directory
        count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

        # Increment the count for the new image
        count += 1

        filename = f"{count}.jpg"

        # Full path where the image will be saved
        full_path = os.path.join(folder_path, filename)
        os.makedirs(folder_path, exist_ok=True)

        with open(full_path, 'wb') as destination:
            destination.write(image_file)

        return full_path


# Encode Faces REST endpoint
class EncodeFaces(APIView):
    def get(self, request, *args, **kwargs):
        try:
            message = encode_faces.quantify_faces()
            return Response({'message': message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Storing the photo and mark attendance REST endpoint
class MarkAttendanceView(APIView):
    serializer_class = serializers.AttendanceDetailsSerializer

    def post(self, request, *args, **kwargs):
        try:
            image_file_64 = request.data.get('image')
            in_time = request.data.get('in_time')

            if not image_file_64:
                return Response({'error': 'Image file is required'}, status=status.HTTP_400_BAD_REQUEST)

            image_file = base64.b64decode(image_file_64)
            # Save the image to a folder
            image_path = self.save_image(image_file)
            emp_id = self.get_name(image_path)

            if emp_id == "Unknown":
                return Response({'message': 'Face Data is not in the database', 'emp_id': emp_id},
                                status=status.HTTP_200_OK)

            else:
                data = {
                    'emp': emp_id,
                    'date': datetime.date.today(),
                    'present': True,
                    'in_time': in_time
                }

                try:
                    serializer = self.serializer_class(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'message': 'Attendance saved successfully', 'emp_id': emp_id}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

                except Exception as e:
                    return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_image(self, image_file):
        save_path = 'captured'
        file_name = 'capture.jpg'

        # Full path where the image will be saved
        full_path = os.path.join(settings.MEDIA_ROOT, save_path, file_name)

        os.makedirs(os.path.join(settings.MEDIA_ROOT, save_path), exist_ok=True)

        # Write the byte data directly to the file
        with open(full_path, 'wb') as destination:
            destination.write(image_file)

        return full_path

    def get_name(self, image_file):
        id_arr = recognize_faces_image.recognize_face(image_file)

        if len(id_arr) == 1:
            return id_arr[0]


# Save New PIN to the database
class StorePinView(APIView):
    serializer_class = serializers.PinDataSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'saved successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Check entered pin
class CheckPinView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            emp_id_value = request.data.get('emp_id')
            pin_code = request.data.get('pin_code')

            if not pin_code or not emp_id_value:
                return Response({'error': 'PIN Code and Employee ID are required'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                state = request_handler.check_pin(emp_id_value, pin_code)

                return Response({'message': 'Unlock Door', 'Status': state},
                                status=status.HTTP_200_OK)

            except ValueError:
                return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Save device lock statue
class StoreDeviceLockView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            device_id = request.data.get('device_id')
            lock_state = request.data.get('lock_state')

            if not device_id or not lock_state:
                return Response({'error': 'Device ID and State are required'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                state = request_handler.update_device_lock_status(device_id, lock_state)

                return Response({'message': 'Unlocking Successful: ', 'Status': state},
                                status=status.HTTP_200_OK)

            except ValueError:
                return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Storing the fingerprints state
class StoreFPView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            emp_id_value = request.data.get('emp_id')

            if not  emp_id_value:
                return Response({'error': 'Employee ID is required'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                emp_id = int(emp_id_value)
            except ValueError:
                return Response({'error': 'Invalid emp_id format'}, status=status.HTTP_400_BAD_REQUEST)

            request_handler.set_fp(emp_id)

            return Response({'message': 'Fingerprint saved successfully'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



