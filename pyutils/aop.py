from functools import wraps


def aspect(fn):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      return fn(func, *args, **kwargs)
    return wrapper
  return decorator
