from types import TracebackType
from typing import Any, Optional, Tuple, Type, TypeVar, Union, overload
import logging

import msgpack

# Try to import plyvel (LevelDB wrapper)
# Falls back to in-memory dict on Windows where compilation is complex
try:
    import plyvel
    PLYVEL_AVAILABLE = True
except ImportError:
    PLYVEL_AVAILABLE = False
    logging.warning("plyvel not available - using in-memory storage (no persistence)")

from .async_helpers import run_sync

Value = TypeVar("Value")


def _encode(value: Any) -> bytes:
    return msgpack.packb(value, use_bin_type=True)


def _decode(value: bytes) -> Any:
    return msgpack.unpackb(value, raw=False)


class AsyncDB:
    """Simplified asyncio wrapper for plyvel that only supports string keys."""

    _db: Any  # plyvel.DB or dict (fallback)
    prefix: Optional[str]
    _fallback_storage: Optional[dict]

    def __init__(self, db: Any) -> None:
        self._db = db
        
        # In-memory fallback if plyvel unavailable
        if not PLYVEL_AVAILABLE and db is None:
            self._fallback_storage = {}
            self._db = None
        else:
            self._fallback_storage = None

        # Inherit PrefixedDB's prefix attribute if applicable
        self.prefix = getattr(db, "prefix", None) if db else None

    # Core operations
    async def put(self, key: str, value: Any, **kwargs: Any) -> None:
        if self._fallback_storage is not None:
            # In-memory fallback
            full_key = f"{self.prefix or ''}{key}"
            self._fallback_storage[full_key] = value
            return
        
        value = _encode(value)
        return await run_sync(self._db.put, key.encode("utf-8"), value, **kwargs)

    @overload
    async def get(self, key: str, **kwargs: Any) -> Optional[Value]:
        pass

    @overload
    async def get(self, key: str, default: Value, **kwargs: Any) -> Value:
        pass

    async def get(
        self, key: str, default: Optional[Value] = None, **kwargs: Any
    ) -> Optional[Value]:
        if self._fallback_storage is not None:
            # In-memory fallback
            full_key = f"{self.prefix or ''}{key}"
            return self._fallback_storage.get(full_key, default)
        
        value: Optional[bytes] = await run_sync(
            self._db.get, key.encode("utf-8"), **kwargs
        )
        if value is None:
            # We re-implement this to disambiguate types
            return default

        return _decode(value)

    async def delete(self, key: str, **kwargs: Any) -> None:
        if self._fallback_storage is not None:
            # In-memory fallback
            full_key = f"{self.prefix or ''}{key}"
            self._fallback_storage.pop(full_key, None)
            return
        
        return await run_sync(self._db.delete, key.encode("utf-8"), **kwargs)

    async def close(self) -> None:
        if self._fallback_storage is not None:
            return  # Nothing to close for in-memory storage
        return await run_sync(self._db.close)

    # Extensions
    async def snapshot(self) -> "AsyncDB":
        if self._fallback_storage is not None:
            # In-memory fallback - return shallow copy
            new_db = AsyncDB(None)
            new_db._fallback_storage = self._fallback_storage.copy()
            return new_db
        
        ss = await run_sync(self._db.snapshot)
        return AsyncDB(ss)

    def prefixed_db(self, prefix: str) -> "AsyncDB":
        if self._fallback_storage is not None:
            # In-memory fallback - share storage but track prefix
            new_db = AsyncDB(None)
            new_db._fallback_storage = self._fallback_storage
            new_db.prefix = f"{self.prefix or ''}{prefix}"
            return new_db
        
        prefixed_db = self._db.prefixed_db(prefix.encode("utf-8"))
        return AsyncDB(prefixed_db)

    async def inc(self, key: str, delta: int = 1) -> None:
        old_value: int = await self.get(key, 0)
        return await self.put(key, old_value + delta)

    async def dec(self, key: str, delta: int = 1) -> None:
        old_value: int = await self.get(key, 0)
        return await self.put(key, old_value - delta)

    async def has(self, key: str, **kwargs: Any) -> bool:
        if self._fallback_storage is not None:
            # In-memory fallback
            full_key = f"{self.prefix or ''}{key}"
            return full_key in self._fallback_storage
        
        value: Optional[Any] = await run_sync(
            self._db.get, key.encode("utf-8"), **kwargs
        )
        return value is not None

    async def clear(self, **kwargs: Any) -> None:
        if self._fallback_storage is not None:
            # In-memory fallback - clear all keys with our prefix
            prefix = self.prefix or ''
            keys_to_delete = [k for k in self._fallback_storage.keys() if k.startswith(prefix)]
            for k in keys_to_delete:
                del self._fallback_storage[k]
            return
        
        async for key, _ in self:
            await self.delete(key, **kwargs)

    # Context manager support
    async def __aenter__(self) -> "AsyncDB":
        return self

    async def __aexit__(
        self,
        typ: Optional[Type[BaseException]],
        value: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    # Iterator support
    def iterator(
        self, *args: Any, **kwargs: Union[bool, str, bytes]
    ) -> "AsyncDBIterator":
        if self._fallback_storage is not None:
            # In-memory fallback
            prefix = self.prefix or ''
            items = [(k[len(prefix):], v) for k, v in self._fallback_storage.items() if k.startswith(prefix)]
            return AsyncDBIterator(iter(items), is_fallback=True)
        
        for key, value in kwargs.items():
            if isinstance(value, str):
                kwargs[key] = value.encode("utf-8")

        iterator = self._db.iterator(*args, **kwargs)
        return AsyncDBIterator(iterator, is_fallback=False)

    def __aiter__(self) -> "AsyncDBIterator":
        return self.iterator()


# Iterator wrapper
class AsyncDBIterator:
    # noinspection PyProtectedMember
    def __init__(self, iterator: Any, is_fallback: bool = False) -> None:
        self.iterator = iterator
        self.is_fallback = is_fallback

    # Iterator core
    def __aiter__(self) -> "AsyncDBIterator":
        return self

    async def __anext__(self) -> Tuple[str, Any]:
        if self.is_fallback:
            # In-memory fallback
            try:
                key, value = next(self.iterator)
                return key, value
            except StopIteration:
                raise StopAsyncIteration
        
        def _next() -> Tuple[bytes, bytes]:
            try:
                return next(self.iterator)
            except StopIteration:
                raise StopAsyncIteration

        tup = await run_sync(_next)
        return tup[0].decode("utf-8"), _decode(tup[1])

    # Context manager support
    async def __aenter__(self) -> "AsyncDBIterator":
        return self

    async def __aexit__(
        self,
        typ: Optional[Type[BaseException]],
        value: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self.is_fallback:
            return  # Nothing to close for in-memory iterator
        return await run_sync(self.iterator.close)

    # plyvel extensions
    async def prev(self) -> Tuple[bytes, bytes]:
        if self.is_fallback:
            raise NotImplementedError("prev() not supported in fallback mode")
        return await run_sync(self.iterator.prev)

    async def seek_to_start(self) -> None:
        if self.is_fallback:
            raise NotImplementedError("seek_to_start() not supported in fallback mode")
        return await run_sync(self.iterator.seek_to_start)

    async def seek_to_stop(self) -> None:
        if self.is_fallback:
            raise NotImplementedError("seek_to_stop() not supported in fallback mode")
        return await run_sync(self.iterator.seek_to_stop)

    async def seek(self, target: str) -> None:
        if self.is_fallback:
            raise NotImplementedError("seek() not supported in fallback mode")
        return await run_sync(self.iterator.seek, target.encode("utf-8"))
