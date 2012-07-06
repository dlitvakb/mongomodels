from unittest import TestCase
from mongomodels.events import EventListener, EventThrower


class SomeListener(EventListener):
    def listen_something(self):
        self.foo = 'bar'


class EventedTest(TestCase):
    def test_event_model(self):
        listener = SomeListener()
        listener.on('something', listener.listen_something)

        thrower = EventThrower()
        thrower.add_listener(listener)

        self.assertTrue(getattr(listener, 'foo', None) is None)

        thrower.emit('something')

        self.assertEqual(listener.foo, 'bar')
