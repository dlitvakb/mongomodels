from unittest import TestCase

from mongomodels.db import DocumentDatabaseBackend, MemoryDatabaseBackend, CouchDatabaseBackend, MongoDatabaseBackend
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


class GenericBackendTest(object):
    def test_set_doc(self):
        self.db.set_doc('foo', {'_id':'1', 'bar':'baz'})
        self._assert_contents('foo', [{'_id':'1', 'bar':'baz'}])

    def test_get_doc(self):
        self.db.set_doc('foo', {'_id':'1', 'bar':'baz'})

        self.assertEquals({'_id':'1','bar':'baz'}, self.db.get_doc('foo', {}))
        self.assertEquals({'_id':'1','bar':'baz'}, self.db.get_doc('foo', {'_id':'1'}))

    def test_find_docs(self):
        self.db.set_doc('foo', {'_id':'1', 'bar':'baz'})

        self.assertEquals({'_id':'1','bar':'baz'}, self.db.find_docs('foo', {}).next())
        self.assertEquals({'_id':'1','bar':'baz'}, self.db.find_docs('foo', {'_id':'1'}).next())


class MongoDatabaseBackendTest(GenericBackendTest, TestCase):
    def setUp(self):
        self.db = MongoDatabaseBackend('localhost', 'test')

    def _assert_contents(self, coll_name, contents):
        collection = self.db.get_collection(coll_name)
        cursor = collection.find()
        self.assertEquals(1, cursor.count())
        self.assertEquals(contents[0], cursor.next())

    def tearDown(self):
        self.db.teardown('test')


class MemoryDatabaseBackendTest(GenericBackendTest, TestCase):
    def setUp(self):
        self.db = MemoryDatabaseBackend()

    def _assert_contents(self, coll_name, contents):
        self.assertEquals({coll_name:contents}, self.db.get_contents())

    def tearDown(self):
        self.db.clean()


class CouchDatabaseBackendTest(GenericBackendTest, TestCase):
    def setUp(self):
        self.db = CouchDatabaseBackend()

    def _assert_contents(self, coll_name, contents):
        collection = self.db.get_collection(coll_name)
        documents = collection.get_all()
        self.assertEquals(contents[0], collection.clean_document(documents.rows[0]))

    def assertEquals(self, expected, expectee, message=None):
        if isinstance(expectee, dict):
            if '_rev' in expectee:
                expectee.pop('_rev')
        super(CouchDatabaseBackendTest, self).assertEquals(expected, expectee, message)

    def tearDown(self):
        self.db.teardown('foo')
