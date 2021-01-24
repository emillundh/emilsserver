import os
import time

from aiohttp import web


async def healthz(request):
    return web.HTTPOk()


async def list_directory(path):
    time.sleep(5)
    files = os.listdir(path)
    return web.json_response({'directory_contents': files})


async def read_file(path):
    time.sleep(5)
    with open(path, 'r') as infile:
        contents = infile.read()
    return web.json_response({'file_contents': contents})
