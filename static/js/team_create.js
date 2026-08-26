// 현재 로그인한 사용자 ID를 저장할 변수 (나중에 서버 응답값으로 채워짐)
let currentUserId = null;

// 홈에서 URL로 전달받은 week 가져오기 (URL Query String에서 추출)
const params = new URLSearchParams(window.location.search);
const week = Number(params.get("week"));

// 팀원 추가 버튼 요소 (HTML DOM 요소- 팀원 추가 버튼, 멤버 출력 영역)
const addMemberButton = document.getElementById("add-member-button");

// 사용자 목록 표시 영역
const memberList = document.getElementById("member-list");

// 팀원 추가 버튼 클릭
addMemberButton.addEventListener("click", async () => {
    // 해당 주차에서 선택 가능한 사용자(팀이 없는) 목록 요청
    const response = await fetch(`/api/users?week=${week}`);
    const data = await response.json();

    // 다시 클릭했을 때 중복 추가 방지 위한 기존 목록 초기화
    memberList.innerHTML = "";

    // 서버가 응답해준 현재 로그인 사용자 ID룰 문자열로 변환하여 저장
    currentUserId = String(data.current_user_id);

    console.log("currentUserId:", currentUserId);
    console.log("users:", data.users);

    // 받아온 사용자 목록(data.users)을 순회하며 체크박스 UI 생성
    data.users.forEach((user) => {
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = String(user.user_id);

        // 현재 로그인한 '나' 자신인 경우 본인이므로 기본 체크 (true), 그리고
        // 자동 선택 + 해제 불가
        if (String(user.user_id) === currentUserId) {
            checkbox.checked = true;
            checkbox.disabled = true;
        }
        // 이름 표기용 Label 생성 후 체크박스를 안에 집어넣고 목록에 추가
        const label = document.createElement("label");
        label.textContent = user.name;
        label.prepend(checkbox);

        memberList.appendChild(label);
    });

});

// 팀 생성 버튼
const createTeamButton = document.getElementById("create-team-button");

// 팀 생성 버튼 클릭
// 팀 생성 버튼 클릭
createTeamButton.addEventListener("click", async () => {
    // 입력 필드값 가져오기
    const teamNumber = Number(document.getElementById("team-number").value);
    const teamName = document.getElementById("team-name").value.trim();

    // 1. [기본 유효성 검사] 팀 번호 및 팀 이름 입력 체크
    if (!teamNumber || teamNumber <= 0) {
        alert("올바른 팀 번호를 입력해주세요.");
        return;
    }
    if (!teamName) {
        alert("팀 이름을 입력해주세요.");
        return;
    }

    // 2. 체크박스가 선택된 팀원 목록 가져오기
    const checkedMembers = document.querySelectorAll(
        '#member-list input[type="checkbox"]:checked'
    );

    // 선택된 다른 팀원들의 ID 담을 배열
    const memberIds = [];

    checkedMembers.forEach((checkbox) => {
        const selectedId = String(checkbox.value);
        
        // 체크되어 있는 사람 중 '나 자신'은 제외하고 pure 팀원만 추가
        // (서버 백엔드에서 생성자 본인은 자동으로 팀원에 넣어주기 때문)
        if (currentUserId && selectedId !== String(currentUserId)) {
            memberIds.push(selectedId);
        }
    });

    // 3. 총 팀원 수 계산 (로그인한 나 자신 1명 + 내가 체크해서 선택한 다른 팀원 수)
    const totalMembers = memberIds.length + 1;

    console.log("총 팀원 수:", totalMembers, "(나 포함)");

    // 4. [핵심 유효성 검사] 최소 2명 이상인지 체크 (다른 팀원을 최소 1명 이상 선택해야 함)
    if (totalMembers < 2) {
        alert("팀원은 최소 2명 이상이어야 합니다. 팀원을 선택해주세요!");
        return;
    }

    // 서버 API로 보낼 JSON 데이터 객체
    const requestData = {
        team_number: teamNumber,
        team_name: teamName,
        week: week,
        member_ids: memberIds
    };

    console.log("팀 생성 요청 데이터:", requestData);

    try {
        const response = await fetch("/api/team_pages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (response.ok) {
            // 성공 시 생성된 팀 페이지로 이동
            window.location.href = `/team/${data.team_page_id}`;
        } else {
            alert(data.error || "팀 생성에 실패했습니다.");
        }
    } catch (error) {
        alert("서버와 통신 중 에러가 발생했습니다.");
    }
});

// 취소 버튼
const cancelButton = document.getElementById("cancel-button");

// 취소 버튼 클릭하면 브라우저의 이전 페이지로 이동. 
cancelButton.addEventListener("click", () => {
    window.history.back();

});