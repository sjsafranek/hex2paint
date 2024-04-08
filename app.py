import logging
from flask import Flask
from flask import render_template

from color_search import search

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%Y-%m-%dT%H:%M:%S',
    #datefmt='%Y-%m-%dT%H:%M:%S%z',
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s %(funcName)s:%(lineno)d %(message)s"
)


app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/<color_hex>", methods=['GET', 'POST'])
def color_search(color_hex=None):
    default_color = "#563d7c"
    colors = None
    if color_hex:
        if not color_hex.startswith('#'):
            color_hex = f'#{color_hex}'
        default_color = color_hex
        colors = search(color_hex, matches=5)
    return render_template('site.html', colors=colors, default_color=default_color)




'''

flask run --host=0.0.0.0


'''