import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    path = getattr(request, 'path', 'unknown') if request else 'unknown'
    method = getattr(request, 'method', 'unknown') if request else 'unknown'
    request_extra = {'path': path, 'method': method}

    if response is not None:
        view = context.get('view')
        view_name = view.__class__.__name__ if view else 'unknown'
        if response.status_code >= 500:
            logger.exception(
                "API error response",
                extra={'view': view_name, 'status_code': response.status_code, **request_extra},
            )
        elif response.status_code >= 400:
            logger.warning(
                "API client error",
                extra={
                    'view': view_name,
                    'status_code': response.status_code,
                    'detail': response.data,
                    **request_extra,
                },
            )
        return response

    view = context.get('view')
    view_name = view.__class__.__name__ if view else 'unknown'
    logger.exception(
        "Unhandled API exception",
        extra={'view': view_name, **request_extra},
    )
    return Response(
        {'detail': 'An unexpected error occurred.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
