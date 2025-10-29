from django.utils.deprecation import MiddlewareMixin
from apps.shared.models import Cliente
import threading

_thread_locals = threading.local()

def get_current_db_name():
    return getattr(_thread_locals, 'db_name', 'default')

class ClienteDBMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]
        subdominio = host.split('.')[0]
        try:
            cliente = Cliente.objects.get(dominio=subdominio)
            _thread_locals.db_name = cliente.banco
        except Cliente.DoesNotExist:
            _thread_locals.db_name = 'default'
