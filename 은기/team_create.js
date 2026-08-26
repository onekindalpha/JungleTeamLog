// 현재 로그인한 사용자 ID
let currentUserId = null;
// 홈에서 URL로 전달받은 week 가져오기
// URL의 ?week=<week>값을 읽음
const params = new URLSearchParams(window.location.search);
const week = Number(params.get("week"));

// 팀원 추가 버튼 요소를 team_create.html에서 가져오기
const addMemberButton = document.getElementById("add-member-button");

// 사용자 목록을 표시할 영역을 team_create.html에서 가져오기 - member-list라는 빈 컨테이너를 가져옴
const memberList = document.getElementById("member-list");

// 팀원 추가 버튼 클릭
addMemberButton.addEventListener("click", async () => {
  // 여기에 AJAX w조회 코드 작성
  // Flask에 해당 주차에 선택 가능한 사용자 목록 요청
  const response = await fetch(`/api/users?week=${week}`);
 
  // 서버응답 받기
  // Json으로 선택 가능한 사용자 목록 받기
  const data = await response.json();

  // 기존 목록 초기화
  memberList.innerHTML = "";

// 서버에서 받은 현재 로그인 사용자의 user_id 저장
currentUserId = data.current_user_id;

  // 사용자 목록을 한 명씩 처리
  data.users.forEach((user) => {
  // 사용자 한 명의 화면 요소 생성
  // <input> 하나 생성
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  // 이 체크박스가 어떤 사용자인지 ID 연결
  checkbox.value = user.user_id;
  //만약에 현재 로그인한 사용자인 경우 자동 선택
  if (user.user_id === currentUserId) {
      // 현재 로그인한 사용자는 자동 선택
      checkbox.checked = true;
      // 본인은 선택 해제할 수 없도록 처리
      checkbox.disabled = true;
      }
  // 사용자 이름을 표시할 label 요소 생성
  const label = document.createElement("label");
  // label에 해당 사용자의 이름 표시
  label.textContent = user.name;
  // label 옆에 체크박스 추가
  label.prepend(checkbox);
  // 생성한 사용자 목록을 member-list에 체크박스로 표시
  memberList.appendChild(label);
  });
}); // 팀원 추가 이벤트 종료
// 취소 버튼 요소를 team_create_html에서 가져오기
const cancelButton = document.getElementById("cancel-button");

// 취소 버튼 클릭
cancelButton.addEventListener("click", () => {
    // 팀 생성 화면을 취소하고 이전 화면으로 이동
    window.history.back();
});

// 팀 생성하기 버튼 요소 가져오기
const createTeamButton = document.getElementById("create-team-button");

// 팀 생성하기 버튼 클릭
createTeamButton.addEventListener("click", async () => {
  // 팀 생성에 필요한 값 가져오기
  // 선택한 팀 번호 가져오기
  const teamNumber = Number(
      document.getElementById("team-number").value
  );
  // 입력한 팀 이름 가져오기
  const teamName = document.getElementById("team-name").value;
  // 선택된 팀원의 체크박스 가져오기
  const checkedMembers = document.querySelectorAll(
    '#member-list input[type="checkbox"]:checked'
  );
  // 선택한 팀원의 user_id를 저장할 배열
  const memberIds = [];

  checkedMembers.forEach((checkbox) => {
      // 현재 로그인한 사용자는 제외
      if (checkbox.value !== currentUserId) {
          memberIds.push(checkbox.value);
      }
  });

  // Flask의 POST 요청에 보낼 팀 생성 데이터 구성
  const requestData = {
      team_number: teamNumber,
      team_name: teamName,
      week: week,
      member_ids: memberIds
  }
  // Flask 의 /api/team_pages로 POST요청한다. 
  const response = await fetch("/api/team_pages", {
      method:"POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify(requestData)
  });
  // 서버 응답의 JSON 데이터 받기
  const data = await response.json();

  // 팀 생성 요청 성공 여부 확인
  if (response.ok) {
      // 생성된 team_page_id로 팀 페이지 이동
      window.location.href = `/team/${data.team_page_id}`;
  } else {
      // 팀 생성 실패
      alert(data.error);
  }
});

