from ..struct_data import is_struct
from exceptions import NoDocumentDatabaseException
import pymongo

class DocumentDatabaseBackend(object):
    def get_collection(self, coll_name):
        pass

    def set_doc(self, coll_name, doc):
        collection = self._get_collection(coll_name)
        self._serialize(doc)
        collection.save(doc)

    def get_doc(self, coll_name, fdoc, struct_class = None):
        pass

    def find_docs(self, coll_name, fdoc = None, struct_class = None):
        pass

    def delete_doc(self, coll_name, fdoc, struct_class = None):
        pass

    def teardown(self, coll_name):
        pass

    def _serialize(self, document):
        for k, v in document.items():
            if k != '_id' and is_struct(v):
                document[k] = v.to_struct()
            elif k == '$set' and isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 != '_id' and is_struct(v2):
                        v[k2] = v2.to_struct()

    def _get_collection(self, collection_name):
        pass

class MemoryDatabase(dict):
    pass


class MemoryCollection(list):
    def __init__(self, db, name):
        super(MemoryCollection, self).__init__()
        self.__DATABASE__ = db
        self.__NAME__ = name

    def save(self, doc):
        to_update = None

        for index, document in enumerate(self):
            if document['_id'] == doc['_id']:
                to_update = index
                break

        if to_update:
            self.pop(to_update)

        self.append(doc)

        self.__DATABASE__[self.__NAME__] = self


class MemoryDatabaseBackend(DocumentDatabaseBackend):
    def __init__(self):
        super(MemoryDatabaseBackend, self).__init__()
        self.__CONTENT__ = MemoryDatabase()

    def _get_collection(self, collection_name):
        return self.__CONTENT__.get(collection_name, MemoryCollection(self.__CONTENT__, collection_name))

    def get_contents(self):
        return self.__CONTENT__

    def teardown(self):
        self.__CONTENT__ = MemoryDatabase()


class MongoDatabaseBackend(DocumentDatabaseBackend):
    def __init__(self, mongo_uri, mongo_name):
        self.db = pymongo.Connection(mongo_uri)[mongo_name]

    def get_collection(self, coll_name):
        return self.db[coll_name]

    def _get_collection(self, collection_name):
        return self.db[collection_name]

    def get_doc(self, coll_name, fdoc, struct_class = None):
        collection = self.db[coll_name]
        doc = collection.find_one(fdoc)
        if doc and struct_class:
            for k, v in doc.items():
                if k != '_id':
                    o = struct_class()
                    doc[k] = o.from_struct(v)
        return doc

    def find_docs(self, coll_name, fdoc = None, struct_class = None):
        collection = self.db[coll_name]
        for doc in collection.find(fdoc):
            if doc and struct_class:
                for k, v in doc.items():
                    if k != '_id':
                        o = struct_class()
                        doc[k] = o.from_struct(v)
            yield doc

    def delete_doc(self, coll_name, fdoc, struct_class = None):
        collection = self.db[coll_name]
        doc = collection.remove(fdoc)
        if doc and struct_class:
            for k, v in doc.items():
                if k != '_id':
                    o = struct_class()
                    doc[k] = o.from_struct(v)
        return doc

    def teardown(self, coll_name):
        return bool(self.db[coll_name].remove())


class NotImplementedDocumentDatabase(DocumentDatabaseBackend):
    def __init__(self):
        pass

    def __getattribute__(self, name):
        raise NoDocumentDatabaseException("A document database should be set for this model")

