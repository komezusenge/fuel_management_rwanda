import threading
from .models import AuditLog

_thread_local = threading.local()

EXCLUDED_PATHS = ['/api/schema/', '/api/docs/', '/api/redoc/', '/admin/']
EXCLUDED_METHODS = []


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Skip excluded paths and non-API paths
        path = request.path
        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return response

        if not path.startswith('/api/'):
            return response

        # Only log mutating operations
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            user = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user

            try:
                AuditLog.objects.create(
                    user=user,
                    action=request.method,
                    path=path,
                    method=request.method,
                    status_code=response.status_code,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                )
            except Exception:
                pass  # Never let audit logging break requests

        return response
