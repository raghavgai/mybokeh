#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Various kinds of slider widgets.

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import numbers
from datetime import date, datetime

# Bokeh imports
from ...core.has_props import abstract
from ...core.properties import (
    Bool,
    Color,
    Date,
    Enum,
    Float,
    Int,
    Override,
    String,
    Tuple,
)
from ...core.validation import error
from ...core.validation.errors import EQUAL_SLIDER_START_END
from .widget import Widget

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'AbstractSlider',
    'Slider',
    'RangeSlider',
    'DateSlider',
    'DateRangeSlider',
)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

@abstract
class AbstractSlider(Widget):
    """ """

    def __init__(self, **kwargs):
        if 'start' in kwargs and 'end' in kwargs:
            if kwargs['start'] == kwargs['end']:
                raise ValueError("Slider 'start' and 'end' cannot be equal.")
        super().__init__(**kwargs)

    title = String(default="", help="""
    Slider's label.
    """)

    show_value = Bool(default=True, help="""
    Whether or not show slider's value.
    """)

    format = String(help="""
    """)

    direction = Enum("ltr", "rtl", help="""
    """)

    tooltips = Bool(default=True, help="""
    """)

    bar_color = Color(default="#e6e6e6", help="""
    """)

    @error(EQUAL_SLIDER_START_END)
    def _check_missing_dimension(self):
        if hasattr(self, 'start') and hasattr(self, 'end'):
            if self.start == self.end:
                return '{!s} with title {!s}'.format(self, self.title)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Slider(AbstractSlider):
    """ Slider-based number selection widget. """

    start = Float(help="""
    The minimum allowable value.
    """)

    end = Float(help="""
    The maximum allowable value.
    """)

    value = Float(help="""
    Initial or selected value.
    """)

    value_throttled = Float(help="""
    Initial or selected value, throttled according to callback_policy.
    """)

    step = Float(default=1, help="""
    The step between consecutive values.
    """)

    format = Override(default="0[.]00")

class RangeSlider(AbstractSlider):
    """ Range-slider based number range selection widget. """

    value = Tuple(Float, Float, help="""
    Initial or selected range.
    """)

    value_throttled = Tuple(Float, Float, help="""
    Initial or selected value, throttled according to callback_policy.
    """)

    start = Float(help="""
    The minimum allowable value.
    """)

    end = Float(help="""
    The maximum allowable value.
    """)

    step = Float(default=1, help="""
    The step between consecutive values.
    """)

    format = Override(default="0[.]00")

class DateSlider(AbstractSlider):
    """ Slider-based date selection widget. """

    value = Date(help="""
    Initial or selected value.
    """)

    value_throttled = Date(help="""
    Initial or selected value, throttled according to callback_policy.
    """)

    start = Date(help="""
    The minimum allowable value.
    """)

    end = Date(help="""
    The maximum allowable value.
    """)

    step = Int(default=1, help="""
    The step between consecutive values.
    """)

    format = Override(default="%d %b %Y")

class DateRangeSlider(AbstractSlider):
    """ Slider-based date range selection widget. """

    @property
    def value_as_datetime(self):
        ''' Convenience property to retrieve the value tuple as a tuple of
        datetime objects.

        '''
        if self.value is None:
            return None
        v1, v2 = self.value
        if isinstance(v1, numbers.Number):
            d1 = datetime.utcfromtimestamp(v1 / 1000)
        else:
            d1 = v1
        if isinstance(v2, numbers.Number):
            d2 = datetime.utcfromtimestamp(v2 / 1000)
        else:
            d2 = v2
        return d1, d2    \

    @property
    def value_as_date(self):
        ''' Convenience property to retrieve the value tuple as a tuple of
        date objects.

        Added in version 1.1
        '''
        if self.value is None:
            return None
        v1, v2 = self.value
        if isinstance(v1, numbers.Number):
            dt = datetime.utcfromtimestamp(v1 / 1000)
            d1 = date(*dt.timetuple()[:3])
        else:
            d1 = v1
        if isinstance(v2, numbers.Number):
            dt = datetime.utcfromtimestamp(v2 / 1000)
            d2 = date(*dt.timetuple()[:3])
        else:
            d2 = v2
        return d1, d2

    value = Tuple(Date, Date, help="""
    Initial or selected range.
    """)

    value_throttled = Tuple(Date, Date, help="""
    Initial or selected value, throttled according to callback_policy.
    """)

    start = Date(help="""
    The minimum allowable value.
    """)

    end = Date(help="""
    The maximum allowable value.
    """)

    step = Int(default=1, help="""
    The step between consecutive values.
    """)

    format = Override(default="%d %b %Y")

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
