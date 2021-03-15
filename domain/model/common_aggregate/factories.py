import uuid

from domain.model.common_aggregate.entities import Language


def create_entity_id() -> uuid.UUID:
    return uuid.uuid4()


def create_language(version: int, name: str, code: str):
    if len(code) != 2:
        raise ValueError('Language Acronym must have a length of 2')
    return Language(language_id=create_entity_id(),
                    language_version=version,
                    name=name,
                    code=code)
