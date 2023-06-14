from flask_security import current_user
import functools

def auth_required_socket(func=None):
    if func is None:
        return functools.partial(auth_required_socket)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            func(*args, **kwargs)
        else:
            return False
    return wrapper