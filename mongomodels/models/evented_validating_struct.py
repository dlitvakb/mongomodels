from event_handler import EventListener, EventThrower
from validating_struct import ValidatingStruct


class EventedValidatingStruct(ValidatingStruct, EventListener, EventThrower):
    def __init__(self, **kwargs):
        ValidatingStruct.__init__(self, **kwargs)
        EventListener.__init__(self)
        EventThrower.__init__(self)
