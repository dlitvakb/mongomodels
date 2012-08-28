from unittest import TestCase

from mongomodels.db import DocumentDatabaseBackend, MemoryDatabaseBackend
from mongomodels.db.exceptions import NoDocumentDatabaseException


class DocumentDatabaseTest(TestCase):
    def test_not_implemented_will_raise_exception_on_any_call(self):
        not_implemented_db = DocumentDatabaseBackend()

        try:
            not_implemented_db.get_doc('foo', {})
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

    def test_get_doc(self):
        self.db.set_doc('foo', {'_id':'1', 'bar':'baz'})

        self.assertEquals({'_id':'1','bar':'baz'}, self.db.get_doc('foo', {}))
        self.assertEquals({'_id':'1','bar':'baz'}, self.db.get_doc('foo', {'_id':'1'}))

    def test_find_docs(self):
        self.db.set_doc('foo', {'_id':'1', 'bar':'baz'})

        self.assertEquals({'_id':'1','bar':'baz'}, self.db.find_docs('foo', {}).next())
        self.assertEquals({'_id':'1','bar':'baz'}, self.db.find_docs('foo', {'_id':'1'}).next())

    def tearDown(self):
        self.db.clean()

