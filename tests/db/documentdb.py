from unittest import TestCase

from mongomodels.db import NotImplementedDocumentDatabase
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
