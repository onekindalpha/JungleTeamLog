# 팀원 선택용 사용자 목록 조회
from flask import Blueprint, request, jsonify
from bson import ObjectId

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/users", methods=["GET"])
def get_available_users():
    # 1. URL에서 week 가져오기
    week = request.args.get("week", type=int)
    # 2. week 값 검증
    if week is None or not (1 <= week <=23):
        return jsonify({
            "error":"week값이 올바르지 않습니다."
        }), 400
    # 3. (중요- 협업 확인 필요 부분) 현재 로그인한 사용자의 user_id를 가져오기 (JWT등 인증정보에서 사용자 ID를 가져오기)
    user_id = get_current_user_id()
    
    # 4. user_id가 유효한 ObjectId인지 확인
    if not ObjectId.is_valid(user_id):
        return jsonify({
            "error": "현재 사용자를 찾을 수 없습니다."
        }), 400
    # 5. users 컬렉션에서 현재 사용자 조회
    current_user = mongo.db.users.find_one({
        "_id": ObjectId(user_id)
    })
    if not current_user:
        return jsonify({
            "error": "현재 사용자를 찾을 수 없습니다."
        }), 404
    
    # 6. 해당 week의 기존 팀 조회
    teams = mongo.db.team_pages.find(
        {"week": week},
        {"members.user_id":1}
    )
    # 7. 기존 팀에 속한 사용자 ID 수집
    joined_user_ids = set()
    for team in teams:
        for member in team.get("members", []):
            joined_user_ids.add(str(member["user_id"]))
    # 8. users 컬렉션에서 선택 가능한 사용자 조회
    users= mongo.db.users.find(
        {},
        {
            "_id":1,
            "name":1,
        }
    )
    available_users = []
    for user in users:
        # 현재 주차의 기존 팀에 속한 사용자는 선택 목록에서 제외
        if str(user["_id"]) in joined_user_ids:
            continue
        available_users.append({
            "user_id": str(user["_id"]),
            "name": user["name"]
        })
    # 9. 현재 로그인한 사용자 정보와 선택 가능한 사용자 목록을 JSON으로 반환
    return jsonify({
        "current_user_id": str(current_user["_id"]),
        "users": available_users
    }), 200