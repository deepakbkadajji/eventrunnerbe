import logging

logger = logging.getLogger(__name__)


class WebRequestLoggingMiddleware:
    """Log unhandled web view exceptions and 5xx responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception:
            logger.exception(
                "Unhandled web view exception",
                extra={
                    "path": request.path,
                    "method": request.method,
                    "user": _request_username(request),
                },
            )
            raise

        if response.status_code >= 500:
            logger.error(
                "Web response server error status=%s",
                response.status_code,
                extra={
                    "path": request.path,
                    "method": request.method,
                    "user": _request_username(request),
                },
            )
        return response


def _request_username(request):
    user = getattr(request, "user", None)
    if user is not None and getattr(user, "is_authenticated", False):
        return user.username
    return None
