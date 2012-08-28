# mongomodels

*A simple ODM for MongoDB*

## Installation
`pip install mongomodels`

## Usage
Define your base model to refer to the mongo instance

```python
from mongomodels.db import MongoDatabaseBackend
from mongomodels.models import ValidatingStruct

class BaseModel(ValidatingStruct):
    __DOCUMENT_DB__ = MongoDatabaseBackend('localhost', 'test_database')
```

* For development purposes you can use an *In-Memory* document database

```python
from mongomodels.db import MemoryDatabaseBackend
from mongomodels.models import ValidatingStruct

class BaseModel(ValidatingStruct):
    __DOCUMENT_DB__ = MemoryDatabaseBackend()
```

### Define your models
Each model must have a document name, so that the it refers to the proper
collection on MongoDB. By default it takes the snake_case version of the class.


```python
class MyTestModel(BaseModel): # This would map to __DOCUMENT_NAME__ = 'my_test_model'
    pass
    # Or you could redefine your document name
    # __DOCUMENT_NAME__ = 'test_model'
```

### Create your objects

```python
test_object = MyTestModel(some_attribute='some value')
test_object.save()
```

### Find your objects

```python
MyTestModel.all() # Returns a list with all the objects in the document
MyTestModel.all(some_attribute='some value') # Returns all the objects
                                             # that meet the same attributes

MyTestModel.get() # Returns the first object of the collection
MyTestModel.get(some_attribute='some value') # Returns the first object
                                             # that meets the attributes
```

### Validations

```python
# Let's say we have some Message model that relates to a User and a chat Room

class Message(BaseModel): # Our previously defined BaseModel

    def validate(self):
        self.validate_not_empty('message')
        self.validate_not_empty('user_id')
        self.validate_not_empty('room_id')
        self.validate_existance('user_id', User)
        self.validate_existance('room_id', Room)

        self.validate_field(
                              'message',
                              self.validate_message,
                              'Message too long, max length is 255'
                           )

    def validate_message(self, message):
        return len(message) <= 255
```

For running validations on our models we have to redefine the method validate,
in which we will set all our pre save validations.

**validate_not_empty**: Validates that our field has any data

**validate_existance**: Validates that the relationship field matches an object
                        on the relationship model

**validate_field**: Validates the given field with a custom function,
                    the function should receive only *one* argument
                    representing the value to validate and should
                    return a boolean. Also, accepts an optional error message.

**validate_in**: Validates that the given field has a value inside the provided
                 value list.

**validate_type**: Validates that the given field contains an object of the
                   expected type. **Valid Types**: Any kind of Struct (models),
                   strings, integers, floats, lists and dictionaries.
