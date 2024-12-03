from django.shortcuts import render
from django.http import JsonResponse
from .utils import predict_waste
import os
from django.conf import settings

def upload_and_detect(request):
    if request.method == 'POST':
        # Handle the uploaded image
        uploaded_image = request.FILES.get('file')
        if not uploaded_image:
            return JsonResponse({'error': 'No image uploaded'}, status=400)

        # Save the image to the media directory
        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.name)
        with open(save_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # Get the URL of the uploaded image
        image_url = os.path.join(settings.MEDIA_URL, uploaded_image.name)

        # Perform waste detection
        try:
            detected_category = predict_waste(save_path)
            return JsonResponse({
                'detected_category': detected_category,
                'image_url': image_url  # Return the image URL for display
            })
        except Exception as e:
            return JsonResponse({'error': f"Prediction error: {str(e)}"}, status=500)

    # Render the upload and detection page for GET requests
    return render(request, 'main.html')


# Create your views here.
def sample(request):
    return render(request, 'main.html')