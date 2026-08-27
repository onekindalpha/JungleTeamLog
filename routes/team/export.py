from flask import Blueprint, render_template, request, redirect, make_response, g
from bson import ObjectId

from config import db
from ..utils.jwt_utils import jwt_required
from weasyprint import HTML
export_bp = Blueprint("export", __name__)


@export_bp.route("/export/team/<team_page_id>/pdf")
@jwt_required
def export_team_pdf(team_page_id):

    page = db.team_pages.find_one({
        "_id": ObjectId(team_page_id)
    })

    if not page:
        return "팀페이지를 찾을 수 없습니다", 404

    current_user_id = ObjectId(
        g.user["user_id"]
    )

    # 현재 사용자가 이 팀의 멤버인지 확인
    member_ids = [
        m["user_id"]
        for m in page["members"]
    ]

    if current_user_id not in member_ids:
        return "접근 권한이 없습니다", 403

    # Goal
    goals = list(
        db.goals.find({
            "team_page_id": ObjectId(team_page_id)
        })
    )

    # Scrum
    scrums = list(
        db.scrums.find({
            "team_page_id": ObjectId(team_page_id)
        }).sort(
            "created_at",
            -1
        )
    )

    # CoreTime
    coretime = list(
        db.coretime.find({
            "team_page_id": ObjectId(team_page_id)
        }).sort(
            "created_at",
            -1
        )
    )

    # WIL
    wil = list(
        db.wil.find({
            "team_page_id": ObjectId(team_page_id)
        })
    )

    wil_map = {
        w["user_id"]: w["url"]
        for w in wil
    }

    member_names = {
        m["user_id"]: m["name"]
        for m in page["members"]
    }

    # PDF용 HTML
    html = render_template(
        "team_page.html",
        page=page,
        current_user_id=current_user_id,
        member_names=member_names,
        goals=goals,
        scrums=scrums,
        coretime=coretime,
        wil_map=wil_map,
        pdf=True
    )

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f"attachment; filename=week_{page['week']}_team_{page['team_number']}.pdf"
    )

    return response