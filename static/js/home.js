// 사용자가 주차를 선택하면 해당 주차의 팀 존재 여부를 확인
// 팀이 있으면 팀 페이지로, 없으면 팀 생성 페이지로 이동

// 홈 화면 JavaScript

// 1. 주차 선택 요소 가져오기
const weekSelect = document.getElementById("week-select");

// 2. 주차 선택 이벤트 등록
// 사용자가 주차를 변경했을 때 실행
weekSelect.addEventListener("change", () => {

    // 선택한 week 가져오기
    const week = Number(weekSelect.value);

    // 서버가 홈 화면에 내려준 해당 주차의 team_page_id 사용
    const teamPageId = weekTeams[week];

    if (teamPageId) {

        // 팀이 존재하면 해당 팀 페이지로 이동
        window.location.href = `/team/${teamPageId}`;

    } else {

        // 팀이 없으면 팀 생성 페이지로 이동
        window.location.href = `/team/new?week=${week}`;
    }
});

// 7. MY WIL 버튼 클릭
const myWilButton = document.getElementById("my-wil-button");

myWilButton.addEventListener("click", () => {

    // My WIL 페이지로 이동
    window.location.href = "/my/wil";
});

// 8. 로그아웃 버튼 클릭
const logoutButton = document.getElementById("logout-button");

logoutButton.addEventListener("click", async () => {

    // 로그아웃 API 요청
    const response = await fetch("/api/auth/logout", {
        method: "POST"
    });

    // 로그아웃 성공 여부 확인
    if (response.ok) {

        // 로그인 페이지로 이동
        window.location.href = "/login";

    } else {

        // 로그아웃 실패
        alert("로그아웃에 실패했습니다.");
    }
});