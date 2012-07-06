from unittest import TestCase

from mongomodels.struct_data import is_struct, Struct

class MyStruct(Struct):
    pass

class StructTest(TestCase):
    def test_a_struct_is_a_struct_when_it_is_a_struct_or_a_child(self):
        self.assertFalse(is_struct(object()))
        self.assertTrue(is_struct(Struct()))
        self.assertTrue(is_struct(MyStruct()))

    def test_a_struct_can_be_accessed_as_a_dict_or_as_an_object(self):
        a_struct = Struct(foo='bar')

        self.assertEqual('bar', a_struct.foo)
        self.assertEqual('bar', a_struct['foo'])

    def test_a_struct_can_be_serialized_as_a_dict(self):
        a_struct = Struct(foo='bar')

        self.assertEqual({'foo':'bar'}, a_struct.to_struct())

    def test_a_struct_can_serialize_nested_structs(self):
        another_struct = Struct(baz='blah')
        a_struct = Struct(foo='bar', something=another_struct)

        self.assertEqual(
          {'foo':'bar', 'something': {'baz':'blah'}},
          a_struct.to_struct()
        )
