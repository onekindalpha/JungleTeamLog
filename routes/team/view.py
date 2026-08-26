from flask import Blueprint, render_template
from bson import ObjectId
from config import db

view_bp = Blueprint('team_view', __name__)

@view_bp.route("/team/<team_page_id>")
def team_page(team_page_id):
    current_user_id = ObjectId('6a8d72d4cd0d6b3be61313b7')

    page = db.team_pages.find_one({"_id": ObjectId(team_page_id)}) 
    if not page:
        return "팀페이지를 찾을 수 없습니다", 404

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