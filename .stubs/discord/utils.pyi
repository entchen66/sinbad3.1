import datetime
import array
import asyncio
from aiohttp.web import Request
from .permissions import Permissions
from .guild import Guild
from .invite import Invite
from .object import Object

from typing import (
    Any,
    Optional,
    Union,
    List,
    Set,
    Iterable,
    TypeVar,
    Type,
    Callable,
    Coroutine,
    Generic,
    Pattern,
    Sequence,
    overload,
)
from typing_extensions import Final

_T = TypeVar("_T")
_U_co = TypeVar("_U_co", covariant=True)

_FuncType = Callable[..., Any]
_F = TypeVar("_F", bound=_FuncType)

DISCORD_EPOCH: Final[int] = ...

class cached_property(Generic[_T, _U_co]):
    def __init__(self, function: Callable[[_T], _U_co]) -> None: ...
    @overload
    def __get__(self, instance: _T, owner: Type[_T]) -> _U_co: ...
    @overload
    def __get__(
        self, instance: None, owner: Type[_T]
    ) -> cached_property[_T, _U_co]: ...

class CachedSlotProperty(Generic[_T, _U_co]):
    def __init__(self, name: str, function: Callable[[_T], _U_co]) -> None: ...
    @overload
    def __get__(self, instance: _T, owner: Type[_T]) -> _U_co: ...
    @overload
    def __get__(
        self, instance: None, owner: Type[_T]
    ) -> CachedSlotProperty[_T, _U_co]: ...

def cached_slot_property(
    name: str,
) -> Callable[[Callable[[_T], _U_co]], CachedSlotProperty[_T, _U_co]]: ...

class SequenceProxy(Sequence[_T]):
    def __init__(self, sequence: Sequence[_T]) -> None: ...
    @overload
    def __getitem__(self, i: int) -> _T: ...
    @overload
    def __getitem__(self, s: slice) -> Sequence[_T]: ...
    def __len__(self) -> int: ...

class SnowflakeList(array.array):
    def has(self, element: int) -> bool: ...

def parse_time(timestamp: Optional[str]) -> Optional[datetime.datetime]: ...
def deprecated(instead: Optional[str] = ...) -> Callable[[_F], _F]: ...
def oauth_url(
    client_id: str,
    permissions: Optional[Permissions] = ...,
    guild: Optional[Guild] = ...,
    redirect_uri: Optional[str] = ...,
) -> str: ...
def snowflake_time(id: int) -> datetime.datetime: ...
def time_snowflake(datetime_obj: datetime.datetime, high: bool = ...) -> int: ...
def find(predicate: Callable[[_T], bool], seq: Iterable[_T]) -> Optional[_T]: ...
def get(iterable: Iterable[_T], **attrs: Any) -> Optional[_T]: ...
def _unique(iterable: Iterable[_T]) -> List[_T]: ...
def _get_as_snowflake(data: Any, key: str) -> Optional[int]: ...
def _get_mime_type_for_image(data: Union[bytes, bytearray]) -> str: ...
def _bytes_to_base64_data(data: Union[bytes, bytearray]) -> str: ...
def to_json(obj: Any) -> str: ...
def _parse_ratelimit_header(request: Request, *, use_clock: bool = ...) -> float: ...
async def maybe_coroutine(
    f: Callable[..., Union[_T, Coroutine[Any, Any, _T]]], *args: Any, **kwargs: Any
) -> _T: ...
async def async_all(
    gen: Iterable[Union[Any, Coroutine[Any, Any, Any]]],
    *,
    check: Callable[[Any], bool] = ...,
) -> bool: ...
async def sane_wait_for(
    futures: List[asyncio.Future[_T]],
    *,
    timeout: float,
    loop: asyncio.AbstractEventLoop,
) -> Set[asyncio.Future[_T]]: ...
def valid_icon_size(size: int) -> bool: ...
def _string_width(string: str, *, _IS_ASCII: Pattern[str] = ...) -> int: ...
def resolve_invite(invite: Union[Invite, Object, str]) -> str: ...
def escape_markdown(
    text: str, *, as_needed: bool = ..., ignore_links: bool = ...
) -> str: ...
def escape_mentions(text: str) -> str: ...