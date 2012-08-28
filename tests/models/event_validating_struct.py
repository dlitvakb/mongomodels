from unittest import TestCase
from mongomodels.models import EventedValidatingStruct
from event_handler.events import EventThrower
from mongomodels.db import MemoryDatabaseBackend


class MyEventedModel(EventedValidatingStruct):
    __DOCUMENT_DB__ = MemoryDatabaseBackend()

    def listen_something(self, *args, **kwargs):
        self.foo = 'bar'


class EventedModelTest(TestCase):
    def test_a_model_can_be_a_listener(self):
        listener = MyEventedModel(baz='bar')

        listener.on('something', listener.listen_something)

        thrower = EventThrower()
        thrower.add_listener(listener)

        self.assertTrue(getattr(listener, 'foo', None) is None)

        thrower.emit('something')

        self.assertEqual(listener.foo, 'bar')

        listener.save()
        self.assertEqual(listener.to_struct(), MyEventedModel.get().to_struct())

    def test_a_model_can_be_a_thrower(self):
        listener = MyEventedModel()

        listener.on('something', listener.listen_something)

        thrower = MyEventedModel(bar='baz')
        thrower.add_listener(listener)

        self.assertTrue(getattr(listener, 'foo', None) is None)

        thrower.emit('something')

        self.assertEqual(listener.foo, 'bar')

        thrower.save()
        self.assertEqual(thrower.to_struct(), MyEventedModel.get().to_struct())

    def tearDown(self):
        MyEventedModel.teardown()

