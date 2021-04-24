app = None
login_manager = None


def set_app(init_app):
    global app
    app = init_app


def set_login_manager(init_login_manager):
    global login_manager
    login_manager = init_login_manager


def get_app():
    return app


def get_login_manager():
    return login_manager