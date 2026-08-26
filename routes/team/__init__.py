from .view import view_bp
from .scrums import scrums_bp
from .coretime import coretime_bf
# view.py, goals.py 등: 각자 독립적인 라우트를 담고 있음 (합쳐지지 않음)
# __init__.py: 그 파일들을 한군데 모아서 리스트로 정리만 함 (일종의 "목차" 역할)
# app.py: 그 리스트를 가져와서 for문으로 각각 따로 등록 (__init__.py가 없다면 app.py는 지저분해짐)

team_blueprints = [view_bp, scrums_bp, coretime_bf]