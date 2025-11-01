from pyrobud import command, module
import re, json, http.client

class myTeamspeak(module.Module):
    name = "myTeamspeak"
    disabled = False
    myts_login = {
        'email': 'admin@timo.de.vc',
        'password': 'dhuQdXzeAGKKSBVMH4YQ5voboNwcTdS4M8BzqAPuBk7u4QrWxnfaKTSPjLY4KwyH',
    }
    
    def redeem_ts_badge(self, code: str):
        print(f"Redeeming myTS badge: {code}")
        conn = http.client.HTTPSConnection('www.myteamspeak.com')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': '',
            'Content-Type': 'application/json',
            'Origin': 'https://www.myteamspeak.com',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.myteamspeak.com/api/login',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers',
        }

        conn.request(
            'POST',
            '/api/login',
            json.dumps(self.myts_login),
            headers
        )
        response = conn.getresponse()
        text = response.read().decode("utf-8")
        data = json.loads(text)
        print(data)
        sessionId = data["data"]["sessionId"]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': '',
            'Authorization': f'Bearer {sessionId}',
            'Content-type': 'application/json',
            'Content-Length': '0',
            'Origin': 'https://www.myteamspeak.com',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': f'https://www.myteamspeak.com/api/badges/{code}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        conn.request('POST', f"/api/badges/{code}", headers=headers)
        response = conn.getresponse()
        return response
    
    @command.desc("Redeem myts badge")
    @command.alias("tsredeem")
    @command.usage("code", optional=False, reply=True)
    async def cmd_redeem(self, ctx: command.Context) -> str:
        response = None
        data = {}
        try:
            await ctx.respond("Processing...")
            if not ctx.input: return "No input provided :("
            codes = re.findall(r"[A-Z0-9]{5,30}", ctx.input, re.MULTILINE)
            if len(codes) > 1:
                codestr = '\n'.join([f'`.redeem {m.group()}`' for m in codes])
                return f"Found too many possible codes:\n\n{codestr}"
            code = codes[0]
            response = self.redeem_ts_badge(code)
        
            text = response.read().decode("utf-8")
            data = json.loads(text)
            print(data)
            if data['code'] != 200:
                raise Exception("")
            return f"Successfully redeemed `{code}`: {data['message']}"
        except Exception as ex:
            msg = f"Failed to redeem `{code}`\n\n``` {getattr(ex, 'message', str(ex))}"
            if response is not None: msg += f" {response.status}"
            for k in ['message','error']:
                if k in data: msg += f" - {data[k]} "
            return f"{msg}\n```"
        

    

