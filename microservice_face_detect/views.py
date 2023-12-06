from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN

class FaceDetect(APIView):

    def is_Face(self, detector, image):
        faces = detector.detect_faces(image)
        print(faces)
        return len(faces) > 0

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('image')
        
        if not uploaded_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Assuming the uploaded file is an image
            image = plt.imread(uploaded_file)
        except Exception as e:
            return Response({'error': 'Invalid image file'}, status=status.HTTP_400_BAD_REQUEST)

        detector = MTCNN()
        has_face = self.is_Face(detector, image)

        response_data = {
            "face": has_face,
        }

        print(response_data)

        return Response(response_data, status=status.HTTP_200_OK)
