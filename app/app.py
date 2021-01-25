from aiohttp import web

from handlers import healthz, list_directory, read_file
from middlewares import parse_json, handle_errors


def get_app():
    web_app = web.Application(middlewares=[parse_json, handle_errors])

    web_app.add_routes([
        web.get('/healthz', healthz),
        web.post('/directory', list_directory),
        web.post('/file', read_file)
    ])
    return web_app


if __name__ == '__main__':
    web_app = get_app()
    web.run_app(web_app)
