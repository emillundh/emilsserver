from json import JSONDecodeError

from aiohttp import web
from aiohttp.web_middlewares import middleware


@middleware
async def parse_json(request, handler):
    if request.method == 'GET':
        return await handler(request)
    try:
        parsed_json = await request.json()
        path = parsed_json['path']
        return await handler(path)
    except (JSONDecodeError, KeyError):
        return web.HTTPBadRequest()


@middleware
async def handle_errors(request, handler):
    try:
        return await handler(request)
    except FileNotFoundError:
        return web.HTTPNotFound(text='Path not found')
    except PermissionError:
        return web.HTTPForbidden(text='You cannot access that path')
    except IsADirectoryError:
        return web.HTTPBadRequest(text='Is a directory')
    except UnicodeDecodeError:
        return web.HTTPBadRequest(text='Not a text file')
    except NotADirectoryError:
        return web.HTTPBadRequest(text='Is not a directory')
