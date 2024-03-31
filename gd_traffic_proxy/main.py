import aiohttp
from aiohttp import web
import asyncio
from typing import Any

from rich.console import Console
from rich.traceback import install
from rich.pretty import pprint

import settings

console = Console()
install(console=console)


async def handle(request: web.Request) -> web.Response:
    if not request.path.startswith(settings.HTTP_PROXY_PREFIX):
        return web.Response(status=404)
    
    data = await request.post()
    path = request.path.removeprefix(settings.HTTP_PROXY_PREFIX).removeprefix("/")

    target_url = f"{settings.TARGET_SERVER_URL}/{path}"

    async with aiohttp.ClientSession() as session:
        async with session.post(target_url, data=data, headers={
            "User-Agent": "",
        }) as resp:
            # TODO: Store results.
            if resp.status == 200:
                console.print(
                    f":white_heavy_check_mark: [bold green] {request.path} "
                    f"-> {resp.status} {resp.reason}",
                )
                pprint(data)
                pprint(await resp.text())
            else:
                console.print(
                    f":x: [bold red] {request.path} "
                    f"-> {resp.status} {resp.reason}",
                )
                pprint(data)
                pprint(await resp.text())

            return web.Response(
                status=resp.status,
                text=await resp.text(),
            )


async def run_server() -> None:
    server = web.Server(handle) # type: ignore
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, settings.HTTP_PROXY_HOST, settings.HTTP_PROXY_PORT)
    await site.start()

    console.print(
        ":white_heavy_check_mark: [bold green]gd_traffic_proxy is running on "
        f"http://{settings.HTTP_PROXY_HOST}:{settings.HTTP_PROXY_PORT}",
    )

    while True:
        await asyncio.sleep(1000)


def main() -> int:
    console.print(
        "Starting gd_traffic_proxy...",
        style="bold underline blue",
    )
    
    asyncio.run(run_server())

    return 0


if __name__ == "__main__":
    exit(main())
