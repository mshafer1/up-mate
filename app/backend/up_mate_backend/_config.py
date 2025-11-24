import pathlib as _pathlib
import decouple as _decouple

_module_dir = _pathlib.Path(__file__)
_cwd = _pathlib.Path.cwd()

_conf = _decouple.AutoConfig(search_path=_cwd)

DB_HOST = _conf("UP_MATE_DB_HOST", default="localhost:27017")
DB_NAME = _conf("UP_MATE_DB_NAME", default="up-mate")
DB_USER = _conf("UP_MATE_DB_USER")
DB_PASS = _conf("UP_MATE_DB_PASS")

DB_CONNECTION_STRING = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
