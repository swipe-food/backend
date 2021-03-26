import inspect


class FoodSwipeError(Exception):
    """Base exception class for all Food Swipe exceptions"""
    pass


class InvalidValueError(FoodSwipeError, ValueError):
    def __init__(self, raiser: type or object, message: str, *args):
        class_name = raiser.__name__ if inspect.isclass(raiser) else raiser.__class__.__name__
        super().__init__(f'{class_name}: {message}', *args)


class EntityError(FoodSwipeError):
    """Base exception for errors related to entities"""
    pass


class DiscardEntityError(EntityError):
    """Raised when an attempt is made to use a discarded entity"""
    pass


class MissingConfigError(FoodSwipeError):
    """Raised when a required configuration field is missing"""
    pass
