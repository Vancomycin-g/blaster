#!/bin/env python3

import argparse
import ddddocr
from aiohttp import web
import base64

parser = argparse.ArgumentParser(prog="cbhs")
parser.add_argument("-a", help="http basic auth")
parser.add_argument("-p", help="http port")
args = parser.parse_args()

ocr = ddddocr.DdddOcr()
auth_base64 = base64.b64encode(args.a.encode('ascii')).decode()
port = args.p


async def handle_cb(request):
    if request.headers.get('Authorization') != 'Basic ' + auth_base64:
        return web.Response(text='Forbidden', status='403')
    return web.Response(text=ocr.classification(img_base64=await request.text()))


async def handle(request):
    return web.Response(text='Forbidden', status='403')


app = web.Application()
app.add_routes([
    web.post('/cb', handle_cb),
    web.post('/', handle),
])

# python3 cbhs.py -a user:pass -p port


if __name__ == '__main__':
    web.run_app(app, port=port)
