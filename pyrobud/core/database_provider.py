from typing import TYPE_CHECKING, Any, Optional
import logging
from pathlib import Path

# Try to import plyvel - fallback to in-memory storage if unavailable
try:
    import plyvel
    PLYVEL_AVAILABLE = True
except ImportError:
    plyvel = None
    PLYVEL_AVAILABLE = False
    logging.warning("plyvel not available - database features will use in-memory storage")

from .. import util
from .bot_mixin_base import MixinBase

if TYPE_CHECKING:
    from .bot import Bot


class DatabaseProvider(MixinBase):
    # Initialized during instantiation
    _db: util.db.AsyncDB
    db: util.db.AsyncDB

    def __init__(self: "Bot", **kwargs: Any) -> None:
        # Initialize database
        db_path = self.config["bot"]["db_path"]
        
        if not PLYVEL_AVAILABLE:
            self.log.warning("Using in-memory storage - data will NOT persist across restarts!")
            self._init_db(None)
        else:
            try:
                self._init_db(db_path)
            except plyvel.IOError as e:
                if "Resource temporarily unavailable" in str(e):
                    raise OSError(
                        f"Database '{db_path}' is in use by another process! Make sure no other bot instances are running before starting this again."
                    )
                else:
                    raise
            except plyvel.CorruptionError:
                self.log.warning("Database is corrupted, attempting to repair")
                plyvel.repair_db(db_path)
                self._init_db(db_path)

        self.db = self.get_db("bot")

        # Propagate initialization to other mixins
        super().__init__(**kwargs)

    def _init_db(self: "Bot", db_path: Optional[str]):
        if db_path is None or not PLYVEL_AVAILABLE:
            # In-memory fallback
            self._db = util.db.AsyncDB(None)
        else:
            # Ensure parent directory exists
            db_path_obj = Path(db_path)
            db_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            self._db = util.db.AsyncDB(
                plyvel.DB(str(db_path_obj), create_if_missing=True, paranoid_checks=True)
            )

    def get_db(self: "Bot", prefix: str) -> util.db.AsyncDB:
        return self._db.prefixed_db(prefix + ".")
