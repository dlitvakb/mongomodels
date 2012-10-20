from exceptions import ValidationException, NotFoundException
from self_saving_struct import SelfSavingStruct


class ValidatingStruct(SelfSavingStruct):
    __NULLABLES__ = []

    def __init__(self, **kwargs):
        super(ValidatingStruct, self).__init__(**kwargs)
        self.update(kwargs)

    def pre_save(self):
        self.validate()

    def validate(self):
        pass

    def _field_can_be_null(self, field_name):
        return (getattr(self, field_name, None) is None and 
                field_name in self.__NULLABLES__)

    def validate_field(self, field_name, validation_fn, nullable=True, exc_message='', *args):
        if self._field_can_be_null(field_name) and nullable:
            return
        if not validation_fn(self.__dict__.get(field_name, None), *args):
            raise ValidationException(exc_message)

    def validate_not_empty(self, field_name):
        self.validate_field(field_name, bool, nullable=False,
                            exc_message='%s is required' % (field_name,))

    def validate_existance(self, relationship_field, object_cls, nullable=False):
        if self._field_can_be_null(relationship_field) and nullable:
            return
        try:
            object_cls.get(_id=self[relationship_field])
        except NotFoundException:
            if nullable:
                return
            raise ValidationException('%s does not exist for id: %s' % (
                                        object_cls.__name__,
                                        self[relationship_field])
                                     )
        except KeyError:
            if nullable:
                return
            raise ValidationException('%s does not have the field %s' % (
                                        object_cls.__name__, relationship_field))

    def validate_in(self, field_name, valid_values):
        if self._field_can_be_null(field_name):
            return
        if self[field_name] not in valid_values:
            raise ValidationException(
            '''
            %s value for the %s field is not included in the allowed values (%s)
            ''' % (
              self[field_name], field_name, valid_values))

    def validate_type(self, field_name, expected_type):
        if self._field_can_be_null(field_name):
            return
        if not isinstance(self[field_name], expected_type):
            raise ValidationException('%s is not an instance of %s' % (
              field_name, str(expected_type)))

    def validate_unique(self):
        if self.__PRIMARY_KEY__:
            try:
                objects = self.__class__.all(**{self.__PRIMARY_KEY__ : self[self.__PRIMARY_KEY__]})
                if len(objects) == 1:
                    raise ValidationException("%s is not unique" % (
                                               self.__class__.__name__
                                              ))
            except NotFoundException:
                pass


