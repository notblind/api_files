# import os
import asyncio
from aiohttp import web

from routes import urls

app = web.Application()

app.add_routes(urls)

web.run_app(app, host='localhost', port='8002')

