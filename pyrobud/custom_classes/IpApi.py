from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class IPAPIResponse:
    query: Optional[str] = None
    status: Optional[str] = None
    continent: Optional[str] = None
    continent_code: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    region_name: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    zip: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    timezone: Optional[str] = None
    offset: Optional[int] = None
    currency: Optional[str] = None
    isp: Optional[str] = None
    org: Optional[str] = None
    ip_api_response_as: Optional[str] = None
    asname: Optional[str] = None
    mobile: Optional[bool] = None
    proxy: Optional[bool] = None
    hosting: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'IPAPIResponse':
        assert isinstance(obj, dict)
        query = from_union([from_str, from_none], obj.get("query"))
        status = from_union([from_str, from_none], obj.get("status"))
        continent = from_union([from_str, from_none], obj.get("continent"))
        continent_code = from_union([from_str, from_none], obj.get("continentCode"))
        country = from_union([from_str, from_none], obj.get("country"))
        country_code = from_union([from_str, from_none], obj.get("countryCode"))
        region = from_union([from_str, from_none], obj.get("region"))
        region_name = from_union([from_str, from_none], obj.get("regionName"))
        city = from_union([from_str, from_none], obj.get("city"))
        district = from_union([from_str, from_none], obj.get("district"))
        zip = from_union([from_none, from_str, lambda x: int(from_str(x))], obj.get("zip"))
        lat = from_union([from_float, from_none], obj.get("lat"))
        lon = from_union([from_float, from_none], obj.get("lon"))
        timezone = from_union([from_str, from_none], obj.get("timezone"))
        offset = from_union([from_int, from_none], obj.get("offset"))
        currency = from_union([from_str, from_none], obj.get("currency"))
        isp = from_union([from_str, from_none], obj.get("isp"))
        org = from_union([from_str, from_none], obj.get("org"))
        ip_api_response_as = from_union([from_str, from_none], obj.get("as"))
        asname = from_union([from_str, from_none], obj.get("asname"))
        mobile = from_union([from_bool, from_none], obj.get("mobile"))
        proxy = from_union([from_bool, from_none], obj.get("proxy"))
        hosting = from_union([from_bool, from_none], obj.get("hosting"))
        return IPAPIResponse(query, status, continent, continent_code, country, country_code, region, region_name, city, district, zip, lat, lon, timezone, offset, currency, isp, org, ip_api_response_as, asname, mobile, proxy, hosting)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.query is not None:
            result["query"] = from_union([from_str, from_none], self.query)
        if self.status is not None:
            result["status"] = from_union([from_str, from_none], self.status)
        if self.continent is not None:
            result["continent"] = from_union([from_str, from_none], self.continent)
        if self.continent_code is not None:
            result["continentCode"] = from_union([from_str, from_none], self.continent_code)
        if self.country is not None:
            result["country"] = from_union([from_str, from_none], self.country)
        if self.country_code is not None:
            result["countryCode"] = from_union([from_str, from_none], self.country_code)
        if self.region is not None:
            result["region"] = from_union([from_str, from_none], self.region)
        if self.region_name is not None:
            result["regionName"] = from_union([from_str, from_none], self.region_name)
        if self.city is not None:
            result["city"] = from_union([from_str, from_none], self.city)
        if self.district is not None:
            result["district"] = from_union([from_str, from_none], self.district)
        if self.zip is not None:
            result["zip"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.zip)
        if self.lat is not None:
            result["lat"] = from_union([to_float, from_none], self.lat)
        if self.lon is not None:
            result["lon"] = from_union([to_float, from_none], self.lon)
        if self.timezone is not None:
            result["timezone"] = from_union([from_str, from_none], self.timezone)
        if self.offset is not None:
            result["offset"] = from_union([from_int, from_none], self.offset)
        if self.currency is not None:
            result["currency"] = from_union([from_str, from_none], self.currency)
        if self.isp is not None:
            result["isp"] = from_union([from_str, from_none], self.isp)
        if self.org is not None:
            result["org"] = from_union([from_str, from_none], self.org)
        if self.ip_api_response_as is not None:
            result["as"] = from_union([from_str, from_none], self.ip_api_response_as)
        if self.asname is not None:
            result["asname"] = from_union([from_str, from_none], self.asname)
        if self.mobile is not None:
            result["mobile"] = from_union([from_bool, from_none], self.mobile)
        if self.proxy is not None:
            result["proxy"] = from_union([from_bool, from_none], self.proxy)
        if self.hosting is not None:
            result["hosting"] = from_union([from_bool, from_none], self.hosting)
        return result


def ipapi_response_from_dict(s: Any) -> IPAPIResponse:
    return IPAPIResponse.from_dict(s)


def ipapi_response_to_dict(x: IPAPIResponse) -> Any:
    return to_class(IPAPIResponse, x)
