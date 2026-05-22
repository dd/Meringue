import pytest

from PIL import Image

from meringue.thumbnail.actions import crop
from meringue.thumbnail.actions import get_size
from meringue.thumbnail.actions import resize
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
from meringue.thumbnail.constants import RESIZE_METHOD_CONTAIN
from meringue.thumbnail.constants import RESIZE_METHOD_COVER
from meringue.thumbnail.constants import RESIZE_METHOD_STRETCH
from meringue.thumbnail.constants import RESIZE_STRATEGY_DO_NOT_INCREASE_SIZE
from meringue.thumbnail.constants import RESIZE_STRATEGY_DO_NOT_REDUCE_SIZE
from meringue.thumbnail.constants import RESIZE_STRATEGY_STANDARD
from meringue.thumbnail.exceptions import ActionError


def make_options(**overrides):
    opts = {
        PROP_NEW_SIZE: [100.0, 100.0],
        PROP_MAX_WIDTH: None,
        PROP_MAX_HEIGHT: None,
        PROP_CURRENT_SIZE: [200.0, 100.0],
        PROP_BG_COLOR: (200, 200, 200, 0),
        PROP_CROP_METHOD: [CROP_METHOD_CENTER, CROP_METHOD_CENTER],
        PROP_RESIZE_METHOD: RESIZE_METHOD_CONTAIN,
        PROP_RESIZE_STRATEGY: RESIZE_STRATEGY_STANDARD,
    }
    opts.update(overrides)
    return opts


class TestGetSize:
    def test_returns_new_size(self):
        opts = make_options(**{PROP_NEW_SIZE: [300.0, 200.0]})
        assert get_size(opts) == [300.0, 200.0]

    def test_clamps_to_max_width(self):
        opts = make_options(**{PROP_NEW_SIZE: [300.0, 200.0], PROP_MAX_WIDTH: 250.0})
        result = get_size(opts)
        assert result[0] == 250.0

    def test_clamps_to_max_height(self):
        opts = make_options(**{PROP_NEW_SIZE: [300.0, 200.0], PROP_MAX_HEIGHT: 150.0})
        result = get_size(opts)
        assert result[1] == 150.0

    def test_no_clamp_when_max_sizes_false(self):
        opts = make_options(**{
            PROP_NEW_SIZE: [300.0, 200.0],
            PROP_MAX_WIDTH: 100.0,
            PROP_MAX_HEIGHT: 50.0,
        })
        result = get_size(opts, max_sizes=False)
        assert result == [300.0, 200.0]


class TestCrop:
    def test_center_crop(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [150.0, 80.0],
            PROP_CROP_METHOD: [CROP_METHOD_CENTER, CROP_METHOD_CENTER],
        })
        result = crop(image, opts)
        assert result.size == (150, 80)

    def test_left_top_crop(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [150.0, 80.0],
            PROP_CROP_METHOD: [CROP_METHOD_LEFT, CROP_METHOD_TOP],
        })
        result = crop(image, opts)
        assert result.size == (150, 80)

    def test_right_bottom_crop(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [150.0, 80.0],
            PROP_CROP_METHOD: [CROP_METHOD_RIGHT, CROP_METHOD_BOTTOM],
        })
        result = crop(image, opts)
        assert result.size == (150, 80)

    def test_updates_current_size(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{PROP_NEW_SIZE: [150.0, 80.0]})
        crop(image, opts)
        assert opts[PROP_CURRENT_SIZE] == [150, 80]


class TestResize:
    def test_cover_enlarges(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [400.0, 200.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_COVER,
        })
        result = resize(image, opts)
        assert result.size == (400, 200)

    def test_contain_shrinks(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [100.0, 100.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_CONTAIN,
        })
        result = resize(image, opts)
        assert result.size[0] == 100
        assert result.size[1] == 50

    def test_cover_shrinks_proportionally(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [100.0, 100.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_COVER,
        })
        result = resize(image, opts)
        assert result.size == (200, 100)

    def test_stretch(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [300.0, 50.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_STRETCH,
        })
        result = resize(image, opts)
        assert result.size == (300, 50)

    def test_no_increase_strategy(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [400.0, 200.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_COVER,
            PROP_RESIZE_STRATEGY: RESIZE_STRATEGY_DO_NOT_INCREASE_SIZE,
        })
        result = resize(image, opts)
        assert result.size == (200, 100)

    def test_no_reduce_strategy(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [100.0, 50.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_COVER,
            PROP_RESIZE_STRATEGY: RESIZE_STRATEGY_DO_NOT_REDUCE_SIZE,
        })
        result = resize(image, opts)
        assert result.size == (200, 100)

    def test_stretch_with_non_standard_strategy_raises(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [300.0, 50.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_STRETCH,
            PROP_RESIZE_STRATEGY: RESIZE_STRATEGY_DO_NOT_INCREASE_SIZE,
        })
        with pytest.raises(ActionError):
            resize(image, opts)

    def test_no_resize_if_same_size(self):
        image = Image.new("RGBA", (200, 100))
        opts = make_options(**{
            PROP_NEW_SIZE: [200.0, 100.0],
            PROP_RESIZE_METHOD: RESIZE_METHOD_CONTAIN,
        })
        result = resize(image, opts)
        assert result.size == (200, 100)
