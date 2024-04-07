class ThumbnailError(Exception):
    """
    Base thumbnail exception
    """

    default_message = "Thumbnail Exception."
    default_code = "thumbnail_exception"

    def __init__(self, message: str | None = None, code: str | None = None):
        """
        Attributes:
            message: Custom error message.
            code: Custom error code.
        """
        self.message = message or self.default_message
        self.code = code or self.default_code
        super().__init__(f"Error `{self.code}`: {self.message}")


class WrongPropertyOptionError(ThumbnailError):
    """
    Exception wrong property option
    """

    default_message = "The value of `{option}` is invalid for property `{prop}`."
    default_code = "wrong_property_option"

    def __init__(self, prop: str, option: str, message: str | None = None, code: str | None = None):
        """
        Attributes:
            prop: The property with the problem.
            option: Value with which there was a problem.
            message: Custom error message.
            code: Custom error code.
        """
        message = (message or self.default_message).format(prop=prop, option=option)
        code = code or self.default_code
        super().__init__(message, code)


class ActionError(ThumbnailError):
    """
    Action exception
    """

    default_message = "Action exception."
    default_code = "action_exception"


class ThumbnailerError(ThumbnailError):
    """
    Thumbnailer exception
    """

    default_message = "Thumbnailer default exception."
    default_code = "thumbnailer_exception"


class WrongActionOrPropertyError(ThumbnailerError):
    """
    Wrong action or property exception
    """

    default_message = "Action or property `{job}` not registered."
    default_code = "wrong_action_or_property"

    def __init__(self, job: str, message: str | None = None, code: str | None = None):
        """
        Attributes:
            job: Action with problem.
            message: Custom error message.
            code: Custom error code.
        """
        message = (message or self.default_message).format(job=job)
        super().__init__(message, code)


class WrongFormatError(ThumbnailerError):
    """
    Wrong action or property exception
    """

    default_message = "`{out_format}` format is not supported."
    default_code = "wrong_action_or_property"

    def __init__(self, out_format: str, message: str | None = None, code: str | None = None):
        """
        Attributes:
            out_format: Problem format.
            message: Custom error message.
            code: Custom error code.
        """
        message = (message or self.default_message).format(out_format=out_format)
        super().__init__(message, code)
