import sys
import logging
from typing import Optional
from functools import wraps
from traceback import format_exc

from azure.functions import HttpRequest, HttpResponse

from errors import _BaseHttpException


# --------------------------------- Logger config ---------------------------------------

logger = logging.getLogger()
logger.handlers.clear()
handler = logging.StreamHandler(sys.stdout)
_format = '%(asctime)s  -  %(name)s  -  %(levelname)s  -  %(message)s'
handler.setFormatter(logging.Formatter(_format))
logger.setLevel(logging.INFO)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


# ---------------------------------- HTTP Handler ---------------------------------------

def http(func=None, method: str = "GET", template: Optional[str] = None):
    
    def decorator(func):
        
        @wraps(func)
        @error_boundary
        def wrapper(*args, **kwargs) -> HttpResponse:
            req = args[0]
            assert isinstance(req, HttpRequest)
            
            logger.info(f'{method} func triggered: {req.url}')
            
            func_result = func(*args, **kwargs)
            
            if template:
                with open(template) as _file:
                    html = _file.read().format(**func_result)
                return HttpResponse(html, mimetype="text/html")

            return HttpResponse(func_result, status_code=__status(method))
            
        return wrapper
    
    return decorator(func) if func else decorator


def __status(method: str) -> int:
    if method == "POST":
        return 201
    elif method == "DELETE":
        return 204
    return 200


# --------------------------------- Error Handling --------------------------------------

def error_boundary(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except _BaseHttpException as e:
            logger.error(f"{e.__class__.__name__}: {e.message}\n{format_exc()}")
            return HttpResponse(e.message, status_code=e.__class__.code)

        except:
            logger.critical("*** Unhandled Exception:\n" + format_exc())
            return HttpResponse(
                "Something went wrong; see logs for details.",
                status_code=500
            )
            
    return wrapper
