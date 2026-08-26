import datetime

from functools import wraps

from flask import redirect, render_template, request, url_for

import jwt

from config import SECRET_KEY


def create_token(email):

    payload = {
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=1),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def decode_token(token):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    # 추가: 만료된 JWT 처리
    except jwt.ExpiredSignatureError:
        return None

    # 추가: 잘못된 JWT 처리
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        # JWT 쿠키 가져오기
        token = request.cookies.get("mytoken")

        # 기존: 토큰이 없거나 검증 실패 시 인증 오류 반환
        # 수정: 로그인 페이지로 이동하도록 redirect 처리
        if not token:
            return redirect("/login")

        # 추가: 토큰 유효성 검증
        payload = decode_token(token)

        # 추가: 만료되었거나 잘못된 토큰이면 로그인 페이지 이동
        if payload is None:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function