from flask import Blueprint, render_template, request
from routes.utils.jwt_utils import decode_token, jwt_required
from bson import ObjectId
from config import db
# 팀 페이지 화면 렌더링 라우트.
view_bp = Blueprint('team_view', __name__)
# 라우트 선언 및 사용자 인증
@view_bp.route("/team/<team_page_id>")
@jwt_required # 로그인한 사용자만 접근 가능하도록 JWT 토큰 검증
def team_page(team_page_id):
    token = request.cookies.get("mytoken")
    payload = decode_token(token)

    if payload is None:
        return "인증이 필요합니다.", 401
    # 토큰의 이메일 정보로 DB에서 현재 로그인한 사용자 정보 조회
    current_user = db.users.find_one({"email": payload["email"]})
    if current_user is None:
        return "사용자를 찾을 수 없습니다.", 404

    # 현재 로그인 유저 정보 추출 
    current_user_id = str(current_user["_id"])
    current_user_name = current_user.get("name") or current_user.get("username") or "팀원"
    
    # URL로 전달받은 ID로 해당 주차의 팀 페이지 DB 조회
    page = db.team_pages.find_one({"_id": ObjectId(team_page_id)}) 
    if not page:
        return "팀페이지를 찾을 수 없습니다", 404
        
    # 팀원 권한 검사 - 현재 로그인한 유저가 해당 주차 팀의 팀원인지 확인 
    is_member = any(
        str(member.get("user_id")) == current_user_id
        for member in page.get("members", [])
        if member.get("user_id")
    )

    if not is_member:
        return "해당 팀의 팀원이 아닙니다.", 403

    # 관련 데이터 DB 조회 및 이름 맵 생성 - 해당 팀페이지에 속한 애들 조회
    goals = list(db.goals.find({"team_page_id": ObjectId(team_page_id)}))
    scrums_raw = list(db.scrums.find({"team_page_id": ObjectId(team_page_id)}).sort("created_at", -1))
    coretime_raw = list(db.coretime.find({"team_page_id": ObjectId(team_page_id)}).sort("created_at", -1)) 
    wil = list(db.wil.find({"team_page_id": ObjectId(team_page_id)}))

    # 유저 이름 맵 생성하는 이유: MongodDB의 ObjectId말고 실제 이름 표시 위함
    member_names = {
        str(m.get("user_id")): m.get("name") 
        for m in page.get("members", []) 
        if m.get("user_id")
    }

    # 스크럼 데이터 가공 (작성자 이름 및 수정/삭제 권한 여부 부여)
    scrums = []
    for s in scrums_raw:
        s_user_id = str(s.get("user_id", "")) if s.get("user_id") else ""
        # 작성자 이름 탐색 (이름 맵 -> 문서 내 이름 -> DB 직접 조회 순)
        author_name = member_names.get(s_user_id) or s.get("user_name")
        if not author_name and s_user_id and ObjectId.is_valid(s_user_id):
            u = db.users.find_one({"_id": ObjectId(s_user_id)})
            if u:
                author_name = u.get("name") or u.get("username")
        # 현재 로그인 유저가 작성자인 경우 is_author를 True로 설정 (수정/삭제)
        author_name = author_name or current_user_name
        is_author = (s_user_id == current_user_id) or (s_user_id == "")

        s["author_name"] = author_name
        s["is_author"] = is_author
        scrums.append(s)

    # 코어타임 데이터 가공 (작성자 이름 및 수정/삭제 권한 부여))
    coretime = []
    for c in coretime_raw:
        c_user_id = str(c.get("user_id", "")) if c.get("user_id") else ""
        c["author_name"] = member_names.get(c_user_id) or c.get("user_name") or current_user_name
        c["is_author"] = (c_user_id == current_user_id) or (c_user_id == "")
        coretime.append(c)
    # 가공된 모든 데이터를 team_page.html 템플릿에 전달하여 화면 렌더링 
    return render_template("team_page.html",
        page=page,
        current_user_id=current_user_id,
        member_names=member_names,
        goals=goals,
        scrums=scrums,
        coretime=coretime,
        wil=wil,
    )