from datetime import datetime

import pytest

from main import get_weekend_dates


def test_get_weekend_dates():
    start, end = get_weekend_dates()
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert end > start
    assert (end - start).days == 1
