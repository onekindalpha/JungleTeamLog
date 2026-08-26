from flask import Blueprint, jsonify, request
from bson import ObjectId
from config import db 
from datetime import date, datetime

coretime_bf = Blueprint('coretime', __name__)

# 등록 
@coretime_bf.route("/api/team_pages/<team_page_id>/coretime", methods=["POST"])
def add_coretime(team_page_id):
    # http request에서 json data 가져오기 
    # request.json
    # Content-Type이 application/json이라는 헤더를 확인하고, 
    # 이 요청의 body를 JSON으로 해석해서 파이썬 dict로 만들어주는 flask 편의기능
    data = request.json
    problem = data.get("problem", "").strip()
    solution = data.get("solution", "").strip()
    if not (problem or solution):
        return jsonify({"error": "문제와 해결 방법을 모두 입력해주세요."}), 400

    # 현재 유저 정보 가져오기 
    current_user_id = ObjectId('6a8d72d4cd0d6b3be61313b7') #임시로 하드코딩, 추후 나중에 JWT에서 꺼내올 부분
    user = db.users.find_one({"_id": current_user_id})
    user_name = user["name"] if user else "알수없음"
    print(user_name)

    today = date.today().isoformat()

    # db에 넣기 
    result = db.coretime.insert_one({
        "team_page_id": ObjectId(team_page_id),
        "user_id": current_user_id,
        "problem": problem,
        "solution": solution,
        "log_date": today,
        "created_at": datetime.now(),
    })

    # http response 만들어 보내기 
    # jsonify
    # 파이썬 dict를 json 문자열로 변환 -> 문자열을 http body에 넣고 -> 헤더 붙이기 (Content-Type: application/json)
    return jsonify({
        "success": True,
        "coretime": {
            "_id": str(result.inserted_id),
            "problem": problem,
            "solution": solution,
            "log_date": today,
            "user_name": user_name,
        }
    })


# 수정
@coretime_bf.route("/api/coretime/<coretime_id>", methods=["PATCH"])
def update_coretime(coretime_id):
    # 존재하는지 확인  
    coretime = db.coretime.find_one({"_id": ObjectId(coretime_id)})
    if not coretime:
        return jsonify({"error": "존재하지 않는 글입니다"})

    # body 가져오기
    data = request.json
    problem = data.get("problem", "").strip()
    solution = data.get("solution", "").strip()

    # 수정
    result = db.coretime.update_one(
        {"_id": ObjectId(coretime_id)},
        {"$set":{"problem": problem, "solution": solution}}
    )

    #수정된 데이터 return
    return jsonify({"success": True, "problem": problem, "solution": solution})

# 삭제
@coretime_bf.route("/api/coretime/<coretime_id>", methods=["DELETE"])
def delete_coretime(coretime_id):
    # 존재하는지 확인 
    coretime = db.coretime.find_one({"_id": ObjectId(coretime_id)})
    if not coretime:
        return jsonify({"error": "존재하지 않는 글입니다"})

    # 삭제
    db.coretime.delete_one({"_id": ObjectId(coretime_id)})

    return jsonify({"success": True})