from datetime import date, datetime

from bson import ObjectId
from config import db
from flask import Blueprint, jsonify, request
from routes.utils.jwt_utils import decode_token, jwt_required

scrums_bp = Blueprint("scrums", __name__)


# 1. 스크럼 추가 API
@scrums_bp.route("/api/team_pages/<team_page_id>/scrums", methods=["POST"])
@jwt_required  # [추가] 로그인한 유저만 접근 가능
def add_scrums(team_page_id):
    # JWT 토큰에서 현재 로그인한 유저 정보 추출
    token = request.cookies.get("mytoken")
    payload = decode_token(token)

    current_user = db.users.find_one({"email": payload["email"]})
    if not current_user:
        return jsonify({"error": "유효하지 않은 사용자입니다."}), 401

    current_user_id = current_user["_id"]
    user_name = (
        current_user.get("name") or current_user.get("username") or "팀원"
    )

    data = request.json or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "내용을 입력해주세요"}), 400

    today = date.today().isoformat()  # 예: "2026-08-26"

    result = db.scrums.insert_one(
        {
            "team_page_id": ObjectId(team_page_id),
            "user_id": current_user_id,  # 실제 로그인한 유저의 ObjectId 저장
            "content": content,
            "log_date": today,
            "created_at": datetime.now(),
        }
    )

    return jsonify(
        {
            "success": True,
            "scrum": {
                "_id": str(result.inserted_id),
                "content": content,
                "log_date": today,
                "user_name": user_name,
            },
        }
    )


# 2. 스크럼 수정 API
@scrums_bp.route("/api/scrums/<scrum_id>", methods=["PATCH"])
@jwt_required  # [추가] 로그인한 유저만 접근 가능
def update_scrums(scrum_id):
    token = request.cookies.get("mytoken")
    payload = decode_token(token)

    current_user = db.users.find_one({"email": payload["email"]})
    if not current_user:
        return jsonify({"error": "유효하지 않은 사용자입니다."}), 401

    scrum = db.scrums.find_one({"_id": ObjectId(scrum_id)})
    if not scrum:
        return jsonify({"error": "존재하지 않는 스크럼입니다."}), 404

    # 본인 글 검증 (DB의 user_id와 로그인한 user_id 비교)
    if str(scrum.get("user_id")) != str(current_user["_id"]):
        return jsonify({"error": "본인 글만 수정할 수 있습니다."}), 403

    data = request.json or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "내용을 입력해주세요"}), 400

    db.scrums.update_one(
        {"_id": ObjectId(scrum_id)}, {"$set": {"content": content}}
    )

    return jsonify({"success": True, "content": content})


# 3. 스크럼 삭제 API
@scrums_bp.route("/api/scrums/<scrum_id>", methods=["DELETE"])
@jwt_required  # [추가] 로그인한 유저만 접근 가능
def delete_scrums(scrum_id):
    token = request.cookies.get("mytoken")
    payload = decode_token(token)

    current_user = db.users.find_one({"email": payload["email"]})
    if not current_user:
        return jsonify({"error": "유효하지 않은 사용자입니다."}), 401

    scrum = db.scrums.find_one({"_id": ObjectId(scrum_id)})
    if not scrum:
        return jsonify({"error": "존재하지 않는 스크럼입니다."}), 404

    # 본인 글 검증
    if str(scrum.get("user_id")) != str(current_user["_id"]):
        return jsonify({"error": "본인 글만 삭제할 수 있습니다."}), 403

    db.scrums.delete_one({"_id": ObjectId(scrum_id)})

    return jsonify({"success": True})