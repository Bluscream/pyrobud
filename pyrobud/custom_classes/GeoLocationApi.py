from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class GeoLocationSearchResponseElement:
    place_id: Optional[int] = None
    licence: Optional[str] = None
    osm_type: Optional[str] = None
    osm_id: Optional[int] = None
    lat: Optional[str] = None
    lon: Optional[str] = None
    geo_location_search_response_class: Optional[str] = None
    type: Optional[str] = None
    place_rank: Optional[int] = None
    importance: Optional[float] = None
    addresstype: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    boundingbox: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GeoLocationSearchResponseElement':
        assert isinstance(obj, dict)
        place_id = from_union([from_int, from_none], obj.get("place_id"))
        licence = from_union([from_str, from_none], obj.get("licence"))
        osm_type = from_union([from_str, from_none], obj.get("osm_type"))
        osm_id = from_union([from_int, from_none], obj.get("osm_id"))
        lat = from_union([from_str, from_none], obj.get("lat"))
        lon = from_union([from_str, from_none], obj.get("lon"))
        geo_location_search_response_class = from_union([from_str, from_none], obj.get("class"))
        type = from_union([from_str, from_none], obj.get("type"))
        place_rank = from_union([from_int, from_none], obj.get("place_rank"))
        importance = from_union([from_float, from_none], obj.get("importance"))
        addresstype = from_union([from_str, from_none], obj.get("addresstype"))
        name = from_union([from_str, from_none], obj.get("name"))
        display_name = from_union([from_str, from_none], obj.get("display_name"))
        boundingbox = from_union([lambda x: from_list(from_str, x), from_none], obj.get("boundingbox"))
        return GeoLocationSearchResponseElement(place_id, licence, osm_type, osm_id, lat, lon, geo_location_search_response_class, type, place_rank, importance, addresstype, name, display_name, boundingbox)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.place_id is not None:
            result["place_id"] = from_union([from_int, from_none], self.place_id)
        if self.licence is not None:
            result["licence"] = from_union([from_str, from_none], self.licence)
        if self.osm_type is not None:
            result["osm_type"] = from_union([from_str, from_none], self.osm_type)
        if self.osm_id is not None:
            result["osm_id"] = from_union([from_int, from_none], self.osm_id)
        if self.lat is not None:
            result["lat"] = from_union([from_str, from_none], self.lat)
        if self.lon is not None:
            result["lon"] = from_union([from_str, from_none], self.lon)
        if self.geo_location_search_response_class is not None:
            result["class"] = from_union([from_str, from_none], self.geo_location_search_response_class)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.place_rank is not None:
            result["place_rank"] = from_union([from_int, from_none], self.place_rank)
        if self.importance is not None:
            result["importance"] = from_union([to_float, from_none], self.importance)
        if self.addresstype is not None:
            result["addresstype"] = from_union([from_str, from_none], self.addresstype)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.display_name is not None:
            result["display_name"] = from_union([from_str, from_none], self.display_name)
        if self.boundingbox is not None:
            result["boundingbox"] = from_union([lambda x: from_list(from_str, x), from_none], self.boundingbox)
        return result


def geo_location_search_response_from_dict(s: Any) -> List[GeoLocationSearchResponseElement]:
    return from_list(GeoLocationSearchResponseElement.from_dict, s)


def geo_location_search_response_to_dict(x: List[GeoLocationSearchResponseElement]) -> Any:
    return from_list(lambda x: to_class(GeoLocationSearchResponseElement, x), x)
