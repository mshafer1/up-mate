import pathlib as _pathlib

import decouple as _decouple

_module_dir = _pathlib.Path(__file__)
_cwd = _pathlib.Path.cwd()

_conf = _decouple.AutoConfig(search_path=_cwd)

DB_HOST = _conf("UP_MATE_DB_HOST", default="localhost:27017")
DB_NAME = _conf("UP_MATE_DB_NAME", default="up-mate")
DB_USER = _conf("UP_MATE_DB_USER")
DB_PASS = _conf("UP_MATE_DB_PASS")

DEBUG = _conf("UP_MATE_DEBUG", cast=bool, default=False)

DB_CONNECTION_STRING = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

USERS = _conf("UP_MATE_USERS_CSV", cast=lambda o: o.split(","))

NOTIFY = _conf("UP_MATE_NOTIFY", default=False, cast=bool)
if NOTIFY:
    print("Notifications are ENABLED")
    NOTIFY_CHANNEL_TEMPLATE = _conf("UP_MATE_NOTIFY_CHANNEL_TEMPLATE", default="up-mate-{}")
    NOTIFY_HOST = _conf("UP_MATE_NOTIFY_HOST")
    NOTIFY_TOKEN = _conf("UP_MATE_NOTIFY_TOKEN")
    WEB_DOMAIN_NAME = _conf("UP_MATE_DOMAIN_NAME")
    WEB_URL_PREFIX = "https://" if _conf("UP_MATE_NOTIFICATION_LINK_USE_HTTPS", default=False, cast=bool) else "http://"
else:
    print("Notifications are DISABLED")
    NOTIFY_CHANNEL_TEMPLATE = None
    NOTIFY_HOST = None
    NOTIFY_TOKEN = None
    WEB_DOMAIN_NAME = None
    WEB_URL_PREFIX = None
