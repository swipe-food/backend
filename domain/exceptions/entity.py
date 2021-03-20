from domain.exceptions.base import FoodSwipeError


class EntityError(FoodSwipeError):
    """Base exception for errors related to entities"""
    pass


class DiscardEntityError(EntityError):
    """Raised when an attempt is made to use a discarded entity"""
    pass
