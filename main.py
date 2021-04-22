from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'biba_i_boba'


def main():
    app.run()


if __name__ == '__main__':
    main()