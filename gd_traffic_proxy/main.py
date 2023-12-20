import aiohttp
from aiohttp import web
import asyncio

from rich.console import Console
from rich.traceback import install

import settings

console = Console()
install(console=console)


async def handle(request: web.Request) -> web.Response:
    return web.Response(text="Hello, world")


async def run_server() -> None:
    server = web.Server(handle)
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
