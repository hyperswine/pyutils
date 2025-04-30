from inspect import signature


def curry(func):
  sig = signature(func)
  total_params = len(sig.parameters)

  def _curried(*args):
    if len(args) >= total_params:
      return func(*args)
    return lambda x: _curried(*args, x)

  return _curried
