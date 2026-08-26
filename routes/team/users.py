# 팀원 선택용 사용자 목록 조회

from routes.utils.jwt_utils import decode_token, jwt_required

from flask import Blueprint, request, jsonify

from config import db


users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users", methods=["GET"])
@jwt_required
def get_available_users():

    # 1. URL에서 week 가져오기
    week = request.args.get("week", type=int)

    # 2. week 값 검증
    if week is None or not (1 <= week <= 23):
        return jsonify({
            "error": "week 값이 올바르지 않습니다."
        }), 400


    # 3. JWT에서 현재 로그인한 사용자 확인

    token = request.cookies.get("mytoken")

    payload = decode_token(token)

    if payload is None:
        return jsonify({
            "error": "인증이 필요합니다."
        }), 401


    # JWT email로 사용자 조회
    current_user = db.users.find_one({
        "email": payload["email"]
    })


    if current_user is None:
        return jsonify({
            "error": "현재 사용자를 찾을 수 없습니다."
        }), 404



    # 4. 해당 주차에 이미 생성된 팀 조회

    teams = db.team_pages.find(
        {
            "week": week
        },
        {
            "members.user_id": 1
        }
    )


    # 5. 이미 다른 팀에 속한 사용자 ID 수집

    joined_user_ids = set()

    for team in teams:

        for member in team.get("members", []):

            joined_user_ids.add(
                str(member["user_id"])
            )



    # 6. 모든 사용자 조회

    users = db.users.find(
        {},
        {
            "_id": 1,
            "name": 1
        }
    )


    available_users = []


    for user in users:

        user_id = str(user["_id"])


        # 현재 주차 다른 팀에 속한 사람 제외
        # 단, 로그인한 본인은 포함

        if (
            user_id in joined_user_ids
            and user_id != str(current_user["_id"])
        ):
            continue


        available_users.append({

            "user_id": user_id,

            "name": user["name"]

        })



    # 7. 반환

    return jsonify({

        "current_user_id": str(current_user["_id"]),

        "users": available_users

    }), 200