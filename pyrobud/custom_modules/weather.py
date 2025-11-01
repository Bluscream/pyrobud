import json
from pathlib import PurePosixPath
from typing import IO, Any
from ipaddress import IPv4Address
from aiohttp import ClientSession
from datetime import datetime
from urllib.parse import quote

# import telethon as tg

from .. import command, module, util
from ..custom_classes.IpApi import IPAPIResponse, ipapi_response_from_dict
from ..custom_classes.WeatherApi import WeatherResponse, weather_response_from_dict
from ..custom_classes.GeoLocationApi import GeoLocationSearchResponseElement, geo_location_search_response_from_dict


class WeatherModule(module.Module):
    name = "Weather Module"
    disabled = False

    db: util.db.AsyncDB
    http: ClientSession

    url_api_ip: str = "http://ip-api.com/json/{ip}?fields=66846719"
    url_api_location: str = "https://nominatim.openstreetmap.org/search?q={search}&format=json"
    url_api_weather: str = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum&timezone=Europe%2FBerlin&forecast_days=1"

    async def on_load(self) -> None:
        self.db = self.bot.get_db("weather")
        self.http = ClientSession()

    async def get_ipinfo(self, ip):
        print(f"Getting ip info for {ip}")
        async with self.http.get(self.url_api_ip.format(ip=ip)) as resp:
            text = await resp.text()
            json_data = json.loads(text)
            print(f"Got ip info: {json.dumps(json_data)}")
            data: IPAPIResponse = ipapi_response_from_dict(json_data)
            if not data or data.status != "success": return None
            return data
        
    def format_temperature(self, celsius: float) -> str:
        """Convert temperature to string with Celsius, Fahrenheit and Kelvin values"""
        fahrenheit = (celsius * 9/5) + 32
        kelvin = celsius + 273.15
        return f"{celsius:.1f}°C | {fahrenheit:.1f}°F | {kelvin:.1f}K"

    @command.desc("Sends weather information for yourself or any ip")
    @command.alias("sendweather")
    @command.usage("[ip]", optional=True)
    async def cmd_weather(self, ctx: command.Context) -> str:
        lines = []
        place = "";lat = 0;lon = 0;
        input = ctx.input.strip() or ""
        is_ipv4 = len(input.split('.')) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in input.split('.'))
        is_ipv6 = len(input.split(':')) >= 2 and all(all(c in '0123456789abcdefABCDEF' for c in p) for p in input.split(':'))
        if not input or is_ipv4 or is_ipv6:
            geo = await self.get_ipinfo(input)
            lat = geo.lat; lon = geo.lon;place = f"{geo.city}, {geo.region}, {geo.country}, {geo.continent}"
        else:
            async with self.http.get(self.url_api_location.format(search=quote(input))) as resp:
                text = await resp.text()
                json_data = json.loads(text)
                print(f"Got location info: {json.dumps(json_data)}")
                location: list[GeoLocationSearchResponseElement] = geo_location_search_response_from_dict(json_data)
                if not location or len(location) < 1:
                    print(f"Could not find place \"{input}\"")
                    await ctx.msg.delete()
                    return
                lat = location[0].lat; lon = location[0].lon;place = location[0].name
        
        if not lat or not lon:
            print(f"Unable to get location info for \"{input}\"!")
            await ctx.msg.delete()
            return
        async with self.http.get(self.url_api_weather.format(lat=lat,lon=lon)) as resp:
            text = await resp.text()
            json_data = json.loads(text)
            print(f"Got weather info: {json.dumps(json_data)}")
            weather: WeatherResponse = weather_response_from_dict(json_data)
            if not input: lines.append(f"**My Current weather:**")
            else: lines.append(f"**Current weather in {place}:**")
            dt = datetime.fromisoformat(weather.current.time)
            formatted_time = dt.strftime("%d.%m.%Y %H:%M:%S")
            lines.append(f"Time: `{formatted_time}` (`{weather.timezone}`)")
            lines.append(f"Temperature: `{self.format_temperature(weather.current.temperature_2_m)}`")
            lines.append(f"Feels like: `{self.format_temperature(weather.current.apparent_temperature)}`")
            if weather.current.precipitation > 0: lines.append(f"Precipitation: `{weather.current.precipitation}{weather.current_units.precipitation}`")
            if weather.current.rain > 0: lines.append(f"Rain: `{weather.current.rain}{weather.current_units.rain}`")
            if weather.current.snowfall > 0: lines.append(f"Snow: `{weather.current.snowfall}{weather.current_units.snowfall}`")
            if weather.daily.precipitation_sum[0] > 0: lines.append(f"Daily precipitation sum: `{weather.daily.precipitation_sum[0]}{weather.daily_units.precipitation_sum}`")
            lines.append(f"Wind: `{weather.current.wind_speed_10_m}{weather.current_units.wind_speed_10_m}` (`{weather.current.wind_direction_10_m}{weather.current_units.wind_direction_10_m}`)")

        return '\n'.join(lines)
