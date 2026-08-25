# app.py: 앱 생성 + .env 로드 + 각 담당자가 만든 blueprint들을 모아서 등록

from flask import Flask
from dotenv import load_dotenv
from routes.team import team_blueprints

load_dotenv() # .env 파일 읽기

app = Flask(__name__) # Flask 애플리케이션 객체를 하나 생성
# __name__은 "지금 이 파일이 뭔지" 파이썬이 자동으로 넣어주는 값

for bp in team_blueprints:
    app.register_blueprint(bp)

@app.route("/") # 라우팅 등록 (테스트용 라우터임)
def home():
    return "Hello Jungle!"

# "이 파일을 직접 실행했을 때만" 아래 코드를 실행하라는 뜻
if __name__ == "__main__":
    app.run(debug=True) # 실제로 서버를 켜서 요청을 기다리기 시작 (http://127.0.0.1:5000)
    # debug=True : 개발 중에 편하라고 켜두는 옵션
    # 코드를 수정하고 저장하면 서버가 자동으로 재시작되고, 에러 나면 브라우저 화면에 자세한 에러 내용을 보여준다
    # 배포할 때는 보안상 False로 바꾸거나 아예 빼야 함