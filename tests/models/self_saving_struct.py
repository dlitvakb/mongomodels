from unittest import TestCase

from mongomodels.models import SelfSavingStruct
from mongomodels.models.exceptions import NotFoundException
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

    def test_all(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(model.to_struct(), Model.all()[0].to_struct())

    def test_when_collection_is_empty_should_raise_an_exception(self):
        self.assertRaises(NotFoundException, Model.get)
        self.assertRaises(NotFoundException, Model.all)

    def test_can_search_for_individual_objects(self):
        model_1 = Model(foo='bar')
        model_1.save()

        model_2 = Model(foo='baz')
        model_2.save()

        self.assertEqual(model_1.to_struct(), Model.get(foo='bar').to_struct())
        self.assertEqual(model_2.to_struct(), Model.get(foo='baz').to_struct())

    def test_can_search_for_multiple_objects(self):
        model_1 = Model(foo='bar')
        model_1.save()

        model_2 = Model(foo='bar', blah='bleh')
        model_2.save()

        models = [document.to_struct() for document in Model.all(foo='bar')]

        self.assertTrue(model_1.to_struct() != model_2.to_struct())

        self.assertTrue(model_1.to_struct() in models)
        self.assertTrue(model_2.to_struct() in models)

    def test_can_delete_a_document(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(model.to_struct(), Model.get().to_struct())

        model.delete()

        self.assertRaises(NotFoundException, Model.get)

    def test_teardown_restarts_the_entire_collection(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(model.to_struct(), Model.get().to_struct())

        Model.teardown()
        self.assertRaises(NotFoundException, Model.get)

    def tearDown(self):
        Model.teardown()
