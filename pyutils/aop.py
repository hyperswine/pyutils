from functools import wraps


def aspect(fn):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      return fn(func, *args, **kwargs)
    return wrapper
  return decorator


def aspectf(fn):
  """
  Decorator that converts a plain decorator function into an `Aspect`
  instance, so you can write:

      @aspectf
      def log(func): ...

  and `log` will be an `Aspect` that supports `|` composition.
  """
  return Aspect(fn)


class Aspect:
  def __init__(self, fn):          # fn: decorator
    self.fn = fn

  # combine two aspects → new Aspect
  def __or__(self, other):
    if isinstance(other, Aspect):
      def composed(f):
        return self.fn(other.fn(f))
      return Aspect(composed)
    elif callable(other):        # last step: apply to function
      return self.fn(other)
    else:
      raise TypeError

  # allow plain function | Aspect  (optional)
  def __ror__(self, other):
    if callable(other):
      return self.fn(other)
    else:
      raise TypeError
