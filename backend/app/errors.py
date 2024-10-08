PARTIAL_SUCCESS = 3000

GENERIC_BAD_REQUEST = 4000
MISSING_ENTRY_DATA = 4001
# MISSING_FOOD_SIZE = 4002
BAD_ENTRY_DATA = 4003
ENTRY_NOT_FOUND = 4004

GENERIC_SERVER_ERROR = 5000


class GeneralException(Exception):
    """Base class for other exceptions"""

    def __init__(self, *args, **kwargs):
        # If the key `message` is provided,
        # provide the message string to Exception class
        # in order to display the message while raising the exception
        self.http_status_code = kwargs.get("http_status_code", 500)
        default_message = kwargs.get("default_message")
        if (
            len(args) > 0
        ):  # If there are any arguments, the first one is the message string
            kwargs["message"] = args[0]
            super().__init__(args[0])
        elif (
            default_message
        ):  # Otherwise, if the keyword argument default_message exists, its the exception string
            kwargs["message"] = default_message
            super().__init__(default_message)
        self.kwargs = kwargs
        # self.args = list(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


class BadRequest(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            default_message="Invalid request",
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=400,
            code=GENERIC_BAD_REQUEST,
            *args,
            **kwargs,
        )


class EntryNotFound(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            default_message="Entry not found",
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=404,
            code=ENTRY_NOT_FOUND,
            *args,
            **kwargs,
        )


class MissingEntryData(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            default_message="Required entry data is missing",
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=400,
            code=MISSING_ENTRY_DATA,
            *args,
            **kwargs,
        )


class ImproperEntryData(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            default_message="Improper entry data",
            data={} if not kwargs.get("data") else kwargs.get("data"),
            http_status_code=400,
            code=BAD_ENTRY_DATA,
            *args,
            **kwargs,
        )


class CoreError(GeneralException):
    pass


class MustDeleteOrders(CoreError):
    pass


class CustomerNotFoundError(CoreError):
    pass


class DatabaseException(GeneralException):
    pass


class ResturantException(MissingEntryData, DatabaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomerException(DatabaseException):
    pass


class EntityNotFound(EntryNotFound, DatabaseException):
    pass


class DataInconsistencyError(DatabaseException):
    pass
