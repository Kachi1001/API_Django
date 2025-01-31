from django.utils.deprecation import MiddlewareMixin
from Home.models import LogEntry
import time
from decouple import config
from django.utils import timezone


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):

            duration = time.time() - request.start_time
            ip_address = request.META.get('REMOTE_ADDR')
            username = request.user.username if request.user.is_authenticated else None
            endpoint = request.path
            method = request.method
            status_code = response.status_code
            server = config('DJ_SERVER')
            version = config('DJ_VERSION')
            if method != 'HEAD':
                try:
                    LogEntry.objects.using('default').create(
                        timestamp=timezone.now(),
                        ip_address=ip_address or request.META,
                        username=username,
                        endpoint=endpoint,
                        method=method,
                        status_code=status_code,
                        response_time=duration,
                        server=server,
                        version=version,
                    )
                except: pass

        return response