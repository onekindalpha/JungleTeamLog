# seed.py (테스트 데이터 한 번만 넣는 임시 스크립트)
from config import db
from bson import ObjectId
from datetime import datetime

# 유저 2명
hong_id = db.users.insert_one({
    "email": "hong@test.com", "password_hash": "temp", "name": "홍길동", "created_at": datetime.now()
}).inserted_id

kim_id = db.users.insert_one({
    "email": "kim@test.com", "password_hash": "temp", "name": "김철수", "created_at": datetime.now()
}).inserted_id

# 팀페이지 1개
page_id = db.team_pages.insert_one({
    "week": 1, "team_number": 1, "team_name": "1팀",
    "members": [
        {"user_id": hong_id, "name": "홍길동"},
        {"user_id": kim_id, "name": "김철수"},
    ],
    "curriculum": "알고리즘 기초, 자료구조",
    "created_at": datetime.now(),
}).inserted_id

# 목표 2개 (팀 공유)
db.goals.insert_many([
    {"team_page_id": page_id, "competency": "구현", "goal_text": "알고리즘을 파이썬으로 구현할 수 있다",
     "achievement_rate": 70, "achievement_note": "재귀 부분이 아직 부족하다", "created_at": datetime.now()},
    {"team_page_id": page_id, "competency": "협업", "goal_text": "스크럼에서 막힌 부분 먼저 공유하기",
     "achievement_rate": None, "achievement_note": None, "created_at": datetime.now()},
])

# 스크럼 몇 개
db.scrums.insert_many([
    {"team_page_id": page_id, "user_id": hong_id, "content": "로그인 마무리, 배포 준비", "log_date": "2026-08-25", "created_at": datetime.now()},
    {"team_page_id": page_id, "user_id": kim_id, "content": "DB 설계 마무리", "log_date": "2026-08-25", "created_at": datetime.now()},
])

# 코어타임 몇 개
db.coretime.insert_many([
    {"team_page_id": page_id, "user_id": hong_id, "problem": "git rebase 충돌", "solution": "(진행중) 아직 원인 파악 못함", "log_date": "2026-08-25", "created_at": datetime.now()},
])

# WIL 하나
db.wil.insert_one({"team_page_id": page_id, "user_id": hong_id, "url": "blog.dev/week3", "created_at": datetime.now()})

print(f"생성된 team_page_id: {page_id}")
print(f"확인용 URL: /team/{page_id}")