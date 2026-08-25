from flask import Blueprint, render_template

# Blueprint(...) — Flask에서 제공하는 클래스, 이걸 호출해서 "작은 미니 앱" 하나를 새로 만든다. 
#  team_view라는 이름의 미니 Flask 앱을 하나 만들어서, view_bp라는 변수에 담아둔다. 
#  이 미니 앱은 지금 이 파일(routes/team/view.py)에 속해있다는 걸 Flask가 인식하게 해둔다.
view_bp = Blueprint('team_view', __name__)

@view_bp.route("/team/<team_page_id>")
def team_page(team_page_id):
    return render_template("team_page.html")