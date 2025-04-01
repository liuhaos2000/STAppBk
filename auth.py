from functools import wraps
from flask import request, jsonify

def check_auth(token):
    # 这里可以实现你的身份验证逻辑，比如检查 token 是否有效
    print(f"Token received: {token}")
    return token == "your-secret-token"

def authenticate():
    return jsonify({"message": "Unauthorized"}), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"Authorization header: {token}")
        if not token or not check_auth(token):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
