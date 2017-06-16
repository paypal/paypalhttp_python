class Injector(object):
    def __call__(self, request):
        raise NotImplementedError("Must be overridden by subclass")
