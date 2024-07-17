MISSING_ENTRY_DATA = 1


class GeneralException(Exception):
    """Base class for other exceptions"""

    def __init__(self, *args, **kwargs):
        # If the key `message` is provided,
        # provide the message string to Exception class
        # in order to display the message while raising the exception
        self.http_status_code = kwargs.get("http_status_code", None)
        default_message = kwargs.get("default_message")
        if len(args) > 0:
            super().__init__(args[0])
        elif default_message:
            super().__init__(default_message)
        self.kwargs = kwargs
        # self.args = list(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


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


raise MissingEntryData("whats good")
