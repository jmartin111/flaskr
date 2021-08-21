import pytz


def timezone_filter(value, time_format='%c'):
    pst = pytz.timezone('US/Pacific')
    utc = pytz.timezone('UTC')
    tz_aware_dt = utc.localize(value)
    local_dt = tz_aware_dt.astimezone(pst)
    return local_dt.strftime(time_format)
