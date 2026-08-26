from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from config import db

goals_bp = Blueprint('goals', __name__)

@goals_bp.route("/api/team_pages/<team_page_id>/goals", methods=["POST"])
def add_goal(team_page_id):
    data = request.json
    competency = data.get("competency", "").strip()
    goal_text = data.get("goal_text", "").strip()

    if not competency or not goal_text:
        return jsonify({"error": "핵심역량과 목표 내용을 모두 입력해주세요"}), 400

    result = db.goals.insert_one({
        "team_page_id": ObjectId(team_page_id),
        "competency": competency,
        "goal_text": goal_text,
        "achievement_rate": None,
        "achievement_note": None,
        "created_at": datetime.now(),
    })

    return jsonify({
        "success": True,
        "goal": {
            "_id": str(result.inserted_id),
            "competency": competency,
            "goal_text": goal_text,
        }
    })


@goals_bp.route("/api/goals/<goal_id>", methods=["PATCH"])
def update_goal(goal_id):
    data = request.json
    goal_text = data.get("goal_text", "").strip()

    goal = db.goals.find_one({"_id": ObjectId(goal_id)})
    if not goal:
        return jsonify({"error": "존재하지 않는 목표입니다"}), 404

    db.goals.update_one(
        {"_id": ObjectId(goal_id)},
        {"$set": {"goal_text": goal_text}})
    
    return jsonify({"success": True, "goal_text": goal_text})

@goals_bp.route("/api/goals/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = db.goals.find_one({"_id": ObjectId(goal_id)})
    if not goal:
        return jsonify({"error": "존재하지 않는 목표입니다"}), 404

    db.goals.delete_one({"_id": ObjectId(goal_id)})
    return jsonify({"success": True})

@goals_bp.route("/api/goals/<goal_id>/achievement", methods=["PATCH"])
def update_achievement(goal_id):
    goal = db.goals.find_one({"_id": ObjectId(goal_id)})
    if not goal:
        return jsonify({"error": "존재하지 않는 목표입니다"}), 404

    data = request.json
    achievement_rate = data.get("achievement_rate") # 값이 없으면 None이 됨 
    achievement_note = data.get("achievement_note", "").strip() # 값이 없으면 빈값으로 

    if achievement_rate not in [0, 25, 50, 75, 100]:
        return jsonify({"error": "달성률 값이 올바르지 않습니다"}), 400

    db.goals.update_one(
        {"_id": ObjectId(goal_id)},
        {"$set": {
            "achievement_rate": achievement_rate,
            "achievement_note": achievement_note,
        }}
    )
    
    return jsonify({
        "success": True,
        "achievement_rate": achievement_rate,
        "achievement_note": achievement_note,
    })