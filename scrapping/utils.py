from datetime import datetime, timedelta


def get_time_delta(a: datetime, b: datetime):
    return (b - a).total_seconds()


def parse_timestamp(timestamp: str):
    tz_delta = timedelta(hours=9)
    return datetime.strptime(timestamp, "%m/%d/%Y %H:%M") - tz_delta
