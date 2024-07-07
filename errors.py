GENERIC_BAD_REQUEST = 4000
MISSING_FOOD_DATA = 4001
MISSING_FOOD_SIZE = 4002
ENTRY_NOT_FOUND = 4003
GENERIC_SERVER_ERROR = 5000

class GeneralException(Exception):
    """Base class for other exceptions"""
    def __init__(self, http_status_code: int, *args, **kwargs):
        # If the key `msg` is provided, provide the msg string
        # to Exception class in order to display
        # the msg while raising the exception
        self.http_status_code = http_status_code
        self.kwargs = kwargs
        msg = kwargs.get('msg', kwargs.get('message'))
        if msg:
            args = (msg,)
            super().__init__(args)
        self.args = list(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


class EntryNotFound(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message="Entry not found", 
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=404,
            code=ENTRY_NOT_FOUND,
            *args, **kwargs
        )

class MissingFoodData(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message="Required data is missing",
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=400,
            code=MISSING_FOOD_DATA, 
            *args, **kwargs
        )

class MissingFoodSize(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message="Food size is required for this category",
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=400,
            code=MISSING_FOOD_SIZE,
            *args, **kwargs
        )

class DatabaseException(GeneralException):
    pass

class ResturantException(DatabaseException):
    pass

class CustomerException(DatabaseException):
    pass

class EntityNotFound(DatabaseException):
    pass

class DataInconsistencyError(Exception):
    pass







