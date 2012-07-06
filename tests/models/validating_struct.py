from unittest import TestCase
from mongomodels.db import DocumentDatabase
from mongomodels.models import ValidatingStruct
from mongomodels.models.exceptions import ValidationException

class BaseValidatingModel(ValidatingStruct):
    __DOCUMENT_DB__ = DocumentDatabase('localhost', 'test')


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
