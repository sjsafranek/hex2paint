from flask import jsonify

class ApiResponse(object):

    @staticmethod
    def BadRequest(message='Bad Request'):
        return jsonify({
            'status': 'error', 
            'message': message
        }), 400

    @staticmethod
    def OK(data=None, params=None):
        return jsonify({
            'status': 'ok', 
            'data': data,
            'params': params
        }), 200

