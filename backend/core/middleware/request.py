import uuid

from django.utils.deprecation import MiddlewareMixin


class RequestIDMiddleware(MiddlewareMixin):
    """Attach a unique request ID to each request for tracing."""

    def process_request(self, request):
        request.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
