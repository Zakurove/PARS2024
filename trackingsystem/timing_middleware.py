import time


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start time before view is called
        start_time = time.time()

        # Call the view (or the next middleware in line)
        response = self.get_response(request)

        # Calculate the duration
        duration = time.time() - start_time

        # Add the duration to the response
        response["X-Duration"] = str(duration)

        return response
