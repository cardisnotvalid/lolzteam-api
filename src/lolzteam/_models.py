class BaseModel:
    __slots__ = ()

    def __init__(self, **kwargs):
        for slot in self.__slots__:
            if slot in kwargs:
                setattr(self, slot, kwargs[slot])
            else:
                setattr(self, slot, None)

    def __repr__(self):
        slots = []
        for key in self.__slots__:
            value = getattr(self, key)
            slot = repr("%s=%s" % (key, value))
            slots.append(slot)
        return "%s(%s)" % (self.__class__.__name__, ", ".join(slots))
