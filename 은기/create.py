# 팀 페이지 생성
# 요청 데이터 -> 사용자 조회-> members구성-> team_pages 저장
# POST 요청 -> JSON 받기 -> 값 꺼내기 -> MongoDB에 저장 -> 응답
# (중요) MONGODB 연결 구조 확인 후 mongo import 방식 결정
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from bson import ObjectId

# Flask Blueprint구조를 통해 작성하는 것이 좋다고 함
create_bp = Blueprint('create', __name__)
@create_bp.route('/api/team_pages', methods=['POST'])

# 이걸 app.py에 연결할 때는 아래처럼 한다고 함. 
# from routes.create import create_bp
# app.register_blueprint(create_bp)라고 함.

def create_team_page():
    # 1. 요청 데이터 가져오는 부분. request에서 JSON 데이터 받기
    data = request.get_json()
    if not data:
        return jsonify({
            'error': '요청 데이터가 필요합니다.'
        }), 400
    # team_number 가져오기
    team_number = data.get('team_number')
    # team_name 가져오기
    team_name = data.get('team_name')
    # 멤버스를 가져오기
    member_ids = data.get("member_ids")
    # week를 가져오기
    week = data.get("week")

    # 이 부분 꼭 확인해야 함. !
    # 2. (협업 관련 중요사항 ) JWT 인증으로 user_id를 가져오기 ? 이 부분 앞의 호환성 확인해야 함. 
    user_id = get_current_user_id()
    
    # user_id가 유효한 ObjectId인지 확인
    if not ObjectId.is_valid(user_id):
        return jsonify({
            'error': '유효하지 않은 사용자 ID입니다.'
        }), 400
    # 3. 기본값 검사:
    # 팀 이름이 입력되었는지 확인
    if not team_name:
        return jsonify({'error': '팀 이름이 필요합니다.'}), 400
    # 문자열 1이 들어오지 않도록 하는 것까지 포함함. 
    if not isinstance(team_number, int) or team_number not in [1,2,3,4]:
        return jsonify({'error': '팀 번호가 올바르지 않습니다.'}), 400
    
    if not isinstance(member_ids, list):
        return jsonify({'error': '팀원 목록이 올바르지 않습니다.'}), 400
    # week도 검사
    if week is None:
        return jsonify({'error': 'week 값이 필요합니다.'}), 400
    if not isinstance(week, int) or not (1 <= week <=23):
        return jsonify({'error': 'week 값이 올바르지 않습니다. 1~23 사이의 정수여야 합니다.'}), 400 

    # 같은 주차 + 같은 팀 번호가 이미 존재하는지 검사
    existing_team = mongo.db.team_pages.find_one({
    "week": week,
    "team_number": team_number
    })
    if existing_team:
        return jsonify({'error': '이미 존재하는 팀 페이지입니다.'}), 409
    
    # 선택된 팀원이 현재 주차의 다른 팀에 이미 소속되어있는지 확인
    existing_teams = mongo.db.team_pages.find(
        {"week": week},
        {"members.user_id":1}
    )
    # 중복제거 하기 위한 set로 포함
    joined_user_ids = set()
    for team in existing_teams:
        # 만약 멤버가 이미 다른 팀에 소속되어있다면
        for member in existing_teams:
            if str(member_id) in joined_user_ids:
                return jsonify({
                    'error': '이미 해당 주차에 소속된 팀원이 있습니다.'
                }), 409
            
    # 선택된 팀원의 중복 검사
    if len(member_ids) != len(set(member_ids)):
        return jsonify({'error': '중복된 팀원이 있습니다.'}), 400
    # 현재 화면에서 본인 자동추가되고, members_ids는 선택한 팀원이니까 서버에서도 막도록 함
    if user_id in member_ids:
        return jsonify({'error': '현재 로그인한 사용자는 팀원 선택에서 제외해야 합니다.'}), 400 

    # 5. members 구성은 현재 사용자 랑 선택된 팀원
    members = []
    # 현재 로그인한 사용자는 자동으로 멤버로 추가
    current_user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    # 그리고 JWT에서 나온 user_id가 실제 users에 존재하는지 확인하는 과정
    if not current_user:
        return jsonify({'error': '현재 사용자를 찾을 수 없습니다.'}), 404
   # 그 다음에 멤버스에 추가한다. 
    members.append({
        "user_id": current_user['_id'],
        "name": current_user['name'],
    })
    
    # 선택한 팀원을 추가하는 과정이 다음으로 와야 함. 
    # 각 멤버 아이디가 멤버스에 존재하는지 확인
    for member_id in member_ids:
        if not ObjectId.is_valid(member_id):
            return jsonify({'error': f'유효하지 않은 사용자 ID: {member_id}'}), 400
        # 선택한 팀원 ID로 사용자 조회
        user = mongo.db.users.find_one({'_id': ObjectId(member_id)})
        # 존재하지 않는 사용자라면 생성 중단 
        if not user:
            return jsonify({'error': f'사용자를 찾을 수 없습니다: {member_id}'}), 404
        # 여기까지 오면 멤버스에 추가하도록 한다. 
        members.append({
            "user_id": user['_id'],
            "name": user['name'],
        })
        
    # 6. 만약에 여기까지 조회가 되었다면 팀 페이지를 생성할 요소들을 정하고. 
    # 팀 페이지 생성할때 에 근데 team_id는 자동으로 생성되는 _id를 사용하면 됨. 자동으로 생성되었는데 왜 안하지. 
    team_page = {
        'week': week,
        'team_number': team_number,
        'team_name': team_name,
        'members': members,
        'created_at': datetime.now(timezone.utc)
    }

    # 6. MongoDB에 저장
    result = mongo.db.team_pages.insert_one(team_page)
    # 7. 그다음에 팀페이지 생성되었음을 이야기하기. 
    return jsonify({'message': '팀 페이지가 생성되었습니다.', 'team_page_id': str(result.inserted_id)}), 201

# 협업 관련 사전 확인: MongoDB 연결 변수, JWT 인증 함수, Blueprint 구조, app.py에서 Blueprint 등록 방식

# create.py 에서 POST /api/team_pages
# team_createe.html은 최소 UI
# team_create.js 선택 + AJAX 요청
# 실제 실행은 화면-> AJAX -> Flask -> MongoDB


# 고민했던 지점: week를 클라이언트가 보내는지 아니면 홈에서 선택한 주차를 서버가 이미 알고 있는지. 
# 고민 했던 지점과 해결한 지점: week는 단순 사용자 입력값이 아니라 홈에서 선택한 주차와 일치해야 하니까 서버에서 검증해야 함. 
