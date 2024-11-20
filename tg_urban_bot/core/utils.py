COMMAND_LIST = dict()


def description_meta(name: str, desc: str):

    def decorator(func):
        COMMAND_LIST[name] = desc
        return func

    return decorator
