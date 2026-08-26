// 사용자가 주차를 선택하면 해당 주차의 팀 존재 여부를 확인
// 팀이 있으면 팀 페이지로, 없으면 팀 생성 페이지로 이동

// 홈 화면 JavaScript

// 1. 주차 선택 요소 가져오기
const weekSelect = document.getElementById("week-select");

// 2. 주차 선택 이벤트 등록 
// 사용자가 주차를 변경했을때 실행되도록
weekSelect.addEventListener("change", async () => {
  // 사용자가 주차를 변경했을 때 실행할 코드

    // 3. 사용자가 선택한 week 가져오기
    const week = Number(weekSelect.value);

    // 4. 선택한 week를 Flask의 팀 조회 API에 전달
    const response = await fetch(`/api/team_pages?week=${week}`);

    // 5. 서버 응답의 JSON 데이터 받기  
    const data = await response.json();

    // 6. 해당 주차에 내 팀이 있는지 확인
    if (data.team_page_id) {
        // 팀이 존재하면 해당 팀 페이지로 이동
        window.location.href = `/team/${data.team_page_id}`;
    }   else {
        // 팀이 없으면 선택한 week를 가지고 팀 생성 페이지로 이동
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

logoutButton.addEventListener("click", async() => {
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
