import hashlib
from config import db


users = [
    {"name": "테스트1", "email": "test1@test.com"},
    {"name": "테스트2", "email": "test2@test.com"},
    {"name": "테스트3", "email": "test3@test.com"},
    {"name": "테스트4", "email": "test4@test.com"},
    {"name": "테스트5", "email": "test5@test.com"},
    {"name": "테스트6", "email": "test6@test.com"},
    {"name": "테스트7", "email": "test7@test.com"},
    {"name": "테스트8", "email": "test8@test.com"},
    {"name": "테스트9", "email": "test9@test.com"},
    {"name": "테스트10", "email": "test10@test.com"},
]


password = "1234"

pw_hash = hashlib.sha256(
    password.encode("utf-8")
).hexdigest()


for user in users:
    exists = db.users.find_one({
        "email": user["email"]
    })

    if exists:
        print("이미 존재:", user["email"])
        continue

    db.users.insert_one({
        "name": user["name"],
        "email": user["email"],
        "password_hash": pw_hash
    })

    print("생성:", user["email"])


print("완료")