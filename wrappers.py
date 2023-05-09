import logging
from typing import Optional
from functools import wraps
from traceback import format_exc

from azure.functions import HttpResponse

from errors import _BaseHttpException


# ---------------------------------- HTTP Handler ---------------------------------------

def http(func=None, method: str = "GET", template: Optional[str] = None):
    
    def decorator(func):
        
        @error_boundary
        @wraps(func)
        def wrapper(*args, **kwargs) -> HttpResponse:
            if "req" in kwargs:
                logging.info(
                    f"Received {method} request for {kwargs['req'].url} "
                    f"with params {kwargs['req'].params}"
                )
            
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
            logging.error(f"{e.__class__.__name__}: {e.message}\n{format_exc()}")
            return HttpResponse(e.message, status_code=e.__class__.code)

        except:
            logging.critical("*** Unhandled Exception:\n" + format_exc())
            return HttpResponse(
                "Something went wrong; see logs for details.",
                status_code=500
            )
            
    return wrapper
