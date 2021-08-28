import redis
import json
from functools import wraps
from datetime import datetime
from scrapers.base.response import SOLD_OUT


config = {
    'host': 'redis.pythonweekend.skypicker.com',
    'port': 6379,
    'decode_responses': True,
}

redis = redis.Redis(**config)

def serialize(o):
    time_format = "%Y-%m-%dT%H:%M:%S.000%z"
    if isinstance(o, datetime):
        return datetime.strftime(o, time_format)
    elif o == SOLD_OUT:
        return "sold_out"

    raise ValueError(f'{type(o)} is not JSON serializable')

def deserialize(o):
    for k, v in o.items():
        time_format = "%Y-%m-%dT%H:%M:%S.000%z"
        if 'datetime' in k:
            o[k] = datetime.strptime(v, time_format)
        if v == "sold_out":
            o[k] = SOLD_OUT
    return o

def get_redis_key(base, *args, name=None):
    """Get redis key.

    Args:
        base (str): base part of key
        *args: additional keys that will form redis key
        name (str): name of scraper

    Returns:
        str: key under which data are stored

    """
    key_parts = [name, base] if name else [base]
    key_parts += [str(x) for x in args]

    return '_'.join(key_parts)

def redis_cache(time=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs) -> None:
            date = request.date.strftime("%Y-%m-%d")
            key = '_'.join([
                request.src,
                request.dst,
                date
            ])
            trips = redis.get(key)

            if trips is not None:
                trips = json.loads(trips, object_hook=deserialize)
                yield from trips
                return

            trips = []
            for trip in func(request, *args, **kwargs):
                trips.append(trip)
                yield trip

            redis.set(key, json.dumps(trips, default=serialize), ex=time)

        return wrapper

    return decorator
