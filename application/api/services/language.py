from __future__ import annotations

import uuid
from typing import List

from domain.exceptions import InvalidValueException
from domain.model.language_aggregate import Language
from domain.repositories.language import AbstractLanguageRepository
from domain.services.language import AbstractLanguageService


def create_language_service(language_repo: AbstractLanguageRepository) -> LanguageService:
    if not isinstance(language_repo, AbstractLanguageRepository):
        raise InvalidValueException(LanguageService, 'language_repo must be a AbstractLanguageRepository')
    return LanguageService(repo=language_repo)


class LanguageService(AbstractLanguageService):

    def __init__(self, repo: AbstractLanguageRepository):
        self._repo = repo

    def get_by_id(self, language_id: uuid.UUID) -> Language:
        return self._repo.get_by_id(language_id)

    def get_all(self, limit: int) -> List[Language]:
        return self._repo.get_all(limit)
