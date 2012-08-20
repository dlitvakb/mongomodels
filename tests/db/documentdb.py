from unittest import TestCase

from mongomodels.db import NotImplementedDocumentDatabase, MemoryDatabaseBackend
from mongomodels.db.exceptions import NoDocumentDatabaseException


class DocumentDatabaseTest(TestCase):
    def test_not_implemented_will_raise_exception_on_any_call(self):
        not_implemented_db = NotImplementedDocumentDatabase()

        try:
            not_implemented_db.fruta()
            self.fail()
        except NoDocumentDatabaseException:
            pass

        try:
            not_implemented_db.teardown('test')
            self.fail()
        except NoDocumentDatabaseException:
            pass


class MemoryDatabaseBackendTest(TestCase):
    def setUp(self):
        self.db = MemoryDatabaseBackend()

    def test_set_doc(self):
        self.db.set_doc('foo', {'_id':'1', 'bar':'baz'})

        self.assertEquals({'foo':[{'_id':'1','bar':'baz'}]}, self.db.get_contents())

    def tearDown(self):
        self.db.teardown()

