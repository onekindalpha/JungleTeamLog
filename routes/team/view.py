from flask import Blueprint, render_template, request, jsonify, g
from bson import ObjectId
from config import db
from ..utils.jwt_utils import jwt_required

view_bp = Blueprint('team_view', __name__)

@view_bp.route("/team/<team_page_id>")
@jwt_required
def team_page(team_page_id):
    # 있는 페이지인지 확인 
    page = db.team_pages.find_one({"_id": ObjectId(team_page_id)}) 
    if not page:
        return "팀페이지를 찾을 수 없습니다", 404

    # 해당 페이지의 멤버인지 확인 
    current_user_id = ObjectId(g.user["user_id"])
    member_ids = [m["user_id"] for m in page["members"]]
    if current_user_id not in member_ids:
        return "접근 권한이 없습니다", 403

    goals = list(db.goals.find({"team_page_id": ObjectId(team_page_id)}))
    scrums = list(db.scrums.find({"team_page_id": ObjectId(team_page_id)}).sort("created_at", -1)) #최신순 정렬 
    coretime = list(db.coretime.find({"team_page_id": ObjectId(team_page_id)}).sort("created_at", -1)) 
    wil = list(db.wil.find({"team_page_id": ObjectId(team_page_id)}))
    wil_map = {w["user_id"] : w["url"] for w in wil}
    member_names = {m["user_id"]: m["name"] for m in page["members"]}

    return render_template("team_page.html",
        page=page,
        current_user_id=current_user_id,
        member_names=member_names,
        goals=goals,
        scrums=scrums,
        coretime=coretime,
        wil_map=wil_map,
    )

@view_bp.route("/api/team_pages/<team_page_id>/curriculum", methods=["PATCH"])
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