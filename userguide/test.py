from flask import Flask

app = Flask(__name__)


class Foo(object):
    def __init__(self, name):
        self.name = name

    def view(self):
        return self.name

bar = Foo('bar')
bee = Foo('bee')

app.add_url_rule('/bar', view_func=bar.view, endpoint='bar.view')

app.add_url_rule('/bee', view_func=bee.view, endpoint='bee.view')

if __name__ == "__main__":
    app.run(debug=True, port=8090)
