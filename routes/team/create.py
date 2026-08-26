# 팀 페이지 생성
# POST 요청 → JSON 데이터 받기 → 입력값 검증  → 팀 중복 확인 → 팀원 검증 → members 구성 → team_pages 저장  → 생성 결과 반환

# MongoDB 연결 구조와 인증 함수의 실제 import 경로는 기존 프로젝트 구조에 맞춰 확인 필요
from config import db
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template
from bson import ObjectId
# jwt_utils 추가
from routes.utils.jwt_utils import decode_token, jwt_required

# Flask Blueprint
create_bp = Blueprint("create", __name__)

# 팀페이지 생성 화면
@create_bp.route("/team/new", methods=["GET"])
@jwt_required
def team_create_page():

    week = request.args.get("week", type=int)

    if week is None or not (1 <= week <= 23):
        return "week 값이 올바르지 않습니다.", 400

    return render_template(
        "team_create.html",
        week=week
    )

# 팀 페이지 생성 API
@create_bp.route("/api/team_pages", methods=["POST"])
@jwt_required
def create_team_page():

    # 1. 요청 데이터 가져오기
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "요청 데이터가 필요합니다."
        }), 400

    # team_number 가져오기
    team_number = data.get("team_number")

    # team_name 가져오기
    team_name = data.get("team_name")

    # member_ids 가져오기
    member_ids = data.get("member_ids")

    # week 가져오기
    week = data.get("week")

    # 2. JWT에서 현재 로그인한 사용자 확인
    token = request.cookies.get("mytoken")
    payload = decode_token(token)

    if payload is None:
        return jsonify({
            "error": "인증이 필요합니다. "
        }), 401
    
    # JWT의 email로 현재 사용자 조회
    current_user = db.users.find_one({
        "email": payload["email"]
    })

    if current_user is None:
        return jsonify({
            "error": "현재 사용자를 찾을 수 없습니다."
        }), 404
    
    user_id = current_user["_id"]

    # 3. 입력값 검증

    # 팀 이름이 입력되었는지 확인
    if not team_name:
        return jsonify({
            "error": "팀 이름이 필요합니다."
        }), 400

    # 팀 번호가 1~4 사이의 정수인지 확인
    if not isinstance(team_number, int) or team_number not in [1, 2, 3, 4]:
        return jsonify({
            "error": "팀 번호가 올바르지 않습니다."
        }), 400

    # 팀원 목록이 배열인지 확인
    if not isinstance(member_ids, list):
        return jsonify({
            "error": "팀원 목록이 올바르지 않습니다."
        }), 400

    # week가 존재하는지 확인
    if week is None:
        return jsonify({
            "error": "week 값이 필요합니다."
        }), 400

    # week가 1~23 사이의 정수인지 확인
    if not isinstance(week, int) or not (1 <= week <= 23):
        return jsonify({
            "error": "week 값이 올바르지 않습니다. 1~23 사이의 정수여야 합니다."
        }), 400

    # 4. 같은 주차 + 같은 팀 번호가 이미 존재하는지 검사
    existing_team = db.team_pages.find_one({
        "week": week,
        "team_number": team_number
    })

    if existing_team:
        return jsonify({
            "error": "이미 존재하는 팀 페이지입니다."
        }), 409

    # 5. 선택된 팀원의 중복 검사
    if len(member_ids) != len(set(member_ids)):
        return jsonify({
            "error": "중복된 팀원이 있습니다."
        }), 400

    # 현재 주차의 기존 팀원 조회
    existing_teams = db.team_pages.find(
        {"week": week},
        {"members.user_id": 1}
    )

    # 현재 주차에 이미 소속된 사용자 ID 수집
    joined_user_ids = set()

    for team in existing_teams:
        for member in team.get("members", []):
            joined_user_ids.add(str(member["user_id"]))

    # 선택한 팀원 중 이미 다른 팀에 소속된 사용자가 있는지 확인
    for member_id in member_ids:
        if str(member_id) in joined_user_ids:
            return jsonify({
                "error": "이미 해당 주차의 다른 팀에 소속된 팀원이 있습니다."
            }), 409

    # 현재 화면에서는 본인이 자동 선택되지만
    # POST의 member_ids에는 현재 로그인 사용자가 포함되지 않아야 함
    if str(user_id) in [str(member_id) for member_id in member_ids]:
        return jsonify({
            "error": "현재 로그인한 사용자는 팀원 선택 목록에서 제외해야 합니다."
        }), 400

    # 6. members 구성
    members = []

    # 현재 로그인한 사용자를 members에 자동 추가
    members.append({
        "user_id": current_user["_id"],
        "name": current_user["name"]
    })

    # 선택한 팀원 조회 및 members에 추가
    for member_id in member_ids:

        # 선택한 user_id가 유효한 ObjectId인지 확인
        if not ObjectId.is_valid(member_id):
            return jsonify({
                "error": f"유효하지 않은 사용자 ID: {member_id}"
            }), 400

        # 선택한 user_id로 사용자 조회
        user = db.users.find_one({
            "_id": ObjectId(member_id)
        })

        # 존재하지 않는 사용자라면 생성 중단
        if not user:
            return jsonify({
                "error": f"사용자를 찾을 수 없습니다: {member_id}"
            }), 404

        # 확인된 사용자를 members에 추가
        members.append({
            "user_id": user["_id"],
            "name": user["name"]
        })

    # 7. 팀 페이지에 저장할 데이터 구성
    # MongoDB가 team_pages._id를 자동 생성
    team_page = {
        "week": week,
        "team_number": team_number,
        "team_name": team_name,
        "members": members,
        "created_at": datetime.now(timezone.utc)
    }

    # 8. MongoDB에 저장
    result = db.team_pages.insert_one(team_page)

    # 9. 팀 페이지 생성 결과 반환
    return jsonify({
        "message": "팀 페이지가 생성되었습니다.",
        "team_page_id": str(result.inserted_id)
    }), 201