from inspect import signature


def curry(func):
  sig = signature(func)
  total_params = len(sig.parameters)

  def _curried(*args):
    if len(args) >= total_params:
      return func(*args)
    return lambda x: _curried(*args, x)

  return _curried


# --- Function composition and piping utilities ---

class Pipe:
  """
  Pipe(f) wraps a function f and allows composition using the | operator.
  You can also apply the function to a value using the >> operator.

  Example:
      def add1(x): return x + 1
      def square(x): return x * x
      def half(x): return x / 2

      pipe = Pipe(add1) | square | half
      result = pipe(3)      # equivalent to half(square(add1(3)))
      result = pipe >> 3    # alternative syntax
  """
  def __init__(self, func):
    self.func = func

  def __call__(self, value):
    return self.func(value)

  def __or__(self, other):
    return Pipe(lambda x: other(self(x)))

  def __rshift__(self, value):
    return self(value)

  def __repr__(self):
    return f"<Pipe {self.func.__name__}>"


def pipe(func):
  """
  Convenience function for creating a Pipe.

  Example:
      def add1(x): return x + 1
      def double(x): return x * 2

      p = pipe(add1) | double
      p(5)  # => 12
  """
  return Pipe(func)
