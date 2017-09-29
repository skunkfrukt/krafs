import collections
import datetime
import random


DateSpan = collections.namedtuple('DateSpan', ("start", "end"))


def generate_date_spans(
        min_date:datetime.date, max_date:datetime.date, num_spans:int,
        allow_overlap=False):
    """Generate a number (num_spans) of date spans between min_date and
    max_date inclusive.
    """
    superspan_length = (max_date - min_date).days
    start_date_offsets = sorted(
        random.sample(range(superspan_length + 1), num_spans))
    end_date_offsets = []
    for i, sdo in enumerate(start_date_offsets):
        if allow_overlap or i == num_spans - 1:
            max_end_date_offset_for_span = superspan_length
        else:
            max_end_date_offset_for_span = start_date_offsets[i + 1] - 1
        end_date_offsets.append(
            random.randint(sdo, max_end_date_offset_for_span))
    date_spans = []
    for sdo, edo in zip(start_date_offsets, end_date_offsets):
        start_date = min_date + datetime.timedelta(days=sdo)
        end_date = min_date + datetime.timedelta(days=edo)
        yield DateSpan(start_date, end_date)


def generate_date_spans_log(
        min_date:datetime.date, max_date:datetime.date,
        allow_overlap:bool=False):
    """Generate a logarithmically distributed number of date spans
    between min_date and max_date inclusive.
    """
    superspan_length = (max_date - min_date).days
    num_spans = round(2 ** random.uniform(0, math.log2(superspan_length)))
    return generate_date_spans(min_date, max_date, num_spans, allow_overlap)


def date_range(
        start_date:datetime.date, end_date:datetime.date=None, step:int=1):
    """Generate a range of dates such that start_date <= x < end_date."""
    current_date = start_date
    while end_date is None or current_date < end_date:
        yield current_date
        current_date += datetime.timedelta(days=step)


def month_range(start_date:datetime.date, num_months:int=None, step:int=1):
    month_offset = 0
    while num_months is None or month_offset < num_months:
        year_offset, month = divmod(start_date.month + month_offset, 12)
        if month == 0:
            month = 12
        year = start_date.year + year_offset
        day = start_date.day
        if month == 2:
            # Handle leap years.
            if year % 4 == 0 and (year % 100 > 0 or year % 400 == 0):
                day = min(day, 29)
            else:
                day = min(day, 28)
        elif month in (4, 6, 9, 11):
            day = min(day, 30)
        yield datetime.date(year, month, day)
        month_offset += step
