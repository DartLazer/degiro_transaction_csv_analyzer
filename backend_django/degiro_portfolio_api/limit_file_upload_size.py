from django.http import JsonResponse

class LimitUploadSizeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            max_size = 5_000_000  # 2MB
            content_length = int(request.META.get('CONTENT_LENGTH', 0))
            if content_length > max_size:
                return JsonResponse({'error': 'File size too large'}, status=400)

        return self.get_response(request)
