import sys
import os.path
import shutil
from flask import Flask, render_template
from werkzeug.debug import DebuggedApplication
import base64

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'parflow', 'src'))
from pfclm import PFCLM_SC as run
from plots import plot

app = Flask(__name__)

title = 'PFCLM'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', host=os.getenv('host'), port=os.getenv('port'))


@app.route('/parflow')
def parflow():
    INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'parflow', 'inputs')
    FORCING_DIR = os.path.join(os.path.dirname(__file__), '..', 'parflow', 'forcing')
    OUTPUT_DIR = os.path.join(os.getenv('HOME'), 'RESULTS/output') 
    PNG_PATH = os.path.join(os.getenv('HOME'), 'RESULTS/plot.png') 

    # copy input files directly in the base output folder,
    # because that's where Parflow expects them to be.
    shutil.copytree(INPUT_DIR, OUTPUT_DIR, dirs_exist_ok=True)

    run.Solver.CLM.CLMFileDir = OUTPUT_DIR
    run.Solver.CLM.MetFilePath  = FORCING_DIR 
    run.run(working_directory=OUTPUT_DIR)
    plot(OUTPUT_DIR, run.get_name(), PNG_PATH, title=title)

    img = open(PNG_PATH, 'rb').read()
    return render_template('result.html', img=base64.encodebytes(img).decode('ascii'))


if __name__ == '__main__':

    DEBUG = True 
    if DEBUG:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    host, port = sys.argv[1], sys.argv[2]
    if len(sys.argv)>3:
        title = sys.argv[3]
    app.run(debug=DEBUG, host=host, port=int(port))

