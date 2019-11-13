import os
import psutil
import subprocess
import sys
import telethon as tg
import utils
from datetime import datetime

import speedtest

from pyrobud import command, module


class SystemModule(module.Module):
    name = "System"

    async def run_process(self, command, **kwargs):
        def _run_process():
            return subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, **kwargs
            )

        return await utils.run_sync(_run_process)

    async def run_process_sudo(self, command, **kwargs):
        def _run_process():
            sudo_password = self.bot.config["shell"]["sudo_pw"]
            sudo_password = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return subprocess.run(
                ['sudo', '-S'] + command, stdin=sudo_password.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, **kwargs
            )

        return await utils.run_sync(_run_process)

    @command.desc("Restart pyrobud")
    async def cmd_restart(self, msg: tg.events.newmessage, confirm: bool = False):
        """Restarts the current program, with file objects and descriptors
           cleanup
        """
        if not confirm: return
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        await msg.result(f"[{timestamp}] ⚠ Restarting pyrobud...")
        try:
            p = psutil.Process(os.getpid())
            for handler in p.open_files() + p.connections(): os.close(handler.fd)
        except Exception as ex: return ex
        python = sys.executable
        return os.execl(python, python, *sys.argv)
        # cmd1 = subprocess.Popen(['echo', self.bot.config["shell"]["sudo_pw"]], stdout=subprocess.PIPE)
        # subprocess.Popen(['sudo', '-S', "service", "selfbot-tguser", "restart"], stdin=cmd1.stdout)


    @command.desc("Run a snippet in a shell")
    @command.alias("sh")
    async def cmd_shell(self, msg, parsed_snip):
        if not parsed_snip:
            return "__Provide a snippet to run in shell.__"

        await msg.result("Running snippet...")
        before = utils.time.usec()

        try:
            proc = await self.run_process(parsed_snip, shell=True, timeout=120)
        except subprocess.TimeoutExpired:
            return "🕑 Snippet failed to finish within 2 minutes."

        after = utils.time.usec()

        el_us = after - before
        el_str = f"\nTime: {utils.time.format_duration_us(el_us)}"

        err = f"⚠️ Return code: {proc.returncode}" if proc.returncode != 0 else ""

        return f"```{proc.stdout.strip()}```{err}{el_str}"

    @command.desc("Get information about the host system")
    @command.alias("si")
    async def cmd_sysinfo(self, msg):
        if msg is not None: await msg.result("Collecting system information...")

        try:
            proc = await self.run_process(["neofetch", "--stdout"], timeout=15)
        except subprocess.TimeoutExpired:
            return "🕑 `neofetch` failed to finish within 15 seconds."
        except FileNotFoundError:
            return "❌ The `neofetch` [program](https://github.com/dylanaraps/neofetch) must be installed on the host system."

        err = f"⚠️ Return code: {proc.returncode}" if proc.returncode != 0 else ""
        sysinfo = "\n".join(proc.stdout.strip().split("\n")[2:]) if proc.returncode == 0 else proc.stdout.strip()
        try:
            proc = await self.run_process(["iostat", "-c", "2", "1"], timeout=10)
            used_cpu = round(float(proc.stdout.strip().split()[-1]))
            sysinfo += f"\nCPU Usage: {100 - used_cpu}%"
        except Exception as ex: print(ex)
        try:
            proc = await self.run_process(["vcgencmd", "measure_temp"], timeout=10)
            sysinfo += "\nTemp: " + proc.stdout.strip().replace("temp=", "")
        except Exception as ex: print(ex)

        return f"```{sysinfo}```{err}"

    @command.desc("Get information about the host network")
    @command.alias("ni")
    async def cmd_netinfo(self, msg, adapter: str = "eth0"):
        await msg.result("Collecting network information...")

        try:
            proc = await self.run_process(["bash", "/etc/net.sh", adapter], timeout=5)
        except subprocess.TimeoutExpired:
            return "🕑 `net` failed to finish within 5 seconds."

        err = f"⚠️ Return code: {proc.returncode}" if proc.returncode != 0 else ""
        sysinfo = proc.stdout.strip()

        return f"Network info for **{adapter}**:\n```{sysinfo}```{err}"

    @command.desc("Test Internet speed")
    @command.alias("stest", "st")
    async def cmd_speedtest(self, msg):
        before = utils.time.usec()

        before = utils.time_us()
        timeout = 500
        try:
            proc = await self.run_process("speedtest", timeout=timeout)
        except subprocess.TimeoutExpired:
            return f"🕑 `speedtest` failed to finish within {timeout / 60} minutes."
        except FileNotFoundError:
            return "❌ The `speedtest` [program](https://github.com/sivel/speedtest-cli) (package name: `speedtest-cli`) must be installed on the host system."
        after = utils.time_us()
        st = await utils.run_sync(speedtest.Speedtest)
        status = "Selecting server..."

        await msg.result(status)
        server = await utils.run_sync(st.get_best_server)
        status += f" {server['sponsor']} ({server['name']})\n"
        status += "Ping: %.2f ms\n" % server["latency"]

        status += "Performing download test..."
        await msg.result(status)
        dl_bits = await utils.run_sync(st.download)
        dl_mbit = dl_bits / 1000 / 1000
        status += " %.2f Mbps\n" % dl_mbit

        status += "Performing upload test..."
        await msg.result(status)
        ul_bits = await utils.run_sync(st.upload)
        ul_mbit = ul_bits / 1000 / 1000
        status += " %.2f Mbps\n" % ul_mbit

        delta = utils.time.usec() - before
        status += f"\nTime elapsed: {utils.time.format_duration_us(delta)}"

        return f"```{out}```{err}{el_str}"

    @command.desc("Test Disk speed")
    @command.alias("dstest", "dst")
    async def cmd_diskspeedtest(self, msg):
        await msg.result("Testing Disk speed; this may take a while...")

        before = utils.time_us()
        timeout = 60
        try:
            proc = await self.run_process_sudo(["/bin/sh","/home/blu/sdtest.sh"], timeout=timeout)
        except subprocess.TimeoutExpired:
            return f"🕑 `sdtest` failed to finish within {timeout / 60} minutes."
        after = utils.time_us()

        el_us = after - before
        el_str = f"\nTime: {utils.format_duration_us(el_us)}"

        err = f"⚠️ Return code: {proc.returncode}" if proc.returncode != 0 else ""

        out = proc.stdout.strip()

        return f"```{out}```{err}{el_str}"
