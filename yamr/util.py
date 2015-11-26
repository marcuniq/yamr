import collections
import time


def sframe_to_list(sframe, nb_elem=None):
    if nb_elem:
        nb_elem = min(nb_elem, sframe.shape[0])
    else:
        nb_elem = sframe.shape[0]

    l = []
    for i in xrange(nb_elem):
        l += [sframe[i]]

    return l


def map_dict_value_as_array(x):
    if x:
        for k, v in x.iteritems():
            x[k] = [v]
        return x


def merge_two_dicts(x, y):
    if x:
        z = x.copy()
    if not x:
        z = {}

    if y:
        for k, v in y.iteritems():
            if k not in z:
                z[k] = []
            if type(v) != list:
                z[k] += [v]
            else:
                z[k] += v

    return z


def convert_unicode_to_str(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_unicode_to_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_unicode_to_str, data))
    else:
        return data


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap
