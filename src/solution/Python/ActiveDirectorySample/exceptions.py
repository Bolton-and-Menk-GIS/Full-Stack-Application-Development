from werkzeug.exceptions import HTTPException

__all__ = ('invalid_credentials', 'unauthorized_user', 'InvalidCredentials', 'UnauthorizedUser', 'TokenRequired', 'token_required', 'TokenExpired', 'token_expired')

class InvalidCredentials(HTTPException):
    code = 401
    description = 'Invalid Credentials'
    message = 'Access Denied: Invalid Credentials'

class UnauthorizedUser(HTTPException):
    code = 403
    description = 'Unauthorized User'
    message = 'Access Denied: Unauthorized User'

class TokenExpired(HTTPException):
    code = 499
    description = 'Token Expired'
    message = 'Access Denied: the user Token is expired'

def token_expired(error):
    response = jsonify({'error':
        {
            'code': TokenExpired.code,
            'message': TokenExpired.message
            }
    })

    response.status_code = TokenExpired.code
    return response

class TokenRequired(HTTPException):
    code = 461
    description = 'Token Required'
    message = 'Access Denied: a Token is required to access this resource'

def token_required(error):
    response = jsonify({'error':
        {
            'code': TokenRequired.code,
            'message': TokenRequired.message
            }
    })

    response.status_code = TokenRequired.code
    return response


def invalid_credentials(error):
    response = jsonify({'error':
        {
            'code': InvalidCredentials.code,
            'message': InvalidCredentials.message}
    })

    response.status_code = InvalidCredentials.code
    return response

def unauthorized_user(error):
    response = jsonify({'error':
        {
            'code': UnauthorizedUser.code,
            'message': UnauthorizedUser.message}
    })

    response.status_code = UnauthorizedUser.code
    return response