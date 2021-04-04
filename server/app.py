from aiohttp import web
from aiohttp_swagger import *

from routes import setup_routes

if __name__ == '__main__':
    app = web.Application()
    setup_routes(app)
    setup_swagger(app, swagger_from_file='swagger.yaml')
    web.run_app(app)
