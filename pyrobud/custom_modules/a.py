
from .. import module
from ..custom_classes.DataCenter import DataCenters


class StartupModule(module.Module):
    name = "Startup"
    disabled = False

    async def on_load(self) -> None:
        print("Initializing bot.dc")
        self.bot.dc = DataCenters()
        await self.bot.dc.update()

        for id, dc in self.bot.dc.dcs.items():
            print(f"DC {id}: {dc.geo.continent} ({dc.endpoints})")