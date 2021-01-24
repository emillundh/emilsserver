from aiohttp import web

from handlers import healthz, list_directory, read_file
from middlewares import parse_json, handle_errors

app = web.Application(middlewares=[parse_json, handle_errors])

app.add_routes([
    web.get('/healthz', healthz),
    web.post('/directory', list_directory),
    web.post('/file', read_file)
])

web.run_app(app)
