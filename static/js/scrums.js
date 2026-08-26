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
          <li class="scrum-item box py-3 px-4 mb-2" data-id="${s._id}" data-user-id="${currentUserId}">
            <span class="scrum-date tag is-light">${s.log_date}</span>
            <span class="scrum-name has-text-weight-semibold ml-2">${s.user_name}</span>
            <span class="scrum-content ml-2"></span>
            <div class="buttons is-pulled-right">
              <button class="scrum-edit-btn button is-small is-link is-light">수정</button>
              <button class="scrum-delete-btn button is-small is-danger is-light">삭제</button>
            </div>
          </li>
        `;
        const $li = $(html);
        $li.find('.scrum-content').text(s.content); // XSS 방지: text()로 안전하게 삽입
        $('#scrum-list').prepend($li);  // 리스트 맨 위에 추가
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

    const $input = $('<input type="text" class="scrum-edit-input input is-small">');
    $input.val(currentContent); // XSS 방지: val()로 안전하게 삽입
    $li.find('.scrum-content').replaceWith($input);

    $(this).text('저장')
      .removeClass('scrum-edit-btn is-link is-light')
      .addClass('scrum-save-btn is-primary');
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
        const $span = $('<span class="scrum-content ml-2"></span>').text(res.content);
        $li.find('.scrum-edit-input').replaceWith($span);
        $li.find('.scrum-save-btn').text('수정')
          .removeClass('scrum-save-btn is-primary')
          .addClass('scrum-edit-btn is-link is-light');
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

  // 더보기
  $('#scrum-more-btn').on('click', function () {
      $('.scrum-hidden').removeClass('scrum-hidden');
      $(this).hide();
  });
});