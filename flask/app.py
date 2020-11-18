from flask import Flask, render_template
from werkzeug.debug import DebuggedApplication


app = Flask(__name__)

greeting = ''

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', message=greeting)


if __name__ == '__main__':

    DEBUG = False
    if DEBUG:
        app.wsgi_app = DebuggedApplication(wsgi_app, evalex=True)

    host, port, greeting = sys.argv[1:]
    app.run(debug=DEBUG, host=host, port=int(port))

