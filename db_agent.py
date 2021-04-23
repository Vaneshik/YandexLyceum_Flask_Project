from db_data import db_session


def init() -> Session:
    db_session.global_init("db/shop.db")
    global sess
    sess = db_session.create_session()


def is_aviable(product):
    pass


if __name__ == '__main__':
    init()
