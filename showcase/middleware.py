import threading
import logging

_thread_locals = threading.local()
logger = logging.getLogger(__name__)

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"Setting user {request.user} in thread local storage")
        _thread_locals.user = request.user
        response = self.get_response(request)
        return response
