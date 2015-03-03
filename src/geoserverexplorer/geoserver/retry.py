from geoserver.catalog import Catalog

def methodDecorator(func):
    def decorator(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception, e:
            if "Errno 10053" in unicode(e):
                result = func(*args, **kwargs)
            else:
                raise e
        return result
    return decorator


class RetryDecorator():
    def __getattribute__(self, attr_name):
        obj = super(Catalog, self).__getattribute__(attr_name)
        if hasattr(obj, '__call__'):
            return methodDecorator(obj)
        return obj

class RetryCatalog(Catalog, RetryDecorator):
    pass

