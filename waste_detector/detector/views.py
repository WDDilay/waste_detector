from django.shortcuts import render
from django.http import JsonResponse
from .utils import predict_waste
import os
from django.conf import settings
import base64
from django.core.files.base import ContentFile

def upload_and_detect(request):
    if request.method == 'POST':
        # Handle the uploaded image
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': 'No image uploaded'}, status=400)

        # Generate a unique filename
        filename = f"waste_image_{uploaded_file.name}"
        save_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Save the image
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Get the URL of the uploaded image
        image_url = os.path.join(settings.MEDIA_URL, filename)

        # Perform waste detection
        try:
            detected_category = predict_waste(save_path)
            return JsonResponse({
                'detected_category': detected_category,
                'image_url': image_url
            })
        except Exception as e:
            return JsonResponse({'error': f"Prediction error: {str(e)}"}, status=500)

    # Render the upload and detection page for GET requests
    return render(request, 'analyze.html')

def main(request):
    return render(request, 'main.html')

def analyze(request):
    return render(request, 'analyze.html')

