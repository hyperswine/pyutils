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
  Decorator that transforms a *plain* `(func, *args, **kwargs)` handler into
  • a standard decorator (via `@aspect` internally), **and**
  • an `Aspect` instance that supports `|` composition.

  Usage:

      @aspectf
      def log(func, *args, **kwargs):
          ...

  After decoration, `log` is an `Aspect`, so you can compose:

      core = log | auth | core
  """
  return Aspect(aspect(fn))


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
