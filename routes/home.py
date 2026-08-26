from config import db
from flask import Blueprint, request, render_template, redirect
from routes.utils.jwt_utils import decode_token, jwt_required

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
@jwt_required
def home():
    # JWT(로그인 인증 토큰) 가져오기 
    token = request.cookies.get("mytoken")

    # JWT 검증 - 가져온 토큰이 유효한지 암호를 해독(Decode)하고 검증
    payload = decode_token(token)
    # 토큰 검증에 실패했다면 (비로그인 상태 혹은 토큰 만료)
    if payload is None:
        return redirect("/login")
    
    # 현재 사용자 조회
    user = db.users.find_one({"email": payload["email"]})

    if user is None:
        return redirect("/login")

    # 현재 로그인한 사용자 ID
    user_id = user["_id"]

    # 현재 사용자가 속한 팀 조회 - user_id가 포함된 문서 찾기. 그중 _id와 week필드만 가져오기
    teams = list(
        db.team_pages.find(
            {"members.user_id": user_id},
            {"_id": 1, "week": 1}
        )
    )

    # 주차 -> 팀 페이지 ID 구성
    week_teams = {}
    for team in teams:
        week_teams[team["week"]] = str(team["_id"])

    # 디버깅용 코드
    print("현재 user_id:", user_id)
    print("teams:", teams)
    print("week_teams:", week_teams)

    # 홈 화면 렌더링
    return render_template("home.html", week_teams=week_teams)


# 주차 클릭 시 DB에서 팀 존재 여부 확인
@home_bp.route("/team/check/<int:week>")
@jwt_required
def check_team(week):
    # JWT 가져오기
    token = request.cookies.get("mytoken")

    # JWT 검증
    payload = decode_token(token)

    if payload is None:
        return redirect("/login")

    # 현재 사용자 조회
    user = db.users.find_one({"email": payload["email"]})

    if user is None:
        return redirect("/login")

    # 해당 주차에 현재 사용자가 속한 팀 조회
    team = db.team_pages.find_one(
        {
            "week": week,
            "members.user_id": user["_id"]
        }
    )

    # 팀이 있으면 해당 팀 페이지 이동
    if team:
        return redirect(f"/team/{team['_id']}")

    # 팀이 없으면 팀 생성 페이지 이동
    return redirect(f"/team/new?week={week}")


# [로그아웃 기능] - path="/" 필수 지정
@home_bp.route("/logout", methods=["GET"])
def logout():
    # 1. 로그인 페이지로 리다이렉트하는 응답 객체 준비
    response = redirect("/login")
    
    # 2. 루트 경로 전체에서 'mytoken' 쿠키를 확실하게 삭제
    response.delete_cookie("mytoken", path="/")
    
    return response

@home_bp.route("/my/wil")
@jwt_required
def my_wil():
    return render_template("my_wil.html")