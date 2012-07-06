from unittest import TestCase

from mongomodels.util import CamelCaseConverter

class CamelCaseConverterTest(TestCase):
    def assertConvertion(self, expectee, to_convert):
        self.assertEqual(expectee, CamelCaseConverter(to_convert).convert())

    def test_capitalized_to_lower(self):
        self.assertConvertion('hello', 'Hello')

    def test_one_lower_word_stays_the_same(self):
        self.assertConvertion('hello', 'hello')

    def test_camel_to_snake_if_no_consecutive_capitals(self):
        self.assertConvertion('hello_world', 'HelloWorld')

    def test_camel_to_snake_with_consecutive_capitals(self):
        self.assertConvertion('hello_world', 'HELLOWorld')
