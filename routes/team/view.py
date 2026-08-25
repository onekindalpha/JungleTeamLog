from flask import Blueprint, render_template
from datetime import datetime

# Blueprint(...) — Flask에서 제공하는 클래스, 이걸 호출해서 "작은 미니 앱" 하나를 새로 만든다. 
#  team_view라는 이름의 미니 Flask 앱을 하나 만들어서, view_bp라는 변수에 담아둔다. 
#  이 미니 앱은 지금 이 파일(routes/team/view.py)에 속해있다는 걸 Flask가 인식하게 해둔다.
view_bp = Blueprint('team_view', __name__)

@view_bp.route("/team/<team_page_id>")
def team_page(team_page_id):
    # 테스트 데이터
    current_user_id = "test_user_1234"
    page = {
        "_id": "page1",
        "week": 1,
        "team_number": 1,
        "team_name": "정글로그",
        "members": [
            {"user_id": "hong123", "name": "홍길동"},
            {"user_id": "kim456", "name": "김철수"},
        ],
        "curriculum": "알고리즘 기초, 자료구조",
        "created_at": datetime(2026, 8, 25),
    }
    goals = [
        {
            "_id": "goal1",
            "team_page_id": "page1",
            "competency": "구현",
            "goal_text": "알고리즘을 파이썬으로 구현할 수 있다",
            "achievement_rate": 70,
            "achievement_note": "재귀 부분이 아직 부족하다",
            "created_at": datetime(2026, 8, 24),
        },
        {
            "_id": "goal2",
            "team_page_id": "page1",
            "competency": "협업",
            "goal_text": "스크럼에서 막힌 부분 먼저 공유하기",
            "achievement_rate": None,  # 아직 미체크
            "achievement_note": None,
            "created_at": datetime(2026, 8, 24),
        },
    ]

    scrums = [
        {"_id": "s1", "team_page_id": "page1", "user_id": "hong123", "content": "로그인 마무리, 배포 준비", "log_date": "2026-08-25"},
        {"_id": "s2", "team_page_id": "page1", "user_id": "kim456", "content": "DB 설계 마무리", "log_date": "2026-08-25"},
        {"_id": "s3", "team_page_id": "page1", "user_id": "hong123", "content": "로그인 구현 시작", "log_date": "2026-08-24"},
        {"_id": "s4", "team_page_id": "page1", "user_id": "kim456", "content": "DB 설계", "log_date": "2026-08-24"},
        {"_id": "s5", "team_page_id": "page1", "user_id": "hong123", "content": "환경 세팅", "log_date": "2026-08-23"},
    ]

    coretime = [
        {"_id": "c1", "team_page_id": "page1", "user_id": "hong123", "problem": "git rebase 충돌", "solution": "(진행중) 아직 원인 파악 못함", "log_date": "2026-08-25"},
        {"_id": "c2", "team_page_id": "page1", "user_id": "kim456", "problem": "CORS 에러", "solution": "미들웨어 설정으로 해결", "log_date": "2026-08-25"},
        {"_id": "c3", "team_page_id": "page1", "user_id": "hong123", "problem": "재귀 부분에서 계속 막힘", "solution": "김철수가 그림으로 설명해줘서 이해함", "log_date": "2026-08-24"},
        {"_id": "c4", "team_page_id": "page1", "user_id": "kim456", "problem": "몽고DB 연결 안됨", "solution": "환경변수 오타 발견", "log_date": "2026-08-24"},
    ]

    wil = [
        {"_id": "w1", "team_page_id": "page1", "user_id": "hong123", "url": "blog.dev/week3"},
        {"_id": "w2", "team_page_id": "page1", "user_id": "kim456", "url": None},
    ]

    member_names = {m["user_id"]: m["name"] for m in page["members"]}

    return render_template("team_page.html",
        page=page,
        current_user_id=current_user_id,
        member_names=member_names,
        goals=goals,
        scrums=scrums,
        coretime=coretime,
        wil=wil,
    )