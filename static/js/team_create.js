// 현재 로그인한 사용자 ID
let currentUserId = null;

// 홈에서 URL로 전달받은 week 가져오기
const params = new URLSearchParams(window.location.search);
const week = Number(params.get("week"));

// 팀원 추가 버튼 요소
const addMemberButton = document.getElementById("add-member-button");

// 사용자 목록 표시 영역
const memberList = document.getElementById("member-list");

// 팀원 추가 버튼 클릭
addMemberButton.addEventListener("click", async () => {
    // 해당 주차에서 선택 가능한 사용자 목록 요청
    const response = await fetch(`/api/users?week=${week}`);
    const data = await response.json();

    // 기존 목록 초기화
    memberList.innerHTML = "";

    // 현재 로그인 사용자 ID 저장
    currentUserId = String(data.current_user_id);

    console.log("currentUserId:", currentUserId);
    console.log("users:", data.users);

    // 사용자 목록 생성
    data.users.forEach((user) => {
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = String(user.user_id);

        // 현재 로그인한 사용자
        // 자동 선택 + 해제 불가
        if (String(user.user_id) === currentUserId) {
            checkbox.checked = true;
            checkbox.disabled = true;
        }

        const label = document.createElement("label");
        label.textContent = user.name;
        label.prepend(checkbox);

        memberList.appendChild(label);
    });

});


// 팀 생성 버튼
const createTeamButton = document.getElementById("create-team-button");

// 팀 생성 버튼 클릭
createTeamButton.addEventListener("click", async () => {

    const teamNumber = Number(
        document.getElementById("team-number").value
    );

    const teamName = document.getElementById("team-name").value;

    // 선택된 체크박스
    const checkedMembers = document.querySelectorAll(
        '#member-list input[type="checkbox"]:checked'
    );

    // 선택한 다른 팀원 ID 저장
    const memberIds = [];

    checkedMembers.forEach((checkbox) => {

        // 본인은 제외
        // 서버에서 자동 추가
        if (String(checkbox.value) !== currentUserId) {
            memberIds.push(String(checkbox.value));
        }
    });

    // 본인 포함 총 팀원 수
    const totalMembers = memberIds.length + 1;

    // 최소 2명 체크
    if (totalMembers < 2) {
        alert("팀원은 최소 2명 이상이어야 합니다.");
        return;
    }


    const requestData = {
        team_number: teamNumber,
        team_name: teamName,
        week: week,
        member_ids: memberIds
    };

    console.log("team create data:", requestData);
    const response = await fetch("/api/team_pages", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    });

    const data = await response.json();
    if (response.ok) {
        window.location.href =
            `/team/${data.team_page_id}`;
    } else {
        alert(data.error);
    }
});

// 취소 버튼
const cancelButton = document.getElementById("cancel-button");

// 취소 버튼 클릭
cancelButton.addEventListener("click", () => {
    window.history.back();

});