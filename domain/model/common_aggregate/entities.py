import uuid

from domain.model.entity import Entity


class DiscardEntityError(Exception):
    """Raised when an attempt is made to use a discarded entity"""
    pass  # TODO extract Exceptions to own package in domain


class Language(Entity):

    def __init__(self, language_id: uuid.UUID, language_version: int, name: str, code: str):
        super().__init__(language_id, language_version)
        self._name = name
        self._code = code

    def __str__(self) -> str:
        return f"Language '{self._name}' with code '{self._code}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, {code!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            code=self._code,
        )

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @property
    def code(self) -> str:
        """The language code according to ISO 639-1"""
        self._check_not_discarded()
        return self._code
