import json

from ..struct_data import Struct
from ..db import DocumentDatabaseBackend
from ..util import CamelCaseConverter
from exceptions import NotFoundException


class SelfSavingStruct(Struct):

    __DOCUMENT_DB__ = DocumentDatabaseBackend()
    __PRIMARY_KEY__ = None

    @property
    def json(self):
        return self.to_struct()

    @property
    def json_string(self):
        return json.dumps(self.json)

    def save(self):
        is_new = False
        if not self.verify_id():
            self.create_id()
            is_new = True
        self.pre_save()
        self.__DOCUMENT_DB__.set_doc(
                               self.__class__._get_document_name(),
                               self.to_struct()
                             )
        self.post_save(is_new)
        return self, is_new

    def delete(self):
        self.pre_delete()
        if self.verify_id():
            self.__DOCUMENT_DB__.delete_doc(
                                   self.__class__._get_document_name(),
                                   self.to_struct(),
                                   self.__class__
                                 )
        self.post_delete(self.verify_id())
        return self, self.verify_id()

    def pre_save(self):
        pass

    def post_save(self, saved):
        pass

    def pre_delete(self):
        pass

    def post_delete(self, deleted):
        pass

    def verify_id(self):
        return '_id' in self.__dict__

    def create_id(self):
        self['_id'] = str(hash(self))

    def __hash__(self):
        if '_id' in self.__dict__:
            return self._id
        h = 0
        for key, value in self.__dict__.iteritems():
            if key.startswith('_'):
                continue
            elif (isinstance(value, list) or
                  isinstance(value, dict)):
                value = str(value)
            h += hash(key) + hash(value)
        return h

    def __repr__(self):
        if self.__PRIMARY_KEY__ is not None:
            return "<%s - %s: %s>" % (
                     self.__class__.__name__,
                     self.__PRIMARY_KEY__,
                     self[self.__PRIMARY_KEY__]
            )
        return "<%s - ID: %s>" % (
                 self.__class__.__name__,
                 self['_id']
               )

    @classmethod
    def _get_document_name(cls):
        doc_name = getattr(cls, '__DOCUMENT_NAME__', None)
        if doc_name is None:
            return CamelCaseConverter(cls.__name__).convert()
        return doc_name

    @classmethod
    def _not_found_exception(cls, params):
        raise NotFoundException(
          '%s not found for the following parameters %r' % (
                                                             cls.__name__,
                                                             params
                                                           )
        )

    @classmethod
    def all(cls, **params):
        documents = cls.__DOCUMENT_DB__.find_docs(cls._get_document_name(), params)
        documents_as_list = [x for x in documents]
        if not len(documents_as_list):
            cls._not_found_exception(params)
        return [cls(**document) for document in documents_as_list]

    @classmethod
    def all_json(cls, **params):
        return [ d.json for d in cls.all(**params) ]

    @classmethod
    def all_json_string(cls, **params):
        return json.dumps(cls.all_json(**params))

    @classmethod
    def get(cls, **params):
        item = cls.__DOCUMENT_DB__.get_doc(cls._get_document_name(), params)
        if item is not None:
            return cls(**item)
        cls._not_found_exception(params)

    @classmethod
    def teardown(cls):
        return cls.__DOCUMENT_DB__.teardown(cls._get_document_name())

