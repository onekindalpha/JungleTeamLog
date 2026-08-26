from .view import view_bp
from .scrums import scrums_bp
from .create import create_bp
from .users import users_bp

# view.py, scrums.py, create.py, users.py의 Blueprint를 한곳에서 관리
# app.py에서는 team_blueprints를 가져와 일괄 등록

team_blueprints = [
    view_bp,
    scrums_bp,
    create_bp,
    users_bp
]