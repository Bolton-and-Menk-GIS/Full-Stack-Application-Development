from werkzeug.exceptions import HTTPException


class InvalidCredentials(HTTPException):
    code = 403
    description = 'Invalid Credentials'
    message = 'Access Denied: Invalid Credentials'


class UnauthorizedUser(HTTPException):
    code = 401
    description = 'Unauthorized User'
    message = 'Access Denied: Unauthorized User'


class TokenRequired(HTTPException):
    code = 461
    description = 'Token Required'
    message = 'Access Denied: a Token is required to access this resource'

class SessionExpired(HTTPException):
    code = 463
    description = 'Session Expired'
    message = 'Your session has expired, please login again'


class InvalidResource(HTTPException):
    code = 513
    description = 'Invalid Resource'
    message = 'The requested resource is invalid, please check the request parameters and try again'


class UsernameAlreadyExists(HTTPException):
    code = 460
    description = 'Username Already Exists'
    message = 'The username supplied is already in use, please try a different name'


class CreateUserError(HTTPException):
    code = 464
    description = 'Create User Error'
    message = 'Unable to create user, please check the input parameters and try again'


class UserNotFound(HTTPException):
    code = 465
    description = 'User Not Found'
    message = 'Could not find user'


class UserNotActivated(HTTPException):
    code = 466
    description = 'User is not Activated'
    message = 'The user has not activated their account'

