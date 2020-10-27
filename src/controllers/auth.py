import jwt

from settings import SECRET_KEY, BCRYPT
from controllers.user import get_one_user


def authentication(auth=None):
    if not auth:
        status = 401
        response = "Login is required"
    elif not auth['username'] or not auth['password']:
        status = 401
        response = "Username and password are required"
    else:
        result, status_ = get_one_user(auth['username'])
        if status_ == 200:
            response, status = get_auth_response(result, auth)
        else:
            response = result
            status = status_
    return response, status


def get_auth_response(user, auth):
    if BCRYPT.check_password_hash(user['password'], auth['password']):
        token = jwt.encode(
            {
                'username': user['username'],
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return {
            'msg': 'Validated successfully',
            'token': token.decode('utf-8'),
        }, 200
    return 'Invalid password', 401
