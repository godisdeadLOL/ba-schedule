from datetime import datetime


def get_time_delta(a: datetime, b: datetime):
    return (b - a).total_seconds()

def parse_timestamp(timestamp: str):
    return datetime.strptime(timestamp, "%m/%d/%Y %H:%M")