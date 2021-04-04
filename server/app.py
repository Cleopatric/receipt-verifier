import json

from aiohttp import web
from aiohttp_swagger import *

from aiohttp_basicauth import BasicAuthMiddleware

from instances.services import ReceiptVerifier

auth = BasicAuthMiddleware()
service = ReceiptVerifier()


async def api_root(request):
    raise web.HTTPFound(location='/api/doc#/')


async def sign_up(request):
    params = await request.json()
    response = await service.add_user(params)
    return web.Response(text=json.dumps(response), status=200)


async def get_user_receipts(request):
    user_info = auth.parse_auth_header(request)
    if user_info:
        response = await service.get_user_info(user_info.login, user_info.password)
    else:
        response = await service.get_user_info('', '')
    return web.Response(text=json.dumps(response), status=200)


async def verify_receipt(request):
    params = await request.json()
    user_info = auth.parse_auth_header(request)
    if user_info:
        response = await service.verify_receipt(user_info.login, user_info.password, params)
    else:
        response = await service.verify_receipt('', '', params)
    return web.Response(text=json.dumps(response), status=200)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('GET', '/', api_root)
    app.router.add_route('GET', '/api/get_user_receipts', get_user_receipts)
    app.router.add_route('POST', '/api/sign_up', sign_up)
    app.router.add_route('POST', '/api/verify_receipt', verify_receipt)
    setup_swagger(app, swagger_from_file='swagger.yaml')
    web.run_app(app)
