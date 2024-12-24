def __enter__(self):
    self.orig = bottle.request.environ
    bottle.request.environ = self.environ
    for k,v in self.extras.items():
        if hasattr(bottle.request, k):
        self.extra_orig[k] = getattr(bottle.request, k)
        setattr(bottle.request, k, v)
    setattr(bottle.BaseRequest, 'app', True)

def __exit__(self,a,b,c):
    bottle.request.environ = self.orig
    for k,v in self.extras.items():
        if k in self.extra_orig:
        setattr(bottle.request, k, self.extra_orig[k])
        else:
        try:
            delattr(bottle.request, k)
        except AttributeError:
            pass
    setattr(bottle.BaseRequest, 'app', self.orig_app_reader)