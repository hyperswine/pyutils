from functools import wraps


def aspect(fn):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      return fn(func, *args, **kwargs)
    return wrapper
  return decorator


class Aspect:
  """
  Aspect(func) wraps a decorator-like function and allows composition using the | operator.
  You can define aspects like:

      @Aspect
      def log(func): ...

      @Aspect
      def auth(func): ...

  Then apply them like:
      core_logic = log | auth | core_logic
  """
  def __init__(self, func):
    self.func = func

  def __or__(self, other):
    if callable(other):
      return self.func(other)
    raise TypeError(f"Cannot compose Aspect with non-callable: {type(other)}")

  def __call__(self, func):
    return self.func(func)
