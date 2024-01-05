from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from attendanceManagement.mqtt import publish_msg


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentification page using React Js and Django!'}
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
    #permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Extract JSON data from the request
            json_data = request.data

            # Connect to MQTT broker
            mqtt_client = publish_msg.connect_mqtt()
            mqtt_client.loop_start()

            # Publish the JSON data to the MQTT topic
            publish_msg.publish(mqtt_client, json_data)

            return Response({'message': 'Configuration sent to MQTT'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to send configuration to MQTT'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)