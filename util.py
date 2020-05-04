from functools import wraps

def protected(required_grants):
    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
                r = f(*args, **kwargs)
        return r
