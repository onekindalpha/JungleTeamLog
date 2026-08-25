$(function () {
  const teamPageId = $('#team-page-id').val();
  const currentUserId = $('#current-user-id').val();

  // 등록
  $('#scrum-register-btn').on('click', function () {
    const content = $('#scrum-content-input').val().trim();
    if (!content) {
      alert('내용을 입력해주세요');
      return;
    }

    $.ajax({
      url: `/api/team_pages/${teamPageId}/scrums`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ content: content }),
      success: function (res) {
        const s = res.scrum;
        const html = `
          <li class="scrum-item" data-id="${s._id}" data-user-id="${currentUserId}">
            <span class="scrum-date">${s.log_date}</span>
            <span class="scrum-name">${s.user_name}</span>
            <span class="scrum-content">${s.content}</span>
            <button class="scrum-edit-btn">수정</button>
            <button class="scrum-delete-btn">삭제</button>
          </li>
        `;
        $('#scrum-list').prepend(html);  // 리스트 맨 위에 추가
        $('#scrum-content-input').val('');
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });

  // 수정 버튼 클릭 → 인라인 입력창으로 전환
  $('#scrum-list').on('click', '.scrum-edit-btn', function () { //이벤트 위임
    const $li = $(this).closest('.scrum-item');
    const currentContent = $li.find('.scrum-content').text();

    $li.find('.scrum-content').replaceWith(
      `<input type="text" class="scrum-edit-input" value="${currentContent}">`
    );
    $(this).text('저장').removeClass('scrum-edit-btn').addClass('scrum-save-btn');
  });

  // 저장 버튼 클릭 → PATCH 요청
  $('#scrum-list').on('click', '.scrum-save-btn', function () {
    const $li = $(this).closest('.scrum-item');
    const scrumId = $li.data('id');
    const newContent = $li.find('.scrum-edit-input').val().trim();

    if (!newContent) {
      alert('내용을 입력해주세요');
      return;
    }

    $.ajax({
      url: `/api/scrums/${scrumId}`,
      method: 'PATCH',
      contentType: 'application/json',
      data: JSON.stringify({ content: newContent }),
      success: function (res) {
        $li.find('.scrum-edit-input').replaceWith(`<span class="scrum-content">${res.content}</span>`);
        $li.find('.scrum-save-btn').text('수정').removeClass('scrum-save-btn').addClass('scrum-edit-btn');
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });

  // 삭제
  $('#scrum-list').on('click', '.scrum-delete-btn', function () {
    const $li = $(this).closest('.scrum-item');
    const scrumId = $li.data('id');

    if (!confirm('삭제하시겠습니까?')) return;

    $.ajax({
      url: `/api/scrums/${scrumId}`,
      method: 'DELETE',
      success: function () {
        $li.remove();
      },
      error: function (xhr) {
        alert(xhr.responseJSON.error);
      }
    });
  });
});