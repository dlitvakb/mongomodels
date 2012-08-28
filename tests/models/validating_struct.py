from unittest import TestCase
from mongomodels.db import MemoryDatabaseBackend
from mongomodels.models import ValidatingStruct
from mongomodels.models.exceptions import ValidationException

class BaseValidatingModel(ValidatingStruct):
    __DOCUMENT_DB__ = MemoryDatabaseBackend()


class ValidatesNotEmptyFieldStruct(BaseValidatingModel):
    def validate(self):
        self.validate_not_empty('foo')


class CustomValidatedStruct(BaseValidatingModel):
    def validate(self):
        self.validate_field('foo', self.validate_foo)

    def validate_foo(self, value):
        return value == 'baz'


class ValidatesExistantRelationshipStruct(BaseValidatingModel):
    def __init__(self, nullable=False, **kwargs):
        self._nullable = nullable
        super(ValidatesExistantRelationshipStruct, self).__init__(**kwargs)

    def validate(self):
        self.validate_existance('father', ValidatesExistantRelationshipStruct, nullable=self._nullable)


class ValueInCollectionValidatingStruct(BaseValidatingModel):
    def validate(self):
        self.validate_in('foo', ['baz', 'boo'])


class TypeValidatingStruct(BaseValidatingModel):
    def validate(self):
        self.validate_type('meaning_of_life', int)


class WithoutNullableFieldStruct(BaseValidatingModel):
    def validate(self):
        self.validate_type('foo', int)


class WithNullableFieldStruct(WithoutNullableFieldStruct):
    __NULLABLES__ = ['foo']


class ValidatingStructTest(TestCase):
    def test_validates_not_empty(self):
        model_1 = ValidatesNotEmptyFieldStruct()

        self.assertRaises(ValidationException, model_1.save)

        model_1['foo'] = 'bar'

        model_1.save()

    def test_validates_existant_relation(self):
        father = ValidatesExistantRelationshipStruct(nullable=True, foo='bar')
        father.save()

        child = ValidatesExistantRelationshipStruct(father=father['_id'])
        child.save()

        fatherless_model = ValidatesExistantRelationshipStruct(bar='baz')
        self.assertRaises(ValidationException, fatherless_model.save)

    def test_custom_field_validation(self):
        model = CustomValidatedStruct(foo='bar')
        self.assertRaises(ValidationException, model.save)

        another_model = CustomValidatedStruct(foo='baz')
        another_model.save()

    def test_validates_value_in_collection(self):
        model = ValueInCollectionValidatingStruct(foo='bar')
        self.assertRaises(ValidationException, model.save)

        another_model = ValueInCollectionValidatingStruct(foo='baz')
        another_model.save()

    def test_validates_type(self):
        model = TypeValidatingStruct(meaning_of_life='bar')
        self.assertRaises(ValidationException, model.save)

        another_model = TypeValidatingStruct(meaning_of_life=42)
        another_model.save()

    def test_check_nullables(self):
        model = WithoutNullableFieldStruct(foo=None)
        self.assertRaises(ValidationException, model.save)

        another_model = WithNullableFieldStruct(foo=None)
        another_model.save()

