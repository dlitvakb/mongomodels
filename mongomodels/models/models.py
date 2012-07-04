from ..struct_data import Struct
from ..db import NotImplementedDocumentDatabase
from ..util import CamelCaseConverter
from hashlib import md5
from exceptions import ValidationException, NotFoundException


class SelfSavingStruct(Struct):

    __DOCUMENT_DB__ = NotImplementedDocumentDatabase()

    def save(self):
        if not self.verify_id():
            self.create_id()
        self.pre_save()
        saved = bool(self.__DOCUMENT_DB__.set_doc(
                                          self.__DOCUMENT_NAME__,
                                          self.to_struct()
                                        ))
        self.post_save(saved)
        return self, saved

    def delete(self):
        self.pre_delete()
        deleted = bool(self.__DOCUMENT_DB__.delete_doc(
                                            self.__DOCUMENT_NAME__,
                                            self.to_struct(),
                                            self.__class__
                                          ))
        self.post_delete(deleted)
        return self, deleted

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
        self['_id'] = md5(str(sum(
                       hash(k) + hash (v) for k, v in self.__dict__.iteritems()
                      ))).hexdigest()

    @classmethod
    def _get_document_name(cls):
        doc_name = getattr(cls, '__DOCUMENT_NAME__', None)
        if doc_name is None:
            return CamelCaseConverter(cls.__name__).convert()

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
        doc = cls.__DOCUMENT_DB__.find_docs(cls.__DOCUMENT_NAME__, params)
        if doc is not None:
            items = []
            for item in doc:
                items.append(cls(**item))
            return items
        cls._not_found_exception(params)

    @classmethod
    def get(cls, **params):
        item = cls.__DOCUMENT_DB__.get_doc(cls.__DOCUMENT_NAME__, params)
        if item is not None:
            return cls(**item)
        cls._not_found_exception(params)

    @classmethod
    def teardown(cls):
        return cls.__DOCUMENT_DB__.teardown(cls.__DOCUMENT_NAME__)


class ValidatingStruct(SelfSavingStruct):

    def __init__(self, **kwargs):
        super(ValidatingStruct, self).__init__(**kwargs)
        self.update(kwargs)

    def pre_save(self):
        self.validate()

    def validate(self):
        pass

    def validate_field(self, field_name, validation_fn, exc_message=''):
        if not validation_fn(self.__dict__.get(field_name, None)):
            raise ValidationException(exc_message)

    def validate_not_empty(self, field):
        self.validate_field(field, bool, '%s is required' % (field,))

    def validate_unique(self):
        objects = self.__class__.all(_id=self['_id'])
        if objects:
            if objects[0]['_id'] == self['_id']:
                raise ValidationException('%s already exists' % (
                                           self.__class__.__name__,))

    def validate_existance(self, relationship_field, object_cls):
        try:
            object_cls.get(_id=self[relationship_field])
        except NotFoundException:
            raise ValidationException('%s does not exist for id: %s' % (
                                        object_cls.__name__, self[relationship_field]))

