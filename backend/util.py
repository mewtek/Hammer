from datetime import datetime, timedelta

def add_time(start_time: datetime, time_to_add: str) -> datetime:
    """
    Adds time to an initial datetime based off
    a specifically formatted string.

    Args:
        start_time (datetime): Time to add to
        time_to_add (str): Addition string. Formatted like "1y 2d 3h 4m"

    Returns:
        datetime: Added time
    """

    added_time = start_time
    time = time_to_add.split()

    for t in time:
        unit = t[-1:]
        amount = t[:-1]

        if unit == 'y':
            added_time = added_time + timedelta(days=amount * 365)
        elif unit == 'n':
            added_time = added_time + timedelta(days=amount * 30)
        elif unit == 'd':
            added_time = added_time + timedelta(days=amount)
        elif unit == 'w':
            added_time = added_time + timedelta(weeks=amount)
        elif unit == 'h':
            added_time = added_time + timedelta(hours=amount)
        elif unit == 'm':
            added_time = added_time + timedelta(minutes=amount)

    return added_time