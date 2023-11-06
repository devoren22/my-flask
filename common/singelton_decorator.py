
def singleton(cls):
    instances = {}
    def wrapped_class(*args, **kwargs):


        if cls not in instances:
            instances[cls] = cls()

        return instances[cls]

    return wrapped_class