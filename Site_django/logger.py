import time
import logging
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from decouple import config
from Home.models import LogEntry, Log

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    MAX_BODY_LENGTH = 500
    MAX_RESPONSE_LENGTH = 1000

    def process_request(self, request):
        request.start_time = time.monotonic()
        
        # Armazena o corpo original antes de qualquer processamento
        try:
            request._body_backup = request.body
        except Exception as e:
            logger.warning(f"Error reading request body: {str(e)}")
            request._body_backup = b''

        request.log_data = {
            'ip_address': self._get_client_ip(request),
            'user': request.user if request.user.is_authenticated else None,
            'method': request.method,
            'path': request.path,
            'query_params': dict(request.GET),
            'body': self._safe_body_content(request)
        }
    def process_response(self, request, response):
        if not hasattr(request, 'start_time') or not hasattr(request, 'log_data'):
            return response

        duration = time.monotonic() - request.start_time
        self._complete_log_data(request, response, duration)
        
        try:
            self._create_log_entries(request, response)
        except Exception as e:
            logger.exception("Failed to create log entries")

        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', '0.0.0.0')

    def _complete_log_data(self, request, response, duration):
        request.log_data.update({
            'status_code': response.status_code,
            'duration': duration,
            'server': config('DJ_SERVER', default='api'),
            'version': config('DJ_VERSION', default='dev'),
            'timestamp': timezone.now(),
            'response_content': self._safe_response_content(response),
        })

    def _safe_response_content(self, response):
        if response.streaming:
            return '[Streaming Content]'
        
        try:
            content = response.content.decode('utf-8', errors='replace')
            return content[:self.MAX_RESPONSE_LENGTH]
        except (UnicodeDecodeError, AttributeError):
            return '[Binary Content]'

    def _create_log_entries(self, request, response):
        log_entry = None
        
        if request.log_data['method'] not in self.SAFE_METHODS:
            log_entry = self._create_action_log(request)

        self._create_request_log(request, log_entry)

    def _create_action_log(self, request):
        try:
            path_parts = request.path.strip('/').split('/')
            app = path_parts[0] if len(path_parts) > 0 else 'unknown'
            resource = path_parts[1] if len(path_parts) > 1 else 'unknown'
            item_id = path_parts[2] if len(path_parts) > 2 else ''

            body_content = self._safe_body_content(request)
            
            return Log.objects.create(
                user_name=request.log_data['user'].username if request.log_data['user'] else 'None',
                action=request.log_data['method'],
                text=body_content,
                app=app,
                resource=resource,
                status=request.log_data['status_code']
            )
        except Exception as e:
            logger.error(f"Action log creation failed: {str(e)}")
            return None

    def _safe_body_content(self, request):
        """Captura o conteúdo do corpo de forma segura"""
        try:
            # Usa o backup criado antes de qualquer leitura
            body = request._body_backup
            
            # Verifica se é binário (ex: upload de arquivo)
            if isinstance(body, bytes):
                return body[:self.MAX_BODY_LENGTH].decode('utf-8', errors='replace')
            
            return str(body)[:self.MAX_BODY_LENGTH]
        except Exception as e:
            logger.error(f"Error processing body content: {str(e)}")
            return '[Unreadable Content]'

    def _create_request_log(self, request, action_log):
        try:
            LogEntry.objects.create(
                timestamp=request.log_data['timestamp'],
                ip_address=request.log_data['ip_address'],
                username=request.log_data['user'].username if request.log_data['user'] else None,
                endpoint=request.log_data['path'],
                method=request.log_data['method'],
                status_code=request.log_data['status_code'],
                response_time=request.log_data['duration'],
                server=request.log_data['server'],
                version=request.log_data['version'],
                response=request.log_data['response_content'],
                log_api=action_log,
                query_params=request.log_data['query_params'],
            )
        except Exception as e:
            logger.error(f"Request log creation failed: {str(e)}")