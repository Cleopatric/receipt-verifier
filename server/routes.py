from views import api_root, get_user_receipts, sign_up, verify_receipt


def setup_routes(app):
    app.router.add_route('GET', '/', api_root)
    app.router.add_route('GET', '/api/get_user_receipts', get_user_receipts)
    app.router.add_route('POST', '/api/sign_up', sign_up)
    app.router.add_route('POST', '/api/verify_receipt', verify_receipt)
