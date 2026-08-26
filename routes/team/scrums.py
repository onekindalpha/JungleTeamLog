from flask import Blueprint, request, jsonify, g
from bson import ObjectId
from datetime import datetime, date
from config import db
from ..utils.jwt_utils import jwt_required

scrums_bp = Blueprint('scrums', __name__)

@scrums_bp.route("/api/team_pages/<team_page_id>/scrums", methods=["POST"])
@jwt_required
def add_scrums(team_page_id):
    current_user_id = ObjectId(g.user["user_id"])
    user = db.users.find_one({"_id": current_user_id})
    user_name = user["name"] if user else "알수없음"

    data = request.json # 파이썬의 딕셔너리로 반환 
    content = data.get("content", "").strip() 
    if not content:
        return jsonify({"error": "내용을 입력해주세요"}), 400 

    today = date.today().isoformat() # "2026-08-25" 형태

    result = db.scrums.insert_one({
        "team_page_id": ObjectId(team_page_id),
        "user_id": current_user_id,
        "content": content,
        "log_date": today,
        "created_at": datetime.now()
    })

    return jsonify({
        "success": True,
        "scrum":{
            "_id": str(result.inserted_id),
            "content": content,
            "log_date": today,
            "user_name": user_name,
        }
    })

@scrums_bp.route("/api/scrums/<scrum_id>", methods=["PATCH"])
@jwt_required
def update_scrums(scrum_id):
    # 존재하는지 확인 
    scrum = db.scrums.find_one({"_id": ObjectId(scrum_id)})
    if not scrum:
        return jsonify({"error":"존재하지 않는 스크럼입니다."}), 404 

    # 본인 글인지 검증 
    current_user_id = ObjectId(g.user["user_id"])
    if scrum["user_id"] != current_user_id:
        return jsonify({"error":"본인 글만 수정할 수 있습니다."}), 403

    # body 가져오기 
    data = request.json
    content = data.get("content", "").strip()

    if not data:
        return jsonify({"error":"내용을 입력해주세요"}), 403

    # 수정
    db.scrums.update_one(
        {"_id": ObjectId(scrum_id)}, # 첫 번째 인자: "어떤 문서를" 찾을지 (조건)
        {"$set": {"content": content}} # 두 번째 인자: "뭘 어떻게" 바꿀지 (변경 내용)
    )

    return jsonify({"success": True, "content": content})


@scrums_bp.route("/api/scrums/<scrum_id>", methods=["DELETE"])
def delete_scrums(scrum_id):
    # 존재하는지 확인  
    scrum = db.scrums.find_one({"_id": ObjectId(scrum_id)})

    if not scrum:
        return jsonify({"error":"존재하지 않는 스크럼입니다."}), 404 

    # 본인 글인지 검증 
    current_user_id = ObjectId(g.user["user_id"])
    if scrum["user_id"] != current_user_id:
        return jsonify({"error":"본인 글만 삭제할 수 있습니다."}), 403

    db.scrums.delete_one({"_id": ObjectId(scrum_id)})

    return jsonify({"success": True})