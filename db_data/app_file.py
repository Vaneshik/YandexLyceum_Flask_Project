app = None


def set_app(init_app):
    global app
    app = init_app


def get_app():
    return app
