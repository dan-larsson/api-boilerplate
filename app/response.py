from flask import Response

class JSONResponse(Response):
    default_mimetype = 'application/json'
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONResponse, cls).force_type(rv, environ)