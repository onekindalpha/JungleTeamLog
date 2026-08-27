from flask import Blueprint, render_template, request, jsonify, g, redirect

from bson import ObjectId

from config import db

from ..utils.jwt_utils import jwt_required


view_bp = Blueprint('team_view', __name__)


@view_bp.route("/team/<team_page_id>")
@jwt_required
def team_page(team_page_id):

    page = db.team_pages.find_one(
        {
            "_id": ObjectId(team_page_id)
        }
    )

    if not page:
        return "팀페이지를 찾을 수 없습니다", 404


    current_user_id = ObjectId(
        g.user["user_id"]
    )


    member_ids = [
        m["user_id"]
        for m in page["members"]
    ]


    if current_user_id not in member_ids:
        return "접근 권한이 없습니다", 403


    goals = list(
        db.goals.find(
            {
                "team_page_id": ObjectId(team_page_id)
            }
        )
    )


    scrums = list(
        db.scrums.find(
            {
                "team_page_id": ObjectId(team_page_id)
            }
        ).sort(
            "created_at",
            -1
        )
    )


    coretime = list(
        db.coretime.find(
            {
                "team_page_id": ObjectId(team_page_id)
            }
        ).sort(
            "created_at",
            -1
        )
    )


    wil = list(
        db.wil.find(
            {
                "team_page_id": ObjectId(team_page_id)
            }
        )
    )


    wil_map = {
        w["user_id"]: w["url"]
        for w in wil
    }


    member_names = {
        m["user_id"]: m["name"]
        for m in page["members"]
    }


    return render_template(
        "team_page.html",
        page=page,
        current_user_id=current_user_id,
        member_names=member_names,
        goals=goals,
        scrums=scrums,
        coretime=coretime,
        wil_map=wil_map
    )



# =========================
# 팀 수정 페이지
# =========================

@view_bp.route("/team/edit/<team_page_id>")
@jwt_required
def edit_team(team_page_id):

    page = db.team_pages.find_one(
        {
            "_id": ObjectId(team_page_id)
        }
    )


    if not page:
        return "팀 페이지를 찾을 수 없습니다", 404



    # 현재 팀원
    current_member_ids = [
        m["user_id"]
        for m in page["members"]
    ]


    # 같은 주차 다른 팀에 들어간 사람
    joined_user_ids = []


    same_week_teams = db.team_pages.find(
        {
            "week": page["week"],
            "_id": {
                "$ne": page["_id"]
            }
        }
    )


    for team in same_week_teams:

        for member in team["members"]:

            joined_user_ids.append(
                member["user_id"]
            )



    # 추가 불가능한 사람
    excluded_ids = list(
        set(
            current_member_ids
            +
            joined_user_ids
        )
    )



    # 추가 가능한 사람
    available_members = list(
        db.users.find(
            {
                "_id": {
                    "$nin": excluded_ids
                }
            }
        )
    )


    return render_template(
        "team_edit.html",
        page=page,
        available_members=available_members
    )



# =========================
# 팀원 추가 저장
# =========================

@view_bp.route(
    "/team/edit/<team_page_id>",
    methods=["POST"]
)
@jwt_required
def update_team(team_page_id):


    selected_member_ids = request.form.getlist(
        "member_ids"
    )


    page = db.team_pages.find_one(
        {
            "_id": ObjectId(team_page_id)
        }
    )


    if not page:
        return "팀 페이지 없음", 404



    # 현재 팀원
    current_member_ids = [
        m["user_id"]
        for m in page["members"]
    ]



    # 같은 주차 다른 팀원 검증
    joined_user_ids = []


    same_week_teams = db.team_pages.find(
        {
            "week": page["week"],
            "_id": {
                "$ne": page["_id"]
            }
        }
    )


    for team in same_week_teams:

        for member in team["members"]:

            joined_user_ids.append(
                member["user_id"]
            )



    allowed_ids = set(
        selected_member_ids
    )


    new_members = []



    for member_id in allowed_ids:

        if not ObjectId.is_valid(member_id):
            continue

        user_id = ObjectId(member_id)


        # 이미 팀에 있음
        if user_id in current_member_ids:
            continue


        # 다른 팀에 있음
        if user_id in joined_user_ids:
            continue



        user = db.users.find_one(
            {
                "_id": user_id
            }
        )


        if user:

            new_members.append(
                {
                    "user_id": user["_id"],
                    "name": user["name"]
                }
            )



    if new_members:

        db.team_pages.update_one(

            {
                "_id": ObjectId(team_page_id)
            },

            {
                "$push":
                {
                    "members":
                    {
                        "$each": new_members
                    }
                }
            }

        )


    return redirect(
        f"/team/{team_page_id}"
    )



# =========================
# 팀 삭제
# =========================

@view_bp.route(
    "/team/delete/<team_page_id>",
    methods=["POST"]
)
@jwt_required
def delete_team(team_page_id):


    db.team_pages.delete_one(
        {
            "_id": ObjectId(team_page_id)
        }
    )


    return redirect("/")



# =========================
# 커리큘럼 수정
# =========================

@view_bp.route(
    "/api/team_pages/<team_page_id>/curriculum",
    methods=["PATCH"]
)
def update_curriculum(team_page_id):


    data = request.json


    curriculum = data.get(
        "curriculum",
        ""
    ).strip()



    if not curriculum:

        return jsonify(
            {
                "error":
                "커리큘럼을 입력해주세요"
            }
        ),400



    db.team_pages.update_one(

        {
            "_id": ObjectId(team_page_id)
        },

        {
            "$set":
            {
                "curriculum": curriculum
            }
        }

    )


    return jsonify(
        {
            "success": True,
            "curriculum": curriculum
        }
    )