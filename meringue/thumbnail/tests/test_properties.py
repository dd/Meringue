import pytest

from meringue.thumbnail.constants import CROP_METHOD_BOTTOM
from meringue.thumbnail.constants import CROP_METHOD_CENTER
from meringue.thumbnail.constants import CROP_METHOD_LEFT
from meringue.thumbnail.constants import CROP_METHOD_RIGHT
from meringue.thumbnail.constants import CROP_METHOD_TOP
from meringue.thumbnail.constants import PROP_BG_COLOR
from meringue.thumbnail.constants import PROP_CROP_METHOD
from meringue.thumbnail.constants import PROP_CURRENT_SIZE
from meringue.thumbnail.constants import PROP_MAX_HEIGHT
from meringue.thumbnail.constants import PROP_MAX_WIDTH
from meringue.thumbnail.constants import PROP_NEW_SIZE
from meringue.thumbnail.constants import PROP_RESIZE_METHOD
from meringue.thumbnail.constants import PROP_RESIZE_STRATEGY
from meringue.thumbnail.exceptions import WrongPropertyOptionError
from meringue.thumbnail.properties import set_bg_color
from meringue.thumbnail.properties import set_crop_method
from meringue.thumbnail.properties import set_max_height
from meringue.thumbnail.properties import set_max_width
from meringue.thumbnail.properties import set_resize_method
from meringue.thumbnail.properties import set_resize_strategy
from meringue.thumbnail.properties import set_size


class TestSetCropMethod:
    def test_center_single_value(self):
        result = set_crop_method("center", {})
        assert result == {PROP_CROP_METHOD: [CROP_METHOD_CENTER, CROP_METHOD_CENTER]}

    def test_two_valid_values(self):
        result = set_crop_method("left top", {})
        assert result == {PROP_CROP_METHOD: [CROP_METHOD_LEFT, CROP_METHOD_TOP]}

    def test_right_bottom(self):
        result = set_crop_method("right bottom", {})
        assert result == {PROP_CROP_METHOD: [CROP_METHOD_RIGHT, CROP_METHOD_BOTTOM]}

    def test_center_center(self):
        result = set_crop_method("center center", {})
        assert result == {PROP_CROP_METHOD: [CROP_METHOD_CENTER, CROP_METHOD_CENTER]}

    def test_single_non_center_raises(self):
        with pytest.raises(WrongPropertyOptionError):
            set_crop_method("left", {})

    def test_invalid_first_position_raises(self):
        with pytest.raises(WrongPropertyOptionError):
            set_crop_method("top center", {})

    def test_invalid_second_position_raises(self):
        with pytest.raises(WrongPropertyOptionError):
            set_crop_method("center left", {})

    def test_three_values_raises(self):
        with pytest.raises(WrongPropertyOptionError):
            set_crop_method("left top center", {})


class TestSetResizeMethod:
    @pytest.mark.parametrize("method", ["cover", "contain", "stretch"])
    def test_valid_methods(self, method):
        result = set_resize_method(method, {})
        assert result == {PROP_RESIZE_METHOD: method}

    def test_invalid_method_raises(self):
        with pytest.raises(WrongPropertyOptionError):
            set_resize_method("invalid", {})


class TestSetResizeStrategy:
    @pytest.mark.parametrize("strategy", ["no_increase", "standard", "no_reduce"])
    def test_valid_strategies(self, strategy):
        result = set_resize_strategy(strategy, {})
        assert result == {PROP_RESIZE_STRATEGY: strategy}

    def test_invalid_strategy_raises(self):
        with pytest.raises(WrongPropertyOptionError):
            set_resize_strategy("invalid", {})


class TestSetSize:
    def test_both_dimensions(self):
        opt = {PROP_CURRENT_SIZE: [200.0, 100.0]}
        result = set_size("300x150", opt)
        assert result == {PROP_NEW_SIZE: [300.0, 150.0]}

    def test_width_only(self):
        opt = {PROP_CURRENT_SIZE: [200.0, 100.0]}
        result = set_size("300x", opt)
        assert result == {PROP_NEW_SIZE: [300.0, 150.0]}

    def test_height_only(self):
        opt = {PROP_CURRENT_SIZE: [200.0, 100.0]}
        result = set_size("x150", opt)
        assert result == {PROP_NEW_SIZE: [300.0, 150.0]}


class TestSetMaxWidth:
    def test_sets_float(self):
        result = set_max_width("500", {})
        assert result == {PROP_MAX_WIDTH: 500.0}


class TestSetMaxHeight:
    def test_sets_float(self):
        result = set_max_height("300", {})
        assert result == {PROP_MAX_HEIGHT: 300.0}


class TestSetBgColor:
    def test_rgba(self):
        result = set_bg_color("255 128 0 128", {})
        assert result == {PROP_BG_COLOR: (255, 128, 0, 128)}

    def test_rgb(self):
        result = set_bg_color("100 200 50", {})
        assert result == {PROP_BG_COLOR: (100, 200, 50)}
