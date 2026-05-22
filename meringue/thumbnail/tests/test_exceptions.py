import pytest

from meringue.thumbnail.exceptions import ActionError
from meringue.thumbnail.exceptions import ThumbnailerError
from meringue.thumbnail.exceptions import ThumbnailError
from meringue.thumbnail.exceptions import WrongActionOrPropertyError
from meringue.thumbnail.exceptions import WrongFormatError
from meringue.thumbnail.exceptions import WrongPropertyOptionError


class TestThumbnailError:
    def test_default_message(self):
        err = ThumbnailError()
        assert err.message == "Thumbnail Exception."
        assert err.code == "thumbnail_exception"
        assert "thumbnail_exception" in str(err)

    def test_custom_message(self):
        err = ThumbnailError(message="custom msg", code="custom_code")
        assert err.message == "custom msg"
        assert err.code == "custom_code"


class TestWrongPropertyOptionError:
    def test_default_message_formatting(self):
        err = WrongPropertyOptionError("resize_method", "invalid_value")
        assert "invalid_value" in err.message
        assert "resize_method" in err.message
        assert err.code == "wrong_property_option"

    def test_custom_message(self):
        err = WrongPropertyOptionError("prop", "opt", message="custom {prop} {option}")
        assert err.message == "custom prop opt"


class TestActionError:
    def test_defaults(self):
        err = ActionError()
        assert err.code == "action_exception"


class TestThumbnailerError:
    def test_defaults(self):
        err = ThumbnailerError()
        assert err.code == "thumbnailer_exception"


class TestWrongActionOrPropertyError:
    def test_message_formatting(self):
        err = WrongActionOrPropertyError("unknown_job")
        assert "unknown_job" in err.message
        assert err.code == "wrong_action_or_property"


class TestWrongFormatError:
    def test_message_formatting(self):
        err = WrongFormatError("AVIF")
        assert "AVIF" in err.message
        assert err.code == "wrong_format"
