import datetime
from functools import wraps
from flask import redirect, render_template, request, url_for
import jwt

from config import SECRET_KEY


def create_token(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ["HS256"])
        return payload
    except:
        return None
    
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("mytoken")
        
        if not token or decode_token(token) is None:
            return redirect("/login")
        
        return f(*args, **kwargs)
    
    return decorated_function