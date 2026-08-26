from flask import Flask, jsonify, render_template, request, Blueprint, make_response
import jwt
import datetime # 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import hashlib
from config import db
from .utils.jwt_utils import create_token, decode_token

auth_bp = Blueprint("auth", __name__)

#################################
##  로그인을 위한 API            ##
#################################

# 1. [GET] 회원가입 페이지 API
@auth_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

# 2. [POST] 회원가입 처리
@auth_bp.route("/api/auth/signup", methods=["POST"])
def api_signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    
    # 이메일 중복 검사
    exists = db.users.find_one({"email": email})
    if exists is not None:
        return jsonify({"result":"fail", "msg":"이미 존재하는 이메일입니다."})
    
    # 비밀번호 해싱 후 DB 저장
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    db.users.insert_one({"email": email, "password_hash": pw_hash, "name": name})
    
    return jsonify({"result": "success", "msg": "회원가입이 완료되었습니다."})

# [로그인 API]
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# 로그인 처리해서 JWT 발급받기
@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = db.users.find_one({"email": email, "password_hash": pw_hash})
    
    if user is None:
        return jsonify({
            "result": "fail",
            "msg": "아이디 또는 비밀번호가 일치하지 않습니다."
        })
        
    token = create_token(user["_id"], email)
    return jsonify({"result": "success", "token": token})


# 로그아웃 토큰 제거하기
@auth_bp.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    response = make_response(
        jsonify({"result": "success", "msg": "로그아웃 완료"})
    )
    response.delete_cookie("mytoken")
    return response