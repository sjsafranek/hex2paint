import os.path
import logging
from functools import reduce
from flask import Flask
from flask import flash
from flask import request
from flask import redirect
from flask import render_template
from flask import send_from_directory

from api import ApiResponse
from paint_search import search
from paint_search import getBrands
from paint_search import getColorSpaces
from utils import getParametersFromRequest


# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%Y-%m-%dT%H:%M:%S',
    #datefmt='%Y-%m-%dT%H:%M:%S%z',
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s %(funcName)s:%(lineno)d %(message)s"
)


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'skeleton'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/favicon.ico')
def favicon():
    file = reduce(os.path.join, [app.root_path, 'static', 'images'])
    return send_from_directory(
            file,
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )


@app.route("/", methods=['GET', 'POST'])
def paint_search():

    # Search Parameters
    params = getParametersFromRequest(request)
    color = params.get('color')

    # Parse request body
    if 'POST' == request.method:
        if not color:
            flash('Color is required!', 'error')
        color = color.lstrip('#')
        brands = ','.join(params.get('brands'))
        matches = params.get('matches')
        algorithm = params.get('algorithm')
        color_space = params.get('color_space').lower()
        return redirect(f'/?color={color}&brands={brands}&matches={matches}&algorithm={algorithm}&color_space={color_space}')

    # Search for matching paints if needed
    paints = None
    if color:
        if not color.startswith('#'):
            color = f'#{color}'
        paints = search(color, **params)

    # Render Template
    return render_template(
        'site.html', 
        paints = paints, 
        color = color or '#563d7c', 
        brands=getBrands(),
        color_spaces=getColorSpaces()
    )


@app.route("/api", methods=['GET', 'POST'])
def paint_search_api():
    params = getParametersFromRequest(request)

    color = params.get('color')
    if not color:
        return ApiResponse.BadRequest(message="Missing Parameter = 'color'")
    if not color.startswith('#'):
        color = f'#{color}'
    
    return ApiResponse.OK(
        data={
            'paints': search(color, **params)
        }, 
        params=params
    )
