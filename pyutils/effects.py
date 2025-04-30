class Effect: pass

class LogEffect(Effect):
    def __init__(self, message): self.message = message

def handle_effects(handler_builder):
    def runner(gen):
        registry = {}

        def match(effect_type, handler_func):
            registry[effect_type] = handler_func

        # Let user register handlers
        handler_builder(match)

        result = None
        try:
            while True:
                effect = gen.send(result)
                effect_type = type(effect)
                if effect_type in registry:
                    result = registry[effect_type](effect)
                else:
                    raise ValueError(f"Unhandled effect: {effect}")
        except StopIteration as e:
            return e.value

    return runner
