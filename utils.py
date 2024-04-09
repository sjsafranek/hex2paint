
from conf import DEFAULT_PARAMETERS


def _getParametersFromJsonBody(request):
    if not request.is_json:
        return {}
    return request.get_json().get('params', {})

def _getParametersFromForm(request):
    if not request.form or 0 == len(request.form.keys()):
        return {}
    form = dict(request.form)
    if request.form.getlist('sources'):
        form['sources'] = request.form.getlist('sources')
    return form

def _getParametersFromUrlArgs(request):
    if not request.args or 0 == len(request.args.keys()):
        return {}
    args = dict(request.args)
    if None != args.get('sources'):
        args['sources'] = [
            source for source in args.get('sources', '').split(',') if source
        ]
    if args.get('matches'):
        args['matches'] = int(args.get('matches'))
    return args

def getParametersFromRequest(request):
    ''' This merges parameters sent via different methods (JSON, form and query string).
        We will prioritize data sent within the request body.
    '''
    return {
        **DEFAULT_PARAMETERS,
        **_getParametersFromUrlArgs(request),
        **_getParametersFromForm(request),
        **_getParametersFromJsonBody(request)
    }

