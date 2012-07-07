from ..struct_data import is_struct
from exceptions import NoDocumentDatabaseException
import pymongo

class DocumentDatabase(object):
    def __init__(self, mongo_uri, mongo_name):
        self.db = pymongo.Connection(mongo_uri)[mongo_name]

    def get_collection(self, coll_name):
        return self.db[coll_name]

    def set_doc(self, coll_name, doc):
        collection = self.db[coll_name]
        for k, v in doc.items():
            if k != '_id' and is_struct(v):
                doc[k] = v.to_struct()
        collection.save(doc)


    def update_doc(self, coll_name, spec, doc, upsert=True):
        collection = self.db[coll_name]
        for k, v in doc.items():
            if k != '_id' and is_struct(v):
                doc[k] = v.to_struct()
            elif k == '$set' and isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 != '_id' and is_struct(v2):
                        v[k2] = v2.to_struct()
        collection.update(spec, doc, upsert=upsert)

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


class NotImplementedDocumentDatabase(DocumentDatabase):
    def __init__(self):
        pass

    def __getattribute__(self, name):
        raise NoDocumentDatabaseException("A document database should be set for this model")

