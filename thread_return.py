from threading import Thread


class ThreadReturn(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.Verbose = Verbose
        self._target = target
        self._args = args
        if kwargs is None:
            kwargs = {}
        self._kwargs = kwargs
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(sel
        f, *args)
        return self._return
