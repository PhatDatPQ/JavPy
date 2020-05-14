from JavPy.utils.db.DB import DB
from pathlib import Path


_config_path = Path.home().joinpath(".JavPy/config.json")
_db_path = Path.home().joinpath(".JavPy/config.db")
if not _db_path.exists():
    db = DB(str(_db_path))
    db.migrate_from_json(str(_config_path))
    db.close()

config_db = DB(str(_db_path))
