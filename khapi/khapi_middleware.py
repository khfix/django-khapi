class KhApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["X-Custom-Header"] = "My Custom Middleware Header"
        return response
