from unittest import TestCase
import json

from mongomodels.models import SelfSavingStruct
from mongomodels.models.exceptions import NotFoundException
from mongomodels.db.exceptions import NoDocumentDatabaseException
from mongomodels.db import MemoryDatabaseBackend

class Model(SelfSavingStruct):
    __DOCUMENT_DB__ = MemoryDatabaseBackend()


class OtherModel(Model):
    __DOCUMENT_NAME__ = 'model'


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

    def test_two_models_can_point_to_the_same_collections(self):
        model_1 = Model(foo='bar')
        model_1.save()

        self.assertEqual(1, len(Model.all()))

        model_2 = OtherModel(bar='baz')
        model_2.save()

        self.assertEqual(2, len(Model.all()))
        self.assertEqual(2, len(OtherModel.all()))

    def test_a_model_can_have_a_list_as_a_field_value(self):
        model = Model(foo=['blah', 'bleh'])
        model.save()

        self.assertTrue(isinstance(Model.get().foo, list))

    def test_a_model_has_json_property_that_behaves_like_to_struct(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(model.json, model.to_struct())

    def test_a_model_has_json_string_property(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(model.json_string, json.dumps(model.to_struct()))

    def test_all_json(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(Model.all_json(), [o.json for o in Model.all()])

    def test_all_json_string(self):
        model = Model(foo='bar')
        model.save()

        self.assertEqual(Model.all_json_string(), json.dumps([o.json for o in Model.all()]))

    def tearDown(self):
        Model.teardown()
