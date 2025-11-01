from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from datetime import datetime


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for _f in fs:
        try:
            return _f(x)
        except Exception as ex:
            print(ex)
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    assert isinstance(x, str)
    return datetime.fromisoformat(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Current:
    time: Optional[str] = None
    interval: Optional[int] = None
    temperature_2_m: Optional[float] = None
    relative_humidity_2_m: Optional[int] = None
    apparent_temperature: Optional[float] = None
    is_day: Optional[int] = None
    precipitation: Optional[float] = None
    rain: Optional[float] = None
    showers: Optional[float] = None
    snowfall: Optional[float] = None
    weather_code: Optional[int] = None
    cloud_cover: Optional[int] = None
    pressure_msl: Optional[float] = None
    surface_pressure: Optional[float] = None
    wind_speed_10_m: Optional[float] = None
    wind_direction_10_m: Optional[int] = None
    wind_gusts_10_m: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Current':
        assert isinstance(obj, dict)
        time = from_union([from_str, from_none], obj.get("time"))
        interval = from_union([from_int, from_none], obj.get("interval"))
        temperature_2_m = from_union([from_float, from_none], obj.get("temperature_2m"))
        relative_humidity_2_m = from_union([from_int, from_none], obj.get("relative_humidity_2m"))
        apparent_temperature = from_union([from_float, from_none], obj.get("apparent_temperature"))
        is_day = from_union([from_int, from_none], obj.get("is_day"))
        precipitation = from_union([from_float, from_none], obj.get("precipitation"))
        rain = from_union([from_float, from_none], obj.get("rain"))
        showers = from_union([from_float, from_none], obj.get("showers"))
        snowfall = from_union([from_float, from_none], obj.get("snowfall"))
        weather_code = from_union([from_int, from_none], obj.get("weather_code"))
        cloud_cover = from_union([from_int, from_none], obj.get("cloud_cover"))
        pressure_msl = from_union([from_float, from_none], obj.get("pressure_msl"))
        surface_pressure = from_union([from_float, from_none], obj.get("surface_pressure"))
        wind_speed_10_m = from_union([from_float, from_none], obj.get("wind_speed_10m"))
        wind_direction_10_m = from_union([from_int, from_none], obj.get("wind_direction_10m"))
        wind_gusts_10_m = from_union([from_float, from_none], obj.get("wind_gusts_10m"))
        return Current(time, interval, temperature_2_m, relative_humidity_2_m, apparent_temperature, is_day, precipitation, rain, showers, snowfall, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10_m, wind_direction_10_m, wind_gusts_10_m)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.time is not None:
            result["time"] = from_union([from_str, from_none], self.time)
        if self.interval is not None:
            result["interval"] = from_union([from_int, from_none], self.interval)
        if self.temperature_2_m is not None:
            result["temperature_2m"] = from_union([to_float, from_none], self.temperature_2_m)
        if self.relative_humidity_2_m is not None:
            result["relative_humidity_2m"] = from_union([from_int, from_none], self.relative_humidity_2_m)
        if self.apparent_temperature is not None:
            result["apparent_temperature"] = from_union([to_float, from_none], self.apparent_temperature)
        if self.is_day is not None:
            result["is_day"] = from_union([from_int, from_none], self.is_day)
        if self.precipitation is not None:
            result["precipitation"] = from_union([from_int, from_none], self.precipitation)
        if self.rain is not None:
            result["rain"] = from_union([from_int, from_none], self.rain)
        if self.showers is not None:
            result["showers"] = from_union([from_int, from_none], self.showers)
        if self.snowfall is not None:
            result["snowfall"] = from_union([from_int, from_none], self.snowfall)
        if self.weather_code is not None:
            result["weather_code"] = from_union([from_int, from_none], self.weather_code)
        if self.cloud_cover is not None:
            result["cloud_cover"] = from_union([from_int, from_none], self.cloud_cover)
        if self.pressure_msl is not None:
            result["pressure_msl"] = from_union([to_float, from_none], self.pressure_msl)
        if self.surface_pressure is not None:
            result["surface_pressure"] = from_union([to_float, from_none], self.surface_pressure)
        if self.wind_speed_10_m is not None:
            result["wind_speed_10m"] = from_union([to_float, from_none], self.wind_speed_10_m)
        if self.wind_direction_10_m is not None:
            result["wind_direction_10m"] = from_union([from_int, from_none], self.wind_direction_10_m)
        if self.wind_gusts_10_m is not None:
            result["wind_gusts_10m"] = from_union([to_float, from_none], self.wind_gusts_10_m)
        return result


@dataclass
class CurrentUnits:
    time: Optional[str] = None
    interval: Optional[str] = None
    temperature_2_m: Optional[str] = None
    relative_humidity_2_m: Optional[str] = None
    apparent_temperature: Optional[str] = None
    is_day: Optional[str] = None
    precipitation: Optional[str] = None
    rain: Optional[str] = None
    showers: Optional[str] = None
    snowfall: Optional[str] = None
    weather_code: Optional[str] = None
    cloud_cover: Optional[str] = None
    pressure_msl: Optional[str] = None
    surface_pressure: Optional[str] = None
    wind_speed_10_m: Optional[str] = None
    wind_direction_10_m: Optional[str] = None
    wind_gusts_10_m: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CurrentUnits':
        assert isinstance(obj, dict)
        time = from_union([from_str, from_none], obj.get("time"))
        interval = from_union([from_str, from_none], obj.get("interval"))
        temperature_2_m = from_union([from_str, from_none], obj.get("temperature_2m"))
        relative_humidity_2_m = from_union([from_str, from_none], obj.get("relative_humidity_2m"))
        apparent_temperature = from_union([from_str, from_none], obj.get("apparent_temperature"))
        is_day = from_union([from_str, from_none], obj.get("is_day"))
        precipitation = from_union([from_str, from_none], obj.get("precipitation"))
        rain = from_union([from_str, from_none], obj.get("rain"))
        showers = from_union([from_str, from_none], obj.get("showers"))
        snowfall = from_union([from_str, from_none], obj.get("snowfall"))
        weather_code = from_union([from_str, from_none], obj.get("weather_code"))
        cloud_cover = from_union([from_str, from_none], obj.get("cloud_cover"))
        pressure_msl = from_union([from_str, from_none], obj.get("pressure_msl"))
        surface_pressure = from_union([from_str, from_none], obj.get("surface_pressure"))
        wind_speed_10_m = from_union([from_str, from_none], obj.get("wind_speed_10m"))
        wind_direction_10_m = from_union([from_str, from_none], obj.get("wind_direction_10m"))
        wind_gusts_10_m = from_union([from_str, from_none], obj.get("wind_gusts_10m"))
        return CurrentUnits(time, interval, temperature_2_m, relative_humidity_2_m, apparent_temperature, is_day, precipitation, rain, showers, snowfall, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10_m, wind_direction_10_m, wind_gusts_10_m)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.time is not None:
            result["time"] = from_union([from_str, from_none], self.time)
        if self.interval is not None:
            result["interval"] = from_union([from_str, from_none], self.interval)
        if self.temperature_2_m is not None:
            result["temperature_2m"] = from_union([from_str, from_none], self.temperature_2_m)
        if self.relative_humidity_2_m is not None:
            result["relative_humidity_2m"] = from_union([from_str, from_none], self.relative_humidity_2_m)
        if self.apparent_temperature is not None:
            result["apparent_temperature"] = from_union([from_str, from_none], self.apparent_temperature)
        if self.is_day is not None:
            result["is_day"] = from_union([from_str, from_none], self.is_day)
        if self.precipitation is not None:
            result["precipitation"] = from_union([from_str, from_none], self.precipitation)
        if self.rain is not None:
            result["rain"] = from_union([from_str, from_none], self.rain)
        if self.showers is not None:
            result["showers"] = from_union([from_str, from_none], self.showers)
        if self.snowfall is not None:
            result["snowfall"] = from_union([from_str, from_none], self.snowfall)
        if self.weather_code is not None:
            result["weather_code"] = from_union([from_str, from_none], self.weather_code)
        if self.cloud_cover is not None:
            result["cloud_cover"] = from_union([from_str, from_none], self.cloud_cover)
        if self.pressure_msl is not None:
            result["pressure_msl"] = from_union([from_str, from_none], self.pressure_msl)
        if self.surface_pressure is not None:
            result["surface_pressure"] = from_union([from_str, from_none], self.surface_pressure)
        if self.wind_speed_10_m is not None:
            result["wind_speed_10m"] = from_union([from_str, from_none], self.wind_speed_10_m)
        if self.wind_direction_10_m is not None:
            result["wind_direction_10m"] = from_union([from_str, from_none], self.wind_direction_10_m)
        if self.wind_gusts_10_m is not None:
            result["wind_gusts_10m"] = from_union([from_str, from_none], self.wind_gusts_10_m)
        return result


@dataclass
class Daily:
    time: Optional[List[datetime]] = None
    weather_code: Optional[List[int]] = None
    temperature_2_m_max: Optional[List[float]] = None
    temperature_2_m_min: Optional[List[float]] = None
    sunrise: Optional[List[str]] = None
    sunset: Optional[List[str]] = None
    precipitation_sum: Optional[List[float]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Daily':
        assert isinstance(obj, dict)
        time = from_union([lambda x: from_list(from_datetime, x), from_none], obj.get("time"))
        weather_code = from_union([lambda x: from_list(from_int, x), from_none], obj.get("weather_code"))
        temperature_2_m_max = from_union([lambda x: from_list(from_float, x), from_none], obj.get("temperature_2m_max"))
        temperature_2_m_min = from_union([lambda x: from_list(from_float, x), from_none], obj.get("temperature_2m_min"))
        sunrise = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sunrise"))
        sunset = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sunset"))
        precipitation_sum = from_union([lambda x: from_list(from_float, x), from_none], obj.get("precipitation_sum"))
        return Daily(time, weather_code, temperature_2_m_max, temperature_2_m_min, sunrise, sunset, precipitation_sum)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.time is not None:
            result["time"] = from_union([lambda x: from_list(lambda x: x.isoformat(), x), from_none], self.time)
        if self.weather_code is not None:
            result["weather_code"] = from_union([lambda x: from_list(from_int, x), from_none], self.weather_code)
        if self.temperature_2_m_max is not None:
            result["temperature_2m_max"] = from_union([lambda x: from_list(to_float, x), from_none], self.temperature_2_m_max)
        if self.temperature_2_m_min is not None:
            result["temperature_2m_min"] = from_union([lambda x: from_list(to_float, x), from_none], self.temperature_2_m_min)
        if self.sunrise is not None:
            result["sunrise"] = from_union([lambda x: from_list(from_str, x), from_none], self.sunrise)
        if self.sunset is not None:
            result["sunset"] = from_union([lambda x: from_list(from_str, x), from_none], self.sunset)
        if self.precipitation_sum is not None:
            result["precipitation_sum"] = from_union([lambda x: from_list(to_float, x), from_none], self.precipitation_sum)
        return result


@dataclass
class DailyUnits:
    time: Optional[str] = None
    weather_code: Optional[str] = None
    temperature_2_m_max: Optional[str] = None
    temperature_2_m_min: Optional[str] = None
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    precipitation_sum: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DailyUnits':
        assert isinstance(obj, dict)
        time = from_union([from_str, from_none], obj.get("time"))
        weather_code = from_union([from_str, from_none], obj.get("weather_code"))
        temperature_2_m_max = from_union([from_str, from_none], obj.get("temperature_2m_max"))
        temperature_2_m_min = from_union([from_str, from_none], obj.get("temperature_2m_min"))
        sunrise = from_union([from_str, from_none], obj.get("sunrise"))
        sunset = from_union([from_str, from_none], obj.get("sunset"))
        precipitation_sum = from_union([from_str, from_none], obj.get("precipitation_sum"))
        return DailyUnits(time, weather_code, temperature_2_m_max, temperature_2_m_min, sunrise, sunset, precipitation_sum)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.time is not None:
            result["time"] = from_union([from_str, from_none], self.time)
        if self.weather_code is not None:
            result["weather_code"] = from_union([from_str, from_none], self.weather_code)
        if self.temperature_2_m_max is not None:
            result["temperature_2m_max"] = from_union([from_str, from_none], self.temperature_2_m_max)
        if self.temperature_2_m_min is not None:
            result["temperature_2m_min"] = from_union([from_str, from_none], self.temperature_2_m_min)
        if self.sunrise is not None:
            result["sunrise"] = from_union([from_str, from_none], self.sunrise)
        if self.sunset is not None:
            result["sunset"] = from_union([from_str, from_none], self.sunset)
        if self.precipitation_sum is not None:
            result["precipitation_sum"] = from_union([from_str, from_none], self.precipitation_sum)
        return result


@dataclass
class WeatherResponse:
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    generationtime_ms: Optional[float] = None
    utc_offset_seconds: Optional[int] = None
    timezone: Optional[str] = None
    timezone_abbreviation: Optional[str] = None
    elevation: Optional[int] = None
    current_units: Optional[CurrentUnits] = None
    current: Optional[Current] = None
    daily_units: Optional[DailyUnits] = None
    daily: Optional[Daily] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherResponse':
        assert isinstance(obj, dict)
        latitude = from_union([from_float, from_none], obj.get("latitude"))
        longitude = from_union([from_float, from_none], obj.get("longitude"))
        generationtime_ms = from_union([from_float, from_none], obj.get("generationtime_ms"))
        utc_offset_seconds = from_union([from_int, from_none], obj.get("utc_offset_seconds"))
        timezone = from_union([from_str, from_none], obj.get("timezone"))
        timezone_abbreviation = from_union([from_str, from_none], obj.get("timezone_abbreviation"))
        elevation = 0 #  = from_union([from_int, from_none], obj.get("elevation"))
        current_units = from_union([CurrentUnits.from_dict, from_none], obj.get("current_units"))
        current = from_union([Current.from_dict, from_none], obj.get("current"))
        daily_units = from_union([DailyUnits.from_dict, from_none], obj.get("daily_units"))
        daily = from_union([Daily.from_dict, from_none], obj.get("daily"))
        return WeatherResponse(latitude, longitude, generationtime_ms, utc_offset_seconds, timezone, timezone_abbreviation, elevation, current_units, current, daily_units, daily)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.latitude is not None:
            result["latitude"] = from_union([to_float, from_none], self.latitude)
        if self.longitude is not None:
            result["longitude"] = from_union([to_float, from_none], self.longitude)
        if self.generationtime_ms is not None:
            result["generationtime_ms"] = from_union([to_float, from_none], self.generationtime_ms)
        if self.utc_offset_seconds is not None:
            result["utc_offset_seconds"] = from_union([from_int, from_none], self.utc_offset_seconds)
        if self.timezone is not None:
            result["timezone"] = from_union([from_str, from_none], self.timezone)
        if self.timezone_abbreviation is not None:
            result["timezone_abbreviation"] = from_union([from_str, from_none], self.timezone_abbreviation)
        if self.elevation is not None:
            result["elevation"] = from_union([from_int, from_none], self.elevation)
        if self.current_units is not None:
            result["current_units"] = from_union([lambda x: to_class(CurrentUnits, x), from_none], self.current_units)
        if self.current is not None:
            result["current"] = from_union([lambda x: to_class(Current, x), from_none], self.current)
        if self.daily_units is not None:
            result["daily_units"] = from_union([lambda x: to_class(DailyUnits, x), from_none], self.daily_units)
        if self.daily is not None:
            result["daily"] = from_union([lambda x: to_class(Daily, x), from_none], self.daily)
        return result


def weather_response_from_dict(s: Any) -> WeatherResponse:
    return WeatherResponse.from_dict(s)


def weather_response_to_dict(x: WeatherResponse) -> Any:
    return to_class(WeatherResponse, x)
