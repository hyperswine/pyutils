from pyutils.aop import Aspect, aspectf


@aspectf
def log(func, *args, **kwargs):
  print(f"[LOG] Calling {func.__name__} with {args} {kwargs}")
  result = func(*args, **kwargs)
  print(f"[LOG] {func.__name__} returned {result}")
  return result


@aspectf
def auth(func, *args, **kwargs):
  print("[AUTH] Checking user permissions...")
  return func(*args, **kwargs)


# Define your core logic

def core_logic(data):
  print(f"Processing {data}")
  return data * 2


# Compose aspects using |
core_logic = log | auth | core_logic


def main():
  print("Hello from pyutils!")
  result = core_logic(21)
  print("Final result:", result)


if __name__ == "__main__":
  main()
