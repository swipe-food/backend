class FoodSwipeError(Exception):
    """Base exception class for all Food Swipe exceptions"""
    pass


class EntityError(FoodSwipeError):
    """Base exception for errors related to entities"""
    pass


class DiscardEntityError(EntityError):
    """Raised when an attempt is made to use a discarded entity"""
    pass
