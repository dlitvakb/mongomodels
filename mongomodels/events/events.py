class EventListener(object):
    def __init__(self, registered_signals=None):
        if registered_signals is None:
            registered_signals = {}
        self.__REGISTERED_SIGNALS__ = registered_signals

    def on(self, signal_name, callback):
        self.__REGISTERED_SIGNALS__[signal_name] = callback

    def respond(self, signal_name, *args, **kwargs):
        try:
            self.__REGISTERED_SIGNALS__[signal_name](*args, **kwargs)
        except KeyError:
            pass # explicitly silenced

class EventThrower(object):
    def __init__(self, listeners=None):
        if not listeners:
            listeners = []
        self.__LISTENERS__ = listeners

    def emit(self, signal_name, *args, **kwargs):
        for listener in self.__LISTENERS__:
            listener.respond(signal_name, *args, **kwargs)

    def add_listener(self, listener):
        self.__LISTENERS__.append(listener)
