import os.path
import logging
from functools import reduce
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

from paint_search import search
from paint_search import getSources


# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%Y-%m-%dT%H:%M:%S',
    #datefmt='%Y-%m-%dT%H:%M:%S%z',
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s %(funcName)s:%(lineno)d %(message)s"
)


app = Flask(__name__, static_url_path='/static')

@app.route('/favicon.ico')
def favicon():
    file = reduce(os.path.join, [app.root_path, 'static', 'images'])
    logging.debug('favicon', file)
    return send_from_directory(
            file,
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

@app.route("/", methods=['GET'])
@app.route("/<color_hex>", methods=['GET', 'POST'])
def paint_search(color_hex=None):
    default_color = "#563d7c"
    colors = None
    if color_hex:
        if not color_hex.startswith('#'):
            color_hex = f'#{color_hex}'
        default_color = color_hex
        sourcesFilter = []
        if 'sources' in request.args:
            sourcesFilter = request.args.get('sources').split(',')
            sourcesFilter = [source for source in sourcesFilter if source]
        colors = search(color_hex, matches=8, sources=sourcesFilter)
    return render_template('site.html', colors=colors, default_color=default_color, sources=getSources())




'''

flask run --reload --host=0.0.0.0


'''