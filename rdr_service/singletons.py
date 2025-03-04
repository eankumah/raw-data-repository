import threading
from datetime import timedelta

from rdr_service.clock import CLOCK

singletons_lock = threading.RLock()
singletons_map = {}

CODE_CACHE_INDEX = 0
HPO_CACHE_INDEX = 1
SITE_CACHE_INDEX = 2
SQL_DATABASE_INDEX = 3
ORGANIZATION_CACHE_INDEX = 4
GENERIC_SQL_DATABASE_INDEX = 5
MAIN_CONFIG_INDEX = 6
DB_CONFIG_INDEX = 7
BACKUP_SQL_DATABASE_INDEX = 8
ALEMBIC_SQL_DATABASE_INDEX = 9
READ_UNCOMMITTED_DATABASE_INDEX = 10
BASICS_PROFILE_UPDATE_CODES_CACHE_INDEX = 11


def reset_for_tests():
    with singletons_lock:
        singletons_map.clear()


def _get(cache_index):
    existing_pair = singletons_map.get(cache_index)
    if existing_pair and (existing_pair[1] is None or existing_pair[1] >= CLOCK.now()):
        return existing_pair[0]
    return None


def get(cache_index, constructor, cache_ttl_seconds=None, **kwargs):
    """Get a cache with a specified index from the list above. If not initialized, use
  constructor to initialize it; if cache_ttl_seconds is set, reload it after that period."""
    # First try without a lock
    result = _get(cache_index)
    if result:
        return result

    # Then grab the lock and try again
    with singletons_lock:
        result = _get(cache_index)
        if result:
            return result
        else:
            new_instance = constructor(**kwargs)
            expiration_time = None
            if cache_ttl_seconds is not None:
                expiration_time = CLOCK.now() + timedelta(seconds=cache_ttl_seconds)
            singletons_map[cache_index] = (new_instance, expiration_time)
            return new_instance


def invalidate(cache_index):
    with singletons_lock:
        singletons_map[cache_index] = None
