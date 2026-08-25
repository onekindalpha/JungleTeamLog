# 홈 화면 SSR
from test_auth import get_current_user_id

from flask import Blueprint, render_template
from bson import ObjectId
from config import db
from test_auth import get_current_user_id

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def home():

    # 1. 현재 로그인한 사용자의 user_id 가져오기
    user_id = get_current_user_id()

    # 2. 현재 사용자가 속한 팀 목록 조회
    teams = db.team_pages.find(
        {
            "members.user_id": ObjectId(user_id)
        },
        {
            "_id": 1,
            "week":
            1
        }
    ).sort("week", 1)

    # 3. 주차별 team_page_id 구성
    week_teams = {}

    for team in teams:
        week_teams[team["week"]] = str(team["_id"])

    # 4. 홈 화면 렌더링
    return render_template(
        "home.html",
        week_teams=week_teams
    )