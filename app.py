from flask import Flask
from dotenv import load_dotenv
from routes.team import team_blueprints
from routes.auth import auth_bp


load_dotenv() # .env 파일 읽기

app = Flask(__name__) # Flask 애플리케이션 객체를 하나 생성
# __name__은 "지금 이 파일이 뭔지" 파이썬이 자동으로 넣어주는 값

for bp in team_blueprints:
    app.register_blueprint(bp)
    
app.register_blueprint(auth_bp)


# "이 파일을 직접 실행했을 때만" 아래 코드를 실행하라는 뜻
if __name__ == "__main__":
    app.run(debug=True) # 실제로 서버를 켜서 요청을 기다리기 시작 (http://127.0.0.1:5000)
