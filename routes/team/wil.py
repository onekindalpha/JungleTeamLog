from flask import Blueprint, jsonify, request, g
from bson import ObjectId
from config import db 
from datetime import datetime
from ..utils.jwt_utils import jwt_required

wil_bf = Blueprint('wil', __name__)

# 등록
@wil_bf.route("/api/team_pages/<team_page_id>/wil", methods=["POST"])
@jwt_required
def add_wil(team_page_id):
    data = request.json
    url = data.get("url", "").strip()

    current_user_id = ObjectId(g.user["user_id"])

    # 본인이 쓴 wil이 존재하는지 확인
    existing = db.wil.find_one({
        "team_page_id": ObjectId(team_page_id),
        "user_id": current_user_id
    })
    if not existing:
        result = db.wil.insert_one({
            "team_page_id": ObjectId(team_page_id),
            "user_id": current_user_id,
            "url": url,
            "created_at": datetime.now(),
        })
        
    else:
        result = db.wil.update_one(
            {"_id": existing["_id"]},
            {"$set":{"url": url}}
        )


    return jsonify({
        "success": True,
        "url": url
    })
