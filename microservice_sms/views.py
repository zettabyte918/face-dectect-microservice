import base64
import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

class SendSMSView(APIView):
    def post(self, request: Request, *args, **kwargs):
        # Get the phone number and message from the request data
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')

        if not phone_number or not message:
            return Response({'error': 'Phone number and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Orange API endpoint for obtaining an access token
        token_url = 'https://api.orange.com/oauth/v3/token'

        # Replace 'your_client_id' and 'your_client_secret' with your actual Orange API client credentials
        basic_token = "Basic ZTdrV0RKSHA5U05RZ1F0RmdIU21OMnB0Q05BMFZaSEc6ZEVoQVN3QjZTSGR3OUFNcA=="

        # Headers for obtaining the access token
        token_headers = {
            'Authorization': basic_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        # Data for obtaining the access token
        token_data = {
            'grant_type': 'client_credentials',
        }

        # Make a POST request to obtain the access token
        try:
            token_response = requests.post(token_url, headers=token_headers, data=token_data)
            token_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to obtain access token: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Extract the access token from the response
        access_token = token_response.json().get('access_token')

        # Orange API endpoint for sending SMS
        orange_api_url = f'https://api.orange.com/smsmessaging/v1/outbound/tel:+21627515642/requests'

        # Headers for the SMS request
        sms_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        # Build the JSON payload for the Orange API request
        payload = {
            'outboundSMSMessageRequest': {
                'address': f'tel:+216{phone_number}',
                'senderAddress': 'tel:+21627515642',
                'senderName': "LES EXPERTS",
                'outboundSMSTextMessage': {
                    'message': message,
                }
            }
        }

        # Make a POST request to the Orange API to send SMS
        try:
            sms_response = requests.post(orange_api_url, headers=sms_headers, data=json.dumps(payload))
            sms_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to send SMS: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check the response status and return True or False accordingly
        if sms_response.status_code == 201:
            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': f'Orange API returned status code {sms_response.status_code}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
