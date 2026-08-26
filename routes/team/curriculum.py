from flask import Blueprint, request, jsonify
from bson import ObjectId
from config import db

curriculum_bp = Blueprint('curriculum', __name__)

@curriculum_bp.route("/api/team_pages/<team_page_id>/curriculum", methods=["PATCH"])
def update_curriculum(team_page_id):
    data = request.json
    curriculum = data.get("curriculum", "").strip()

    if not curriculum:
        return jsonify({"error": "커리큘럼을 입력해주세요"}), 400

    db.team_pages.update_one(
        {"_id": ObjectId(team_page_id)},
        {"$set": {"curriculum": curriculum}}
    )

    return jsonify({"success": True, "curriculum": curriculum})