# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, send_from_directory, url_for
from glob import glob

app = Flask(__name__)

@app.route('/')
def index():
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, 'templates', 'xcolors')
    themes = [os.path.splitext(os.path.basename(t))[0]
              for t in glob('{0}/*.html'.format(path))]
    return render_template('index.html', themes=themes)

@app.route('/dl/<path:filename>')
def download(filename):
    return send_from_directory('themes', filename,
                               mimetype='text/plain')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')


if __name__ == '__main__':
    from xcolor.generator import Generator
    path = os.path.dirname(__file__)
    xcolor = Generator(os.path.join(path, 'themes'),
                       os.path.join(path, 'templates', 'xcolors'))
    xcolor.cleanup()
    xcolor.generate_files()

    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG') in ("true", "True")

    app.run(host=host, port=port, debug=debug)
