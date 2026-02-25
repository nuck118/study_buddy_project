class NgrokSkipWarningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Add the header to the response
        response["ngrok-skip-browser-warning"] = "any-value"
        return response
        