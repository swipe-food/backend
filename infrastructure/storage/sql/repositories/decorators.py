from decorator import decorator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from common.exceptions import RepositoryException, StorageException, StorageNoResultFoundException, StorageAddException, StorageDeleteException, StorageUpdateException


@decorator
def catch_add_data_exception(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)

    except SQLAlchemyError as exception:
        raise StorageAddException(exception) from None
    except Exception as exception:
        raise RepositoryException(exception) from None


@decorator
def catch_no_result_found_exception(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)

    except NoResultFound as exception:
        raise StorageNoResultFoundException(exception) from None
    except SQLAlchemyError as exception:
        raise StorageException(exception) from None
    except Exception as exception:
        raise RepositoryException(exception) from None


@decorator
def catch_update_data_exception(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)

    except SQLAlchemyError as exception:
        raise StorageUpdateException(exception) from None
    except Exception as exception:
        raise RepositoryException(exception) from None


@decorator
def catch_delete_data_exception(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)

    except SQLAlchemyError as exception:
        raise StorageDeleteException(exception) from None
    except Exception as exception:
        raise RepositoryException(exception) from None
