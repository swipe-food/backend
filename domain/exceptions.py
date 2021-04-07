import inspect


class FoodSwipeException(Exception):
    """Base exception class for all Food Swipe exceptions"""
    pass


class InvalidValueException(FoodSwipeException, ValueError):
    def __init__(self, raiser: type or object, message: str, *args):
        class_name = raiser.__name__ if inspect.isclass(raiser) else raiser.__class__.__name__
        super().__init__(f'{class_name}: {message}', *args)


class EntityException(FoodSwipeException):
    """Base exception for errors related to entities"""
    pass


class DiscardEntityException(EntityException):
    """Raised when an attempt is made to use a discarded entity"""
    pass


class MissingConfigException(FoodSwipeException):
    """Raised when a required configuration field is missing"""
    pass


class MissingArgumentException(FoodSwipeException):
    """Raised when a required parameter is None"""
    pass


class RepositoryException(FoodSwipeException):
    """Raised when a error in the repository occurs"""
    pass


class StorageException(FoodSwipeException):
    """Raised when a error in the storage modules occurs"""


class StorageAddException(StorageException):
    """Raised when a add request failed"""


class StorageNoResultFoundException(StorageException):
    """Raised when no result was found"""


class StorageUpdateException(StorageException):
    """Raised when a update request failed"""


class StorageDeleteException(StorageException):
    """Raised when a delete request failed"""