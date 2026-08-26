from flask import Blueprint, render_template, request
from routes.utils.jwt_utils import decode_token, jwt_required
from bson import ObjectId
from config import db

view_bp = Blueprint('team_view', __name__)

@view_bp.route("/team/<team_page_id>")
@jwt_required
def team_page(team_page_id):
    # current_user_id 하드코딩 제거하고 JWT 기반으로 수정 
    token = request.cookies.get("mytoken")
    payload = decode_token(token)

    if payload is None:
        return "인증이 필요합니다.", 401

    current_user = db.users.find_one({
        "email": payload["email"]
    })

    if current_user is None:
        return "사용자를 찾을 수 없습니다.", 404

    current_user_id = current_user["_id"]
    page = db.team_pages.find_one({"_id": ObjectId(team_page_id)}) 
    if not page:
        return "팀페이지를 찾을 수 없습니다", 404
    is_member = any(
        member["user_id"] == current_user_id
        for member in page.get("members", [])
    )

    if not is_member:
        return "해당 팀의 팀원이 아닙니다.", 403
    goals = list(db.goals.find({"team_page_id": ObjectId(team_page_id)}))
    scrums = list(db.scrums.find({"team_page_id": ObjectId(team_page_id)}).sort("created_at", -1)) #최신순 정렬 
    coretime = list(db.coretime.find({"team_page_id": ObjectId(team_page_id)}).sort("created_at", -1)) 
    wil = list(db.wil.find({"team_page_id": ObjectId(team_page_id)}))

    member_names = {m["user_id"]: m["name"] for m in page["members"]}
    print("member_names:", member_names)   # 여기 추가

    for s in scrums:
        print("scrum user_id:", s["user_id"], "→ str:", str(s["user_id"]))  # 이것도 추가
    return render_template("team_page.html",
        page=page,
        current_user_id=current_user_id,
        member_names=member_names,
        goals=goals,
        scrums=scrums,
        coretime=coretime,
        wil=wil,
    )