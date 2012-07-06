from copy import deepcopy

#This class is used as a base class for all objects that are persisted into MonngoDB
#it allows the object to be converted to and from a struct (e.g. dictionary, tuples, etc...)
#To create a persistent object that will be stored as a struct
#- Create a subclass of Struct
#- add a global variable 'classes' set it to a dictionary mapping name of attribute to class objec
#  for nested objects to be converted into a struct
#  - this will handle conversion of other objects (if the attribute is a collection then contents are
#    are assumed to be objects)
# for more details see the object bellow
# All persistent object should be able to be initialized with out any parameters

def is_struct(o):
    for c in o.__class__.__bases__:
        if c.__name__ == 'Struct':
            return True
    return o.__class__.__name__ == 'Struct'

def struct_doc(o):
    if is_struct(o):
        return deepcopy(o).to_struct()
    else:
        return o

class Struct(object):
    _match_all = '__ALL__'
    classes = {}

    def to_struct(self):
        d = dict(self.__dict__)
        if self.classes.has_key(self._match_all):
            keys = d.keys()
        else:
            keys = self.classes.keys()
            to_pop = []
            for k, v in d.iteritems():
                if k.startswith('__'):
                    to_pop.append(k)
                    continue
                if is_struct(v):
                    keys.append(k)
            for popping in to_pop:
                d.pop(popping)
        for name in keys:
            if d.get(name, None) != None:
                if d[name].__class__.__name__ == 'list':
                    d[name] = [o.to_struct() for o in d[name]]
                else:
                    d[name] = d[name].to_struct()
        return d


    def from_struct(self, d):
        self.__dict__.update(d)
        if self.classes.has_key(self._match_all):
            cls = self.classes[self._match_all]
            for name in self.__dict__.keys():
                a = getattr(self, name, None)
                if a != None:
                    if a.__class__.__name__  == 'list':
                        o = a.__class__()
                        for i in a:
                            no = cls()
                            no.from_struct(i)
                            o.append(no)
                    else:
                        o = cls()
                        o.from_struct(a)
                    setattr(self, name, o)
        else:
            for name, cls in self.classes.items():
                a = getattr(self, name, None)
                if a != None:
                    if a.__class__.__name__  == 'list':
                        o = a.__class__()
                        for i in a:
                            no = cls()
                            no.from_struct(i)
                            o.append(no)
                    else:
                        o = cls()
                        o.from_struct(a)
                    setattr(self, name, o)
        return self

    # make it look like a dict
    def __init__(self, *args, **kw):
        self.__dict__.__init__(*args, **kw)

    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __delitem__(self, key):
        del self.__dict__[key]

    def __containes__(self, key):
        return self.__dict__.has_key(key)

    def __iter__(self):
        return self.__dict__.iterkeys()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def has_key(self, key):
        return self.__dict__.has_key(key)

    def setdefault(self, key, default):
        return self.__dict__.setdefault(key, default)

    def update(self, dict):
        return self.__dict__.update(dict)

    def iteritems(self):
        return self.__dict__.iteritems()

    def iterkeys(self):
        return self.__dict__.iterkeys()

    def keys(self):
        return self.__dict__.keys()

    def itervalues(self):
        return self.__dict__.itervalues()
