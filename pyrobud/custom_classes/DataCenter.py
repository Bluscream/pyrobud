import asyncio, json
from ipaddress import IPv4Address
from aiohttp import ClientSession

from ..custom_classes.IpApi import IPAPIResponse, ipapi_response_from_dict

class DataCenter(object):
    id: int
    code: str = "???"

    geo: IPAPIResponse = None

    endpoints: set[tuple[IPv4Address, int]] = set()

    ping: int = -1
    status: int = -1
    last_down: int = -1
    last_lag: int = -1

    def __init__(self, id, code) -> None:
        self.id = id; self.code = code;

class DataCenters(object):
    ipapi_url: str = "http://ip-api.com/json/{ip}?fields=66846719"
    list_url: str = "https://core.telegram.org/getProxyConfig"
    update_url: str = "https://raw.githubusercontent.com/OctoGramApp/assets/master/DCStatus/dc_status.json"

    http: ClientSession
    dcs: dict[int,DataCenter] = dict()

    def __init__(self) -> None:
        self.http = ClientSession()
        pass # await self.update()
        # self.dcs[1] = DataCenter(1, "MIA", "Miami FL", "USA")

    def add_or_update(self, id, code:str=None, geo:IPAPIResponse=None, ip:IPv4Address=None, port:int=None, ping:int=None, status:int=None, last_down:int=None, last_lag:int=None) -> DataCenter:
        id = int(str(id).replace('-',''))
        if id not in self.dcs: self.dcs[id] = DataCenter(id, code)
        dc = self.dcs[id]
        if code: dc.code=code;
        if geo: dc.geo=geo;
        if ping: dc.ping=ping;
        if status: dc.status=status;
        if last_down: dc.last_down=last_down;
        if last_lag: dc.last_lag=last_lag;
        if ip: dc.endpoints.add((ip, port or 8888))
        return dc

    async def update(self):
        async with self.http.get(self.list_url) as resp:
            dc_list: list[str] = (await resp.text()).split("\n")
            for line in dc_list:
                print(line)
                if not line.startswith("proxy_for "): continue
                l = line.split(" ")
                print(f"l:{l}")
                i = l[2].split(":")
                print(f"i:{i}")
                print(f"id:{l[1]}")
                print(f"ip:{IPv4Address(i[0])}")
                print(f"port:{int(i[1].replace(';',''))}")
                self.add_or_update(id=l[1],ip=IPv4Address(i[0]),port=int(i[1].replace(';','')))
        print(f"Got list of {len(self.dcs)} DataCenters")

        for dc in self.dcs.values():
            for endpoint in dc.endpoints:
                if dc.geo: continue
                ip = endpoint[0]
                print(f"Getting ip info for DC{dc.id}, Server {ip}")
                async with self.http.get(self.ipapi_url.format(ip=ip)) as resp:
                    apiresp: IPAPIResponse = ipapi_response_from_dict(json.loads(await resp.text()))
                    if not apiresp or apiresp.status != "success": continue
                    dc.geo = apiresp
                    print(f"Got ipapi response for dc {dc.id}")

        async with self.http.get(self.update_url) as resp:
            data: dict = json.loads(await resp.text())
            for _dc in data["status"]:

                dc = self.add_or_update(id=_dc["dc_id"])
                if dc:
                    dc.ping = _dc["ping"]
                    dc.status = _dc["dc_status"]
                    dc.last_down = _dc["last_down"]
                    dc.last_lag = _dc["last_lag"]
        
        print(f"Updated {len(self.dcs)} DataCenters")

        for id, dc in self.dcs.items():
            print(f"DC {id}: {dc.geo.continent} ({dc.endpoints})")