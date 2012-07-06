from unittest import TestCase

from mongomodels.models import SelfSavingStruct
from mongomodels.db.exceptions import NoDocumentDatabaseException
from mongomodels.db import DocumentDatabase

class Model(SelfSavingStruct):
    __DOCUMENT_DB__ = DocumentDatabase('localhost', 'test')

class SelfSavingStructTest(TestCase):
    def test_when_no_database_is_assigned_should_raise_exception_on_action(self):
        document = SelfSavingStruct()
        self.assertRaises(NoDocumentDatabaseException, document.save)

    def test_when_database_is_assigned_should_save_properly(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(model.to_struct(), Model.get().to_struct())

    def tearDown(self):
        Model.teardown()
